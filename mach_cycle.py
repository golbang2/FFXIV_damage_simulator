# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 18:51:11 2022

@author: atgol
"""

import range_job as job
import functions as f
import time
import numpy as np

def opening(mach):
    mach.buff_reassemble = 1 * mach.time_multiply
    mach.ab_reassemble = 1
    mach.cool_reassemble = 51 * mach.time_multiply
    mach.airanchor()
    mach.gaussround()
    mach.ricochet()
    mach.drill()
    mach.barrelstabilizer()
    mach.splitshot()
    mach.slugshot()
    mach.gaussround()
    mach.ricochet()
    mach.cleanshot()
    mach.reassemble()
    mach.wildfire()
    mach.chainsaw()
    mach.automaton_queen()
    mach.hypercharge()
    mach.heatblast()
    mach.ricochet()
    mach.heatblast()
    mach.gaussround()
    mach.heatblast()
    mach.ricochet()
    mach.heatblast()
    mach.gaussround()
    mach.ricochet()
    mach.heatblast()
    mach.drill()

def GC(mach):
    if mach.buff_hypercharge >0:
        mach.heatblast()
    elif mach.cool_chainsaw <= mach.global_cooldown:
        mach.chainsaw()
    elif mach.cool_airanchor <= mach.global_cooldown:
        mach.airanchor()
    elif mach.cool_drill <= mach.global_cooldown:
        mach.drill()    
    elif mach.combo == 0:
        mach.splitshot()
    elif mach.combo == 1:
        mach.slugshot()
    elif mach.combo == 2:
        mach.cleanshot()

def NGC(mach):
    if mach.battery>=90:
        mach.automaton_queen()
    elif (mach.heat>=50 and min(mach.cool_drill,mach.cool_airanchor,mach.cool_chainsaw)> 8 * mach.time_multiply):
        mach.hypercharge()
    elif (mach.ab_ricochet>0 and mach.ab_ricochet>=mach.ab_gaussround):
        mach.ricochet()
    elif (mach.ab_gaussround>0 and mach.ab_gaussround>mach.ab_ricochet):
        mach.gaussround()
    elif mach.ab_ricochet>0:
        mach.ricochet()
    elif mach.ab_gaussround>0:
        mach.gaussround()
    elif ((mach.cool_chainsaw <= mach.global_cooldown or mach.cool_drill <= mach.global_cooldown or mach.cool_airanchor <= mach.global_cooldown) and mach.ab_reassemble>0):
        mach.reassemble()
        
def burst(mach):
    if mach.cool_potion==0:
        mach.potion()
    mach.airanchor()
    mach.gaussround()
    mach.ricochet()
    mach.drill()
    if mach.heat>=50:
        mach.hypercharge()
        mach.heatblast()
        mach.barrelstabilizer()
        mach.heatblast()
        mach.gaussround()
        mach.heatblast()
        mach.ricochet()
        mach.heatblast()
        mach.gaussround()
        mach.heatblast()
        mach.reassemble()
        mach.chainsaw()
        mach.wildfire()
        mach.hypercharge()
        mach.heatblast()
        mach.ricochet()
        mach.heatblast()
        mach.gaussround()
        mach.heatblast()
        mach.ricochet()
        mach.heatblast()
        mach.drill()
    else:
        mach.barrelstabilizer()
        GC(mach)
        GC(mach)
        NGC(mach)
        NGC(mach)
        GC(mach)
        mach.wildfire()
        mach.chainsaw()
        mach.hypercharge()
        for i in range(5):
            mach.heatblast()
            NGC(mach)
        mach.drill()
    
def skill_dps(skill_name):
    dps = np.array(act_log[act_log['Skill']==skill_name]['Damage']).sum()/(mach.elapsed*0.01)
    casts = len(act_log[act_log['Skill']==skill_name]['Damage'])
    total_dmg = np.array(act_log[act_log['Skill']==skill_name]['Damage']).sum()
    
    crit_count = len(act_log[(act_log['Skill']==skill_name) & (act_log['Crit']=='T')])
    dhit_count = len(act_log[(act_log['Skill']==skill_name) & (act_log['Dhit']=='T')])
    return dps, casts, round(total_dmg/casts,2),round(crit_count/casts,2),round(dhit_count/casts,2)
    
if __name__=='__main__':
    #https://etro.gg/gearset/e8c4176b-aad2-4719-9774-36f6d0377624
    period = 410
    iteration = 100
    print_log = 0
    
    cr = 2193
    dt = 1507
    dh = 1662
    spd = 400
    dex = int(2574*1.05)
    wd = 120
    weapon_delay = 2.64

    main = 390
    sub = 400
    div = 1900
    
    pcr,dcr = f.f_crit(cr)
    pdh = f.f_dh(dh)
    
    dps_list = []
            
    for i in range(iteration):
        if i ==iteration-1:
            print_log = 1
        mach = job.Machinist(cr,dh,dt,dex,wd,spd,weapon_delay,period,print_log = print_log)
        opening(mach)
        while not mach.done:
            if (mach.elapsed*0.01%120)<5:
                burst(mach)
            GC(mach)
            NGC(mach)
            NGC(mach)
        
        act_log = mach.extract_log()
        dmg_log = act_log['Damage'].to_numpy()
        dps = np.sum(dmg_log)/(mach.elapsed*0.01)
        dps_list.append(dps)
    
    print('Job: Machinist')
    print('iterations: ',iteration)
    print('Average: ',np.mean(dps_list))
    print('Max: ',np.max(dps_list))
