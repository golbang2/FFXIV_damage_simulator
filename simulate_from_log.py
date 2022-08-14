# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 14:58:37 2022

@author: atgol
"""

import ffxiv_calculate_damage as f
import numpy as np
import read_log
import mach

active_log = read_log.read_from_csv("D:/game_plan/FFXIV/Jomusse_first.csv").activation_log
character = mach.machinist(2.5, 2121, 1626,1615,2575,120,400)


damage_list = []
crit_list = []
dhit_list = []

for i in active_log.index.tolist():
    if active_log['auto_attack'][i]:
        dmg,is_cr,is_dh = character.auto_shot()
        damage_list.append(dmg)
    elif active_log['reassemble'][i]:
        dmg,is_cr,is_dh = character.calculate_dmg(active_log['potency'][i],reassemble=1)
        damage_list.append(dmg)
    else:
        dmg,is_cr,is_dh = character.calculate_dmg(active_log['potency'][i],reassemble=0)
        damage_list.append(dmg)