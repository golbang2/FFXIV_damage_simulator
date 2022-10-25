# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 18:51:11 2022

@author: atgol
"""

import range_job as job
import functions as f
import time

def opening(machinist):
    machinist.buff_reassemble = 1 * machinist.time_multiply
    machinist.ab_reassemble = 1
    machinist.cool_reassemble = 51 * machinist.time_multiply
    machinist.air_anchor()
    




if __name__=='__main__':
    #https://etro.gg/gearset/e8c4176b-aad2-4719-9774-36f6d0377624
    period = 300
    cr = 2193
    dt = 1507
    dh = 1662
    spd = 400
    dex = 2574
    wd = 120
    weapon_delay = 2.64

    main = 390
    sub = 400
    div = 1900
    
    pcr,dcr = f.f_crit(cr)
    pdh = f.f_dh(dh)
    
    mach = job.Machinist(cr,dh,dt,dex,wd,spd,period,print_log = 1)