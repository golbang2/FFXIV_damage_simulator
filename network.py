import range_job
from ray.rllib.algorithms.ppo import PPOConfig

algo = (
    PPOConfig()
    .rollouts(num_rollout_workers=1)
    .resources(num_gpus=0)
    .environment(env="CartPole-v1")
    .build()
)


class MyEnv():
    def __init__(self, env):
        self.env = env
        self.action_space = env.action_space
        self.observation_space = env.observation_space
    def reset(self):
        obs = self.env.start()
        return state
    def step(self, action):
        return obs, reward, done, info