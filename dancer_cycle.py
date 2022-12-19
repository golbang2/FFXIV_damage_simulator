# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 20:36:30 2022

@author: atgol
"""

import range_job as job
import functions as f
import numpy as np
import matplotlib.pyplot as plt

def opening(dancer):
    dancer.opening_standard_finish()
    dancer.technical_finish()
    dancer.devilment()
    dancer.starfall_dance()
    dancer.flourish()
    dancer.fandance_third()
    dancer.tillana()
    dancer.fandance_fourth()
    GC(dancer)
    NGC(dancer)
    NGC(dancer)
    GC(dancer)
    
def burst(dancer):
    dancer.technical_finish()
    dancer.devilment()
    dancer.starfall_dance()
    dancer.flourish()
    dancer.fandance_third()
    dancer.tillana()
    dancer.fandance_fourth()
    GC(dancer)
    NGC(dancer)
    NGC(dancer)
    GC(dancer)

def GC_in_burst(dancer):
    if dancer.esprit>=50:
        dancer.saber_dance()
    elif dancer.cool_standard<dancer.global_cooldown:
        dancer.standard_finish()
    elif dancer.ab_fountainfall>0:
        dancer.fountainfall()
    elif dancer.ab_reverse_cascade>0:
        dancer.reverse_cascade()
    elif dancer.combo ==1:
        dancer.fountain()
    else:
        dancer.cascade()

def GC(dancer):
    if dancer.buff_technical>0:
        GC_in_burst(dancer)
    elif dancer.esprit>=80:
        dancer.saber_dance()
    elif dancer.cool_standard<dancer.global_cooldown:
        dancer.standard_finish()
    elif dancer.ab_fountainfall>0:
        dancer.fountainfall()
    elif dancer.ab_reverse_cascade>0:
        dancer.reverse_cascade()
    elif dancer.combo ==1:
        dancer.fountain()
    else:
        dancer.cascade()

def NGC_in_burst(dancer):
    if dancer.ab_third>0:
        dancer.fandance_third()
    elif dancer.ab_fandance==4:
        dancer.fandance()
    elif dancer.ab_fourth>0:
        dancer.fandance_fourth()
    elif dancer.ab_fandance>0:
        dancer.fandance()
        
def NGC(dancer):
    if dancer.buff_technical>0:
        NGC_in_burst(dancer)
    elif dancer.cool_flourish==0:
        dancer.flourish()
    elif dancer.ab_fandance==4:
        dancer.fandance()
    elif dancer.ab_third>0:
        dancer.fandance_third()
    elif (dancer.ngc==2 and dancer.cool_potion==0):
        dancer.potion()

def skill_dps(skill_name):
    dps = np.array(act_log[act_log['Skill']==skill_name]['Damage']).sum()/(dancer.elapsed*0.01)
    casts = len(act_log[act_log['Skill']==skill_name]['Damage'])
    total_dmg = np.array(act_log[act_log['Skill']==skill_name]['Damage']).sum()
    min_hit = np.min(np.array(act_log[act_log['Skill']==skill_name]['Damage']))
    
    crit_count = len(act_log[(act_log['Skill']==skill_name) & (act_log['Crit']=='T')])
    dhit_count = len(act_log[(act_log['Skill']==skill_name) & (act_log['Dhit']=='T')])
    return dps, casts, round(total_dmg/casts,2),round(crit_count/casts,2),round(dhit_count/casts,2),min_hit

if __name__=='__main__':
    #https://etro.gg/gearset/fd333e44-0f90-42a6-a070-044b332bb54e
    period = 410
    print_log = 0
    iteration = 200
    
    cr = 2283
    dt = 1453
    dh = 1477
    spd = 549
    dex = int(2574 *1.05)
    wd = 120
    weapon_delay = 3.12

    main = 390
    sub = 400
    div = 1900
    
    dancer_dps_list = []
    
    for i in range(iteration):
        if i == iteration-1:
            print_log = 0
        dancer = job.Dancer(cr,dh,dt,dex,wd,spd,weapon_delay,period,print_log)
        opening(dancer)
        while not dancer.done:
            if dancer.cool_technical<dancer.global_cooldown:
                burst(dancer)
            GC(dancer)
            NGC(dancer)
            NGC(dancer)
            
        act_log = dancer.extract_log()
        dmg_log = act_log['Damage'].to_numpy()
        dps = np.sum(dmg_log)/(dancer.elapsed*0.01)
        dancer_dps_list.append(dps)
        
    print('Job: Dancer')
    print('iterations: ',iteration)
    print('Average: ',np.mean(dancer_dps_list))
    print('Max: ',np.max(dancer_dps_list))
    
    plt.figure(figsize = (10,4))
    plt.hist(dancer_dps_list, bins=15,rwidth = 0.8, color = 'goldenrod')
    plt.xlabel('Dancer DPS', fontsize = 14)
    plt.show()
                    
    