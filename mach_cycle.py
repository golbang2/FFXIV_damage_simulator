# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 18:51:11 2022

@author: atgol
"""

import range_job as job
import functions as f
import time

def opening(machinist):
    machinist.buff_reassemble = 1
    machinist.ab_reassemble = 1
    machinist.air_anchor()