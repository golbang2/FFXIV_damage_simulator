# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 23:01:43 2022

@author: atgol
"""

import range_job

class Environment:
    def __init__(self,job):
        if job=='bard':
            self.job = 'bard'   
            self.action_space = 17 #num_of_skills
            self.observation_space = 11+5+1+2 #cooltime+buff+gc+dot
            self.job_class = range_job()
            
    def reset(self):
        if self.job == 'bard':
            self.cr = 2229
            self.dt = 1381
            self.dh = 1662
            self.spd = 479
            self.stat = int(2574*1.05)
            
            self.wd = 120
            self.weapon_delay = 3.04

            self.main = 390
            self.sub = 400
            self.div = 1900
            self.job_class = range_job.Bard(cr,dh,dt,stat,wd,spd,period,print_log = print_log)
            
        return 0
    
    def step(self, action):
        if self.job_class(action):
            
        
        return obs, reward, done, info