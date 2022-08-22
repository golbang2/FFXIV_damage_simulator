# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 14:58:37 2022

@author: atgol
"""

import ffxiv_calculate_damage as f
import numpy as np
import read_log
import mach
import bard
import pandas as pd

class read_machinist():
    def __init__(self,file_name="D:/game_plan/FFXIV/FF Logs - Combat Analysis for FF1.csv"):
        
        reading_log = read_log.read_from_csv(file_name)
        self.active_log = reading_log.add_potency()
        self.period = np.sum(self.active_log['global_cooldown']) - 2.5
        self.character = mach.machinist(gc = 2.5, cr = 2121, dh = 1626, dt = 1615, stat = 2575, wd = 120,spd = 400, period = self.period)
        
    def simulate_from_log(self):
        damage_list = []
        crit_list = []
        dhit_list = []
        
        for i in self.active_log.index.tolist():
            if self.active_log['auto_attack'][i]:
                dmg,is_cr,is_dh = self.character.auto_shot()
                crit_list.append(is_cr)
                dhit_list.append(is_dh)
                damage_list.append(dmg)
            elif self.active_log['reassemble'][i]:
                dmg,is_cr,is_dh = self.character.calculate_dmg(self.active_log['potency'][i],reassemble=1)
                crit_list.append(is_cr)
                dhit_list.append(is_dh)
                damage_list.append(dmg)
            else:
                dmg,is_cr,is_dh = self.character.calculate_dmg(self.active_log['potency'][i],reassemble=0)
                crit_list.append(is_cr)
                dhit_list.append(is_dh)
                damage_list.append(dmg)
        simulated_damage = damage_dataframe(damage_list, crit_list, dhit_list)
        return simulated_damage
    
    def repeat_simulate(self,epoch):
        log_list = []
        for i in range(epoch):
            log_list.append(self.simulate_from_log())
            
        dps_list = []
        for i in log_list:
            dps = i['damage']/self.period
            dps_list.append(dps)
        return log_list
            
class read_bard():
    def __init__(self,file_name):
        active_log = read_log.read_from_csv(file_name).activation_log
        self.character = bard.bard(gc = 2.08, cr = 2229, dh = 1662, dt = 1381, stat = 2575, wd = 120,spd = 479, period = 120)
        self.simulated_damage = self.simulate_from_log(active_log)
    
    def simulate_from_log(self,active_log):
        damage_list=[]
        crit_list = []
        dhit_list = []
        
        for i in active_log.index.tolist():
            if active_log['auto_attack'][i]:
                dmg,is_cr,is_dh = self.character.auto_shot()
                crit_list.append(is_cr)
                dhit_list.append(is_dh)
                damage_list.append(dmg)
            
def damage_dataframe(dmg_list, crit_list, dhit_list):
    df_damage = pd.DataFrame(dmg_list, columns = ['damage'])
    df_damage.insert(1,'cr',crit_list)
    df_damage.insert(2,'dh',dhit_list)
    return df_damage


if __name__=='__main__':
    read_mach = read_machinist()
    data = read_mach.simulate_from_log()