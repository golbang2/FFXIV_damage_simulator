# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 16:26:50 2022

@author: Taeyoon
"""

import bard as job

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
    if agent.straight:
        agent.sidewinder()
        agent.burst_shot()
        agent.barrage()
        agent.burst_shot()
        agent.burst_shot()
        agent.empyreal()
        agent.iron_jaws()
    else:
        agent.barrage()
        agent.burst_show()
        agent.sidewinder()
        agent.burst_show()
        agent.burst_show()
        agent.burst_show()
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
    if (agent.dot_caustic<3 or agent.dot_storm<3):
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
    elif agent.cool_sidewinder<0:
        agent.sidewinder()
    elif agent.cool_empyreal<0:
        agent.empyreal()
    elif agent.available_blood>0:
        agent.blood()
    
    if agent.wanderer<3:
        agent.mage_ballad()
        
def gc_in_mage(agent):
    if (agent.dot_caustic<3 or agent.dot_storm<3):
        agent.iron_jaws()
    elif agent.soul>80:
        agent.apex_arrow()
    elif agent.available_blast:
        agent.blast_arrow()
    elif (agent.buff_raging >0 and agent.buff_radient>0 and agent.buff_battle>0 and agent.soul>80):
        agent.apex_arrow()
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

def gc_in_army(agent):
    if (agent.dot_caustic<3 or agent.dot_storm<3):
        agent.iron_jaws()
    else:
        agent.burst_shot()