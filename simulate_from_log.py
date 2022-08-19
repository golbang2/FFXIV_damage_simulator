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
    def __init__(self,file_name="D:/game_plan/FFXIV/Jomusse_first.csv"):
        active_log = read_log.read_from_csv(file_name).activation_log
        self.character = mach.machinist(2.5, 2121, 1626,1615,2575,120,400)
        
        self.simulated_damage = self.simulate_from_log(active_log)
        
    def simulate_from_log(self,active_log):
        damage_list = []
        crit_list = []
        dhit_list = []
        
        for i in active_log.index.tolist():
            if active_log['auto_attack'][i]:
                dmg,is_cr,is_dh = self.character.auto_shot()
                crit_list.append(is_cr)
                dhit_list.append(is_dh)
                damage_list.append(dmg)
            elif active_log['reassemble'][i]:
                dmg,is_cr,is_dh = self.character.calculate_dmg(active_log['potency'][i],reassemble=1)
                crit_list.append(is_cr)
                dhit_list.append(is_dh)
                damage_list.append(dmg)
            else:
                dmg,is_cr,is_dh = self.character.calculate_dmg(active_log['potency'][i],reassemble=0)
                crit_list.append(is_cr)
                dhit_list.append(is_dh)
                damage_list.append(dmg)
        simulated_damage = damage_dataframe(damage_list, crit_list, dhit_list)
        return simulated_damage
        
class read_bard():
    def __init__(self,file_name):
        active_log = read_log.read_from_csv(file_name).activation_log
        self.character = bard.bard(2.5, 2121, 1626,1615,2575,120,400)
        
        self.simulated_damage = self.simulate_from_log(active_log)
        
        
        
def damage_dataframe(dmg_list, crit_list, dhit_list):
    df_damage = pd.DataFrame(dmg_list, columns = ['damage'])
    df_damage.insert(1,'cr',crit_list)
    df_damage.insert(2,'dh',dhit_list)
    return df_damage