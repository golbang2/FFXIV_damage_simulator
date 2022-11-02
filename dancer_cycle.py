# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 20:36:30 2022

@author: atgol
"""

import range_job as job
import functions as f
import time
import numpy as np
from collections import deque

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
    iteration = 100
    epoch_a = 40
    epoch_b = 5
    interval_prob = 0.005
    phase = 0
    
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
    
    pcr,dcr = f.f_crit(cr)
    pdh = f.f_dh(dh)
    
    dps_list = []
    saber_burst= deque()
    saber = deque()
    
    prob_a = 0.335
    prob_init_a = prob_a - epoch_a * interval_prob * 0.5
    prob_b = 0.125
    prob_init_b = prob_b - epoch_a * interval_prob * 0.5
    

    for a in range(epoch_a):
        saber_burst = deque()
        saber = deque()
        for i in range(iteration):
            if i == iteration-1:
                print_log = 0
            dancer = job.Dancer(cr,dh,dt,dex,wd,spd,weapon_delay,period,print_log)
            dancer.prob_esprit_in_burst = prob_init_a + a * interval_prob
            dancer.prob_esprit_in_normal = prob_b
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
            dps_list.append(dps)
            saber_burst.append((dancer.casts_saberdance_burst, dancer.casts_saberdance_burst/dancer.casts_saberdance,((dancer.casts_saberdance * 0.4-dancer.casts_saberdance_burst)**2)*np.exp(-1)))
            saber.append((dancer.casts_saberdance,((26.8-dancer.casts_saberdance)**2)*np.exp(-1)))
            
            #print('Job: Dancer')
            #print('iterations: ',iteration)
            #print('Average: ',np.mean(dps_list))
            #print('Max: ',np.max(dps_list))
            loss = np.sum(np.array(saber),0)[1] + np.sum(np.array(saber_burst),0)[2]
        print(a, loss)
                
    