# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 20:17:23 2022

@author: atgol
"""

import numpy as np
import pandas as pd
import re

def burst_time(t):
    return (t//120 * 20) + np.min((t%120,20))

class read_mach_log():
    def __init__(self, path = "D:/game_plan/FFXIV/FF Logs - Combat Analysis for FF1.csv", gc = 2.5):
        self.activation_log = pd.read_csv(path)
        self.activation_log = self.activation_log.fillna(0)
        self.gc = gc
        
        p = re.compile('prepares')
        for i in range(len(self.activation_log)-1,0,-1):
            if (p.search(self.activation_log['Event'][i]) == None):
                self.activation_log = self.activation_log.drop(index=i)
        
    def add_potency(self):
        potency_list = []
        auto_list = []
        gc_list = []
        get_skill_name = re.compile("\s\s(.+?)\s\s")
        for i in self.activation_log['Event']:
            skill_name = get_skill_name.findall(i)[0]
            
            if skill_name=='Drill':
                potency_list.append(570)
                gc_list.append(self.gc)
            elif skill_name=='Air Anchor':
                potency_list.append(570)
                gc_list.append(self.gc)
            elif skill_name=='Chain Saw':
                potency_list.append(570)
                gc_list.append(self.gc)
            elif skill_name== 'Heated Split Shot':
                potency_list.append(380)
                gc_list.append(self.gc)
            elif skill_name=='Heated Slug Shot':
                potency_list.append(380)
                gc_list.append(self.gc)
            elif skill_name=='Heated Clean Shot':
                potency_list.append(460)
                gc_list.append(self.gc)
            elif skill_name=='Heat Blast':
                potency_list.append(170)
                gc_list.append(1.5)
            elif skill_name=='Gauss Round':
                potency_list.append(120)
                gc_list.append(0)
            elif skill_name=='Ricochet':
                potency_list.append(120)
                gc_list.append(0)
            elif skill_name=='Arm Punch':
                potency_list.append(120)
                gc_list.append(0)
            elif skill_name=='Pile Bunker':
                potency_list.append(650)
                gc_list.append(0)
            elif skill_name=='Crowned Collider':
                potency_list.append(750)
                gc_list.append(0)
            elif skill_name=='Shot':
                potency_list.append(100)
                gc_list.append(0)
            else:
                print(skill_name)
            
            if skill_name == 'Shot':
                auto_list.append(1)
            else:
                auto_list.append(0)
        self.make_dataframe(auto_list,gc_list,potency_list)
        
    def make_dataframe(self,auto, gc, potency):
        self.activation_log.insert(2,'auto_attack',auto)
        self.activation_log.insert(3,'global_cooldown',gc)
        self.activation_log.insert(4,'potency',potency)
        return self.activation_log
        
class read_bard_log():
    def __init__(self,path = 'd:/game_plan/FFXIV/noya ki-erichthonios.csv', gc = 2.48):
        self.activation_log = pd.read_csv(path)
        self.activation_log = self.activation_log.fillna(0)
        self.gc = gc
        
        p = re.compile('prepares')
        for i in range(len(self.activation_log)-1,0,-1):
            if (p.search(self.activation_log['Event'][i]) == None):
                self.activation_log = self.activation_log.drop(index=i)
    
    def add_potency(self):
        potency_list = []
        auto_list = []
        gc_list = []
        get_skill_name = re.compile("\s\s(.+?)\s\s")
        
        for i in self.activation_log['Event']:
            skill_name = get_skill_name.findall(i)[0]
            if skill_name=='Stormbite':
                potency_list.append(100)
                gc_list.append(self.gc)
            elif skill_name=="the Wanderer's Minuet":
                potency_list.append(100)
                gc_list.append(0)
            elif skill_name=='Caustic Bite':
                potency_list.append(150)
                gc_list.append(self.gc)
            elif skill_name== 'Bloodletter':
                potency_list.append(110)
                gc_list.append(0)
            elif skill_name=='Empyreal Arrow':
                potency_list.append(200)
                gc_list.append(0)
            elif skill_name=='Refulgent Arrow':
                potency_list.append(280)
                gc_list.append(self.gc)
            elif skill_name=='Burst Shot':
                potency_list.append(220)
                gc_list.append(self.gc)
            elif skill_name=='Sidewinder':
                potency_list.append(300)
                gc_list.append(0)
            elif skill_name=='Iron Jaws':
                potency_list.append(100)
                gc_list.append(self.gc)
            elif skill_name=="Pitch Perfect":
                potency_list.append(360)
                gc_list.append(0)
            elif skill_name=="Mage's Ballad":
                potency_list.append(100)
                gc_list.append(0)
            elif skill_name=="Army's Paeon":
                potency_list.append(100)
                gc_list.append(0)
            elif skill_name=='Shot':
                potency_list.append(100)
                gc_list.append(0)
            elif skill_name == 'Apex Arrow':
                potency_list.append(600)
                gc_list.append(self.gc)
            elif skill_name == 'Blast Arrow':
                potency_list.append(600)
                gc_list.append(self.gc)
            else:
                print(skill_name)
            
            if skill_name == 'Shot':
                auto_list.append(1)
            else:
                auto_list.append(0)
    
        self.make_dataframe(auto_list,gc_list,potency_list)
        
    def make_dataframe(self,auto, gc, potency):
        self.activation_log.insert(2,'auto_attack',auto)
        self.activation_log.insert(3,'global_cooldown',gc)
        self.activation_log.insert(4,'potency',potency)
        return self.activation_log