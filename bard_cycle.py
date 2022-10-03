# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 16:26:50 2022

@author: Taeyoon
"""

import bard
import functions as f

def opening(agent):
    agent.stormbite()
    agent.wanderer_minuet()
    agent.raging()
    agent.causticbite()
    agent.empyreal()
    agent.blood()
    agent.burst_shot()
    agent.radient()
    agent.battle()
    agent.burst_shot()
    
    if agent.available_straight:
        agent.sidewinder()
        ngc_in_minuet(agent)
        agent.burst_shot()
        agent.barrage()
        agent.burst_shot()
        agent.burst_shot()
        agent.empyreal()
        agent.iron_jaws()
    else:
        agent.barrage()
        agent.burst_shot()
        agent.sidewinder()
        agent.burst_shot()
        agent.burst_shot()
        agent.burst_shot()
        agent.empyreal()
        agent.iron_jaws()

def burst(agent):
    gc_in_minuet(agent)
    agent.wanderer_minuet()
    agent.raging()
    gc_in_minuet(agent)
    ngc_in_minuet(agent)
    ngc_in_minuet(agent)
    gc_in_minuet(agent)
    agent.radient()
    agent.battle()
    gc_in_minuet(agent)

def gc_in_minuet(agent):
    if (agent.dot_caustic<3 * agent.time_multiply or agent.dot_storm<3 * agent.time_multiply):
        agent.iron_jaws()
    elif agent.available_blast:
        agent.blast_arrow()
    elif (agent.buff_raging >0 and agent.buff_radient>0 and agent.buff_battle>0 and agent.soul>80):
        agent.apex_arrow()
    else:
        agent.burst_shot()
        

def ngc_in_minuet(agent):
    if agent.stack_wanderer==3:
        agent.pitch()
    elif agent.cool_sidewinder<=0:
        agent.sidewinder()
    elif agent.cool_empyreal<=0:
        agent.empyreal()
    elif agent.available_blood>0:
        agent.blood()
    
    if agent.buff_wanderer<3*agent.time_multiply:
        if agent.stack_wanderer>0:
            agent.pitch()
        else:
            agent.mage_ballad()
        
def gc_in_mage(agent):
    if (agent.dot_caustic < 3 * agent.time_multiply or agent.dot_storm < 3 * agent.time_multiply):
        agent.iron_jaws()
    elif (agent.soul==100 and agent.buff_mage > 15 * agent.time_multiply):
        agent.apex_arrow()
    elif (agent.soul>80 and agent.buff_mage > 18 * agent.time_multiply and agent.buff_mage<21 * agent.time_multiply):
        agent.apex_arrow()
    elif agent.available_blast:
        agent.blast_arrow()
    else:
        agent.burst_shot()
        
def ngc_in_mage(agent):
    if agent.stack_wanderer==3:
        agent.pitch()
    elif agent.cool_sidewinder<0:
        agent.sidewinder()
    elif agent.cool_empyreal<0:
        agent.empyreal()
    elif agent.available_blood>0:
        agent.blood()
        
    if agent.buff_wanderer < 15 * agent.time_multiply:
        agent.army_paeon()
        
def gc_in_army(agent):
    if (agent.dot_caustic<3 or agent.dot_storm<3):
        agent.iron_jaws()
    else:
        agent.burst_shot()
        
def ngc_in_army(agent):
    if (agent.available_blood>2 and agent.cool_blood<agent.gc_ap):
        agent.blood()
    if agent.cool_empyreal<=0:
        agent.empyreal()
    if agent.buff_army<3 * agent.time_multiply:
        agent.wanderer_minuet()
        
if __name__=='__main__':
    period = 300
    cr = 2229
    dt = 1381
    dh = 1662
    spd = 479
    stat = 2575
    wd = 120
    weapon_delay = 3.04

    main = 390
    sub = 400
    div = 1900
    
    pcr,dcr = f.f_crit(cr)
    pdh = f.f_dh(dh)
    
    agent = bard.bard(cr,dh,dt,stat,wd,spd,period,print_log = 1)