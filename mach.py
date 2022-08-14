# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 03:06:25 2022

@author: atgol
"""

import ffxiv_calculate_damage as f
import numpy as np

class machinist():
    def __init__(self,gc,cr,dh,dt,stat,wd,spd,period=360.):
        self.gc = gc
        self.pcr,self.dcr = f.f_crit(cr)
        self.pdh = f.f_dh(dh)
        self.dt = f.f_det(dt)
        self.dex = stat
        self.weapon = wd
        self.atk = f.f_atk(stat)
        self.wd = f.f_wd(wd)
        self.spd = f.f_spd(spd)
        self.jobmod = 1.1*1.2
        self.weapon_delay = 2.64
        self.left_time = period
        
        self.buff_reassemble = 0
        self.buff_wildfire = 0
        
        self.heat = 0
        self.battery = 0 
        
    def calculate_dmg(self,potency,buff=1.,reassemble = 0):
        pcr = self.pcr
        pdh = self.pdh
        is_cr = 0
        is_dh = 0
        d1 = int(potency * self.atk * self.dt)
        d2 = int(int(d1*int(self.wd))*self.jobmod/100)
        
        if reassemble == 0:
            if np.random.random()<pcr:
                d2 = int(d2 * self.dcr)
                is_cr = 1
            if np.random.random()<pdh:
                d2 = int(d2*1.25)
                is_dh = 1
                
        elif reassemble == 1:
            d2 = int(d2 * self.dcr)
            d2 = int(d2*1.25)
            is_cr = 1
            is_dh =1
            
        dmg = f.random_dmg(d2)*buff
        
        return int(dmg), is_cr,is_dh
    
    def auto_shot(self):
        d = f.auto_dmg(self.dex,self.weapon, self.weapon_delay)
        d = int(f.random_dmg(d))
        is_cr = 0
        is_dh = 0
        if np.random.random()<f.pcr:
            d = int(d * self.dcr)
            is_cr = 1
        if np.random.random()<f.pdh:
            d = int(d*1.25)
            is_dh = 1
        return d,is_cr,is_dh
    