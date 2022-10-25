# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 20:36:30 2022

@author: atgol
"""

import range_job as job
import functions as f
import time


if __name__=='__main__':
    #https://etro.gg/gearset/fd333e44-0f90-42a6-a070-044b332bb54e
    period = 300
    cr = 2283
    dt = 1453
    dh = 1477
    spd = 549
    dex = 2574
    wd = 120
    weapon_delay = 3.12

    main = 390
    sub = 400
    div = 1900
    
    pcr,dcr = f.f_crit(cr)
    pdh = f.f_dh(dh)
    
    dancer = job.Dancer(cr,dh,dt,dex,wd,spd,period,print_log = 1)