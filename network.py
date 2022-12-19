# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 23:16:09 2022

@author: atgol
"""

import multiprocessing
import multiprocessing.connection
from typing import Dict, List

import cv2
import gym
import numpy as np
import torch
from labml import monit, tracker, logger, experiment
from torch import nn
from torch import optim
from torch.distributions import Categorical
from torch.nn import functional as F

if torch.cuda.is_available():
    device = torch.device("cuda:1")
else:
    device = torch.device("cpu")
    
class Game:
    def __init__(self, seed: int):
        self.env = gym.make('BreakoutNoFrameskip-v4')
        self.env.seed(seed)
        
        self.obs_4 = np.zeros((4, 84, 84))
        
        self.rewards = []
        
        self.lives = 0
        
    def step(self, action):
        reward = 0.
        done = None
        for i in range(4):
            obs, r, done, info = self.env.step(action)
            reward += r
            lives = self.env.unwrapped.ale.lives()
            if lives < self.lives:
                done = True
                break
        obs = self._process_obs(obs)
        self.rewards.append(reward)
        if done:
            episode_info = {"reward": sum(self.rewards), "length": len(self.rewards)}
            self.reset()
        else:
            episode_info = None
            self.obs_4 = np.roll(self.obs_4, shift=-1, axis=0)
            self.obs_4[-1] = obs
        return self.obs_4, reward, done, episode_info
    
    def reset(self):
        obs = self.env.reset()
        obs = self._process_obs(obs)
        for i in range(4):
            self.obs_4[i] = obs
        self.rewards = []

        self.lives = self.env.unwrapped.ale.lives()

        return self.obs_4
            
    
def worker_process(remote: multiprocessing.connection.Connection, seed: int):
    game = Game(seed)
    while True:
        cmd, data = remote.recv()
        if cmd == "step":
            remote.send(game.step(data))
        elif cmd == "reset":
            remote.send(game.reset())
        elif cmd == "close":
            remote.close()
            break
        else:
            raise NotImplementedError
            
class Worker:
    def __init__(self, seed):
        self.child, parent = multiprocessing.Pipe()
        self.process = multiprocessing.Process(target=worker_process, args=(parent, seed))
        self.process.start()
        
class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels=4, out_channels=32, kernel_size=8, stride=4)
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=4, stride=2)
        self.conv3 = nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, stride=1)
        self.lin = nn.Linear(in_features=7 * 7 * 64, out_features=512)
        self.pi_logits = nn.Linear(in_features=512, out_features=4)
        self.value = nn.Linear(in_features=512, out_features=1)
    
    def forward(self, obs: torch.Tensor):
        h = F.relu(self.conv1(obs))
        h = F.relu(self.conv2(h))
        h = F.relu(self.conv3(h))
        h = h.reshape((-1, 7 * 7 * 64))

        h = F.relu(self.lin(h))

        pi = Categorical(logits=self.pi_logits(h))
        value = self.value(h).reshape(-1)

        return pi, value
    
def obs_to_torch(obs: np.ndarray) -> torch.Tensor:
    return torch.tensor(obs, dtype=torch.float32, device=device) / 255.

class Main:
    def __init__(self):
        self.gamma = 0.99
        self.lamda = 0.95
        self.updates = 10000
        self.epochs = 4
        self.n_workers = 8
        self.worker_steps = 128
        self.n_mini_batch = 4
        self.batch_size = self.n_workers * self.worker_steps
        self.mini_batch_size = self.batch_size // self.n_mini_batch
        assert (self.batch_size % self.n_mini_batch == 0)
        self.workers = [Worker(47 + i) for i in range(self.n_workers)]
        self.obs = np.zeros((self.n_workers, 4, 84, 84), dtype=np.uint8)
        for worker in self.workers:
            worker.child.send(("reset", None))
        for i, worker in enumerate(self.workers):
            self.obs[i] = worker.child.recv()
        self.model = Model().to(device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=2.5e-4)
        
    def sample(self) -> (Dict[str, np.ndarray], List):
        rewards = np.zeros((self.n_workers, self.worker_steps), dtype=np.float32)
        actions = np.zeros((self.n_workers, self.worker_steps), dtype=np.int32)
        done = np.zeros((self.n_workers, self.worker_steps), dtype=np.bool)
        obs = np.zeros((self.n_workers, self.worker_steps, 4, 84, 84), dtype=np.uint8)
        log_pis = np.zeros((self.n_workers, self.worker_steps), dtype=np.float32)
        values = np.zeros((self.n_workers, self.worker_steps), dtype=np.float32)
    
        for t in range(self.worker_steps):
            with torch.no_grad():
                obs[:, t] = self.obs
                pi, v = self.model(obs_to_torch(self.obs))
                values[:, t] = v.cpu().numpy()
                a = pi.sample()
                actions[:, t] = a.cpu().numpy()
                log_pis[:, t] = pi.log_prob(a).cpu().numpy()
            for w, worker in enumerate(self.workers):
                worker.child.send(("step", actions[w, t]))

            for w, worker in enumerate(self.workers):
                self.obs[w], rewards[w, t], done[w, t], info = worker.child.recv()
                if info:
                    tracker.add('reward', info['reward'])
                    tracker.add('length', info['length'])
        advantages = self._calc_advantages(done, rewards, values)
        samples = {
            'obs': obs,
            'actions': actions,
            'values': values,
            'log_pis': log_pis,
            'advantages': advantages }
        samples_flat = {}
        for k, v in samples.items():
            v = v.reshape(v.shape[0] * v.shape[1], *v.shape[2:])
            if k == 'obs':
                samples_flat[k] = obs_to_torch(v)
            else:
                samples_flat[k] = torch.tensor(v, device=device)

        return samples_flat

    def _calc_advantages(self, done: np.ndarray, rewards: np.ndarray, values: np.ndarray) -> np.ndarray:
        advantages = np.zeros((self.n_workers, self.worker_steps), dtype=np.float32)
        last_advantage = 0
        _, last_value = self.model(obs_to_torch(self.obs))
        last_value = last_value.cpu().data.numpy()
        for t in reversed(range(self.worker_steps)):
            mask = 1.0 - done[:, t]
            last_value = last_value * mask
            last_advantage = last_advantage * mask
            delta = rewards[:, t] + self.gamma * last_value - values[:, t]
            last_advantage = delta + self.gamma * self.lamda * last_advantage
            advantages[:, t] = last_advantage
            last_value = values[:, t]
        return advantages
    
    
    def train(self, samples: Dict[str, torch.Tensor], learning_rate: float, clip_range: float):
        for _ in range(self.epochs):
            indexes = torch.randperm(self.batch_size)
            for start in range(0, self.batch_size, self.mini_batch_size):
                    end = start + self.mini_batch_size
                    mini_batch_indexes = indexes[start: end]
                    mini_batch = {}
                    for k, v in samples.items():
                        mini_batch[k] = v[mini_batch_indexes]
                    loss = self._calc_loss(clip_range=clip_range,samples=mini_batch)
                    for pg in self.optimizer.param_groups:
                        pg['lr'] = learning_rate
                    self.optimizer.zero_grad()
                    loss.backward()
                    torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=0.5)
                    self.optimizer.step() 
                    
    def _normalize(adv: torch.Tensor):
        return (adv - adv.mean()) / (adv.std() + 1e-8)
    
    def _calc_loss(self, samples: Dict[str, torch.Tensor], clip_range: float) -> torch.Tensor:
        sampled_return = samples['values'] + samples['advantages']
        sampled_normalized_advantage = self._normalize(samples['advantages'])
        pi, value = self.model(samples['obs'])
        log_pi = pi.log_prob(samples['actions'])
        ratio = torch.exp(log_pi - samples['log_pis'])
        clipped_ratio = ratio.clamp(min=1.0 - clip_range,max=1.0 + clip_range)
        policy_reward = torch.min(ratio * sampled_normalized_advantage, clipped_ratio * sampled_normalized_advantage)
        policy_reward = policy_reward.mean()
        entropy_bonus = pi.entropy()
        entropy_bonus = entropy_bonus.mean()
        clipped_value = samples['values'] + (value - samples['values']).clamp(min=-clip_range,max=clip_range)
        vf_loss = torch.max((value - sampled_return) ** 2, (clipped_value - sampled_return) ** 2)
        vf_loss = 0.5 * vf_loss.mean()
        loss = -(policy_reward - 0.5 * vf_loss + 0.01 * entropy_bonus)
        approx_kl_divergence = .5 * ((samples['log_pis'] - log_pi) ** 2).mean()
        clip_fraction = (abs((ratio - 1.0)) > clip_range).to(torch.float).mean()
    
        tracker.add({'policy_reward': policy_reward, 
                     'vf_loss': vf_loss,
                     'entropy_bonus': entropy_bonus,
                     'kl_div': approx_kl_divergence,
                     'clip_fraction': clip_fraction})
        return loss
    
    def run_training_loop(self):
        tracker.set_queue('reward', 100, True)
        tracker.set_queue('length', 100, True)
    
        for update in monit.loop(self.updates):
            progress = update / self.updates
            learning_rate = 2.5e-4 * (1 - progress)
            clip_range = 0.1 * (1 - progress)
            samples = self.sample()
            self.train(samples, learning_rate, clip_range)
            tracker.save()
            if (update + 1) % 1_000 == 0:
                logger.log()
                
    def destroy(self):
        for worker in self.workers:
            worker.child.send(("close", None))

if __name__ == "__main__":
    experiment.create()
    m = Main()
    experiment.start()
    m.run_training_loop()
    m.destroy()