# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 16:26:50 2022

@author: Taeyoon
"""

import bard as job

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
    if bard.straight:
        bard.sidewinder()
        bard.burst_shot()
        bard.barrage()
        bard.burst_shot()
        bard.burst_shot()
        bard.empyreal()
        bard.iron_jaws()
    else:
        bard.barrage()
        bard.burst_show()
        bard.sidewinder()
        bard.burst_show()
        bard.burst_show()
        bard.burst_show()
        bard.empyreal()
        bard.iron_jaws()

def burst(bard):
    gc_in_minuet(bard)
    bard.wanderer_minuet()
    bard.raging()
    gc_in_minuet(bard)
    ngc_in_minuet(bard)
    ngc_in_minuet(bard)
    gc_in_minuet(bard,apex=1)
    bard.radient()
    bard.battle()

def gc_in_minuet(bard,apex=0):
    if (bard.dot_caustic<3 or bard.dot_storm<3):
        bard.iron_jaws()
    elif bard.available_blast:
        bard.blast_arrow()
    elif (bard.buff_raging >0 and bard.buff_radient>0 and bard.buff_battle>0 and bard.soul>80 and apex==1):
        bard.apex_arrow()

def ngc_in_minuet(bard):
    if bard.stack_wanderer==3:
        bard.pitch()
    elif bard.cool_sidewinder<0:
        bard.sidewinder()
    elif bard.cool_empyreal<0:
        bard.empyreal()
    elif bard.available_blood>0:
        bard.blood()