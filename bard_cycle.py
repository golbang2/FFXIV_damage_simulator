# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 16:26:50 2022

@author: Taeyoon
"""

import bard
import functions as f
import time

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
        ngc_in_wanderer(agent)
        agent.burst_shot()
        agent.barrage()
        agent.burst_shot()
        agent.burst_shot()
        agent.empyreal()
        agent.iron_jaws()
    else:
        agent.barrage()
        ngc_in_wanderer(agent)
        agent.burst_shot()
        agent.sidewinder()
        ngc_in_wanderer(agent)
        agent.burst_shot()
        ngc_in_wanderer(agent)
        ngc_in_wanderer(agent)
        agent.burst_shot()
        ngc_in_wanderer(agent)
        ngc_in_wanderer(agent)
        agent.burst_shot()
        ngc_in_wanderer(agent)
        ngc_in_wanderer(agent)
        agent.empyreal()
        agent.iron_jaws()

def burst(agent):
    gc_in_wanderer(agent)
    agent.wanderer_minuet()
    agent.raging()
    gc_in_wanderer(agent)
    ngc_in_wanderer(agent)
    ngc_in_wanderer(agent)
    gc_in_wanderer(agent)
    agent.radient()
    agent.battle()
    if agent.dot_caustic< 38 * agent.time_multiply:
        agent.iron_jaws()
    else:
        gc_in_wanderer(agent)

def gc_in_wanderer(agent):
    if (agent.dot_caustic < agent.gc_ap or agent.dot_storm< agent.gc_ap):
        agent.iron_jaws()
    elif agent.available_blast:
        agent.blast_arrow()
    elif (agent.buff_raging >0 and agent.buff_radient>0 and agent.buff_battle>0 and agent.soul>80):
        agent.apex_arrow()
    else:
        agent.burst_shot()

def ngc_in_wanderer(agent):
    if agent.stack_wanderer==3:
        agent.pitch()
    elif agent.cool_sidewinder<=0:
        agent.sidewinder()
    elif agent.cool_empyreal<=0:
        agent.empyreal()
    elif agent.available_blood>0:
        agent.blood()
    
    if agent.buff_wanderer< 3 * agent.time_multiply:
        if agent.stack_wanderer>0:
            agent.pitch()
        else:
            agent.mage_ballad()
        
def gc_in_mage(agent):
    if (agent.dot_caustic < agent.gc_ap or agent.dot_storm < agent.gc_ap):
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
    if agent.cool_sidewinder<=0:
        agent.sidewinder()
    elif agent.cool_empyreal<=0:
        agent.empyreal()
    elif agent.available_blood>0:
        agent.blood()
        
    if agent.buff_mage < 15 * agent.time_multiply:
        agent.army_paeon()
        
def gc_in_army(agent):
    if (agent.dot_caustic< agent.gc_ap or agent.dot_storm< agent.gc_ap):
        agent.iron_jaws()
    else:
        agent.burst_shot()
        
def ngc_in_army(agent):
    if (agent.cool_wanderer == 0 and agent.cool_raging == 0):
        agent.wanderer_minuet()
    if (agent.available_blood>2 and agent.cool_blood<agent.gc_ap):
        agent.blood()
    if agent.cool_empyreal<=0:
        agent.empyreal()
        
def GC(agent):
    if agent.buff_wanderer>0:
        gc_in_wanderer(agent)
    elif agent.buff_mage>0:
        gc_in_mage(agent)
    elif agent.buff_army>0:
        gc_in_army(agent)
        
def NGC(agent):
    if agent.buff_wanderer>0:
        ngc_in_wanderer(agent)
    elif agent.buff_mage>0:
        ngc_in_mage(agent)
    elif agent.buff_army>0:
        ngc_in_army(agent)

        
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
    
    agent = bard.Bard(cr,dh,dt,stat,wd,spd,period,print_log = 1)
    
    opening(agent)
    
    
    while not agent.done:
        if agent.cool_wanderer<=0:
            burst(agent)
        if (agent.buff_wanderer ==0 and agent.buff_mage ==0 and agent.buff_army==0):
            if agent.cool_wanderer<agent.gc_ap:
                agent.wanderer_minuet()
            if agent.cool_mage<agent.gc_ap:
                agent.mage_ballad()
            if agent.cool_army<agent.gc_ap:
                agent.army_paeon()

        GC(agent)
        NGC(agent)
        NGC(agent)
    
    act_log = agent.extract_log()