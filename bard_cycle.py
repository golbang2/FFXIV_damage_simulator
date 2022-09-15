# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 16:26:50 2022

@author: Taeyoon
"""

import bard

def opening(class_bard):
    class_bard.stormbite()
    class_bard.wanderer_minuet()
    class_bard.raging()
    class_bard.causticbite()
    class_bard.empyreal()
    class_bard.blood()
    class_bard.burst_shot()
    class_bard.radient()
    class_bard.battle_voice()
    class_bard.burst_shot()
    if class_bard.straight:
        class_bard.sidewinder()
        class_bard.burst_shot()
        class_bard.barrage()
        class_bard.burst_shot()
        class_bard.burst_shot()
        class_bard.empyreal()
        class_bard.iron_jaws()
    else:
        class_bard.barrage()
        class_bard.burst_show()
        class_bard.sidewinder()
        class_bard.burst_show()
        class_bard.burst_show()
        class_bard.burst_show()
        class_bard.empyreal()
        class_bard.iron_jaws()

def cycle_in_minuet(class_bard):
    if class_bard.stack_wanderer==3:
        class_bard.pitch()
    elif 