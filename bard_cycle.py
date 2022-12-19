# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 16:26:50 2022

@author: Taeyoon
"""

import range_job as job
import time
import numpy as np
import matplotlib.pyplot as plt

def opening(bard):
    bard.stormbite()
    bard.wanderer_minuet()
    bard.raging()
    bard.causticbite()
    bard.empyreal()
    bard.blood()
    bard.burst_shot()
    bard.radient()
    bard.battle()
    bard.burst_shot()
    if bard.available_straight:
        bard.sidewinder()
        ngc_in_wanderer(bard)
        bard.burst_shot()
        bard.barrage()
        bard.burst_shot()
        bard.burst_shot()
        bard.empyreal()
        bard.iron_jaws()
    else:
        bard.barrage()
        ngc_in_wanderer(bard)
        bard.burst_shot()
        bard.sidewinder()
        ngc_in_wanderer(bard)
        bard.burst_shot()
        ngc_in_wanderer(bard)
        ngc_in_wanderer(bard)
        bard.burst_shot()
        ngc_in_wanderer(bard)
        ngc_in_wanderer(bard)
        bard.burst_shot()
        ngc_in_wanderer(bard)
        ngc_in_wanderer(bard)
        bard.empyreal()
        bard.iron_jaws()

def burst(bard):
    gc_in_wanderer(bard)
    bard.wanderer_minuet()
    bard.raging()
    gc_in_wanderer(bard)
    if bard.cool_potion==0:
        bard.potion()
    else:
        ngc_in_wanderer(bard)
        ngc_in_wanderer(bard)
    gc_in_wanderer(bard)
    bard.radient()
    bard.battle()
    if bard.dot_caustic< 38 * bard.time_multiply:
        bard.iron_jaws()
    else:
        gc_in_wanderer(bard)

def gc_in_wanderer(bard):
    if (bard.dot_caustic < bard.gc_ap or bard.dot_storm< bard.gc_ap):
        bard.iron_jaws()
    elif bard.available_blast:
        bard.blast_arrow()
    elif (bard.buff_raging >0 and bard.buff_radient>0 and bard.buff_battle>0 and bard.soul>80):
        bard.apex_arrow()
    else:
        bard.burst_shot()

def ngc_in_wanderer(bard):
    if bard.stack_wanderer==3:
        bard.pitch()
    elif bard.cool_barrage == 0:
        bard.barrage()
    elif bard.cool_sidewinder<=0:
        bard.sidewinder()
    elif bard.cool_empyreal<=0:
        bard.empyreal()
    elif bard.available_blood>0:
        bard.blood()
    
    if bard.buff_wanderer< 3 * bard.time_multiply:
        if bard.stack_wanderer>0:
            bard.pitch()
        else:
            bard.mage_ballad()
        
def gc_in_mage(bard):
    if (bard.dot_caustic < bard.gc_ap or bard.dot_storm < bard.gc_ap):
        bard.iron_jaws()
    elif (bard.soul==100 and bard.buff_mage > 15 * bard.time_multiply):
        bard.apex_arrow()
    elif (bard.soul>80 and bard.buff_mage > 18 * bard.time_multiply and bard.buff_mage<21 * bard.time_multiply):
        bard.apex_arrow()
    elif bard.available_blast:
        bard.blast_arrow()
    else:
        bard.burst_shot()
        
def ngc_in_mage(bard):
    if bard.cool_sidewinder<=0:
        bard.sidewinder()
    elif bard.cool_empyreal<=0:
        bard.empyreal()
    elif bard.available_blood>0:
        bard.blood()
        
    if bard.buff_mage < 12 * bard.time_multiply:
        bard.army_paeon()
        
def gc_in_army(bard):
    if (bard.dot_caustic< bard.gc_ap or bard.dot_storm< bard.gc_ap):
        bard.iron_jaws()
    else:
        bard.burst_shot()
        
def ngc_in_army(bard):
    if (bard.available_blood>2 and bard.cool_blood<bard.gc_ap):
        bard.blood()
    if bard.cool_empyreal<=0:
        bard.empyreal()
        
def GC(bard):
    if bard.buff_wanderer>0:
        gc_in_wanderer(bard)
    elif bard.buff_mage>0:
        gc_in_mage(bard)
    else:
        gc_in_army(bard)
        
def NGC(bard):
    if bard.buff_wanderer>0:
        ngc_in_wanderer(bard)
    elif bard.buff_mage>0:
        ngc_in_mage(bard)
    elif bard.buff_army>0:
        ngc_in_army(bard)
        
def skill_dps(skill_name):
    dps = np.array(act_log[act_log['Skill']==skill_name]['Damage']).sum()/(bard.elapsed*0.01)
    casts = len(act_log[act_log['Skill']==skill_name]['Damage'])
    total_dmg = np.array(act_log[act_log['Skill']==skill_name]['Damage']).sum()
    
    crit_count = len(act_log[(act_log['Skill']==skill_name) & (act_log['Crit']=='T')])
    dhit_count = len(act_log[(act_log['Skill']==skill_name) & (act_log['Dhit']=='T')])
    return dps, casts, total_dmg,crit_count/casts,dhit_count/casts


if __name__=='__main__':
    #https://etro.gg/gearset/cec981af-25c7-4ffb-905e-3024411b797a
    period = 410
    iteration = 200
    print_log = 0
    
    cr = 2229
    dt = 1381
    dh = 1662
    spd = 479
    stat = int(2574*1.05)
    
    wd = 120
    weapon_delay = 3.04

    main = 390
    sub = 400
    div = 1900
    
    dps = 0
    bard_dps_list = []
    
    for i in range(iteration):
        if i==iteration-1:
            print_log =1
        bard = job.Bard(cr,dh,dt,stat,wd,spd,period,print_log = print_log)
        opening(bard)
        while not bard.done:
            if bard.cool_wanderer==0:
                burst(bard)
            GC(bard)
            NGC(bard)
            NGC(bard)
        
        act_log = bard.extract_log()
        dmg_log = act_log['Damage'].to_numpy()
        dps = np.sum(dmg_log)/(bard.elapsed*0.01)
        bard_dps_list.append(dps)    
    print('Job: Bard')
    print('iterations:',iteration)
    print('Average:',np.mean(bard_dps_list))
    print('Max:',np.max(bard_dps_list))
    plt.figure(figsize = (10,4))
    plt.hist(bard_dps_list, bins=15,rwidth = 0.8, color = 'green')
    plt.xlabel('Bard DPS', fontsize = 14)
    plt.show()