# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 03:06:25 2022

@author: atgol
"""

import ffxiv_calculate_damage as f
import numpy as np

class machinist():
    def __init__(self,gc,cr,dh,dt,stat,wd,spd,period):
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
        
    def calculate_dmg(self,potency):
        buff = 1.
        pcr = self.pcr
        pdh = self.pdh
        
        d1 = int(potency * self.atk * self.dt)
        d2 = int(int(d1*int(self.wd))*self.jobmod/100)
        
        if np.random.random()<pcr:
            d2 = int(d2 * self.dcr)
        if np.random.random()<pdh:
            d2 = int(d2*1.25)
        
        dmg = f.random_dmg(d2)*buff
        
        return int(dmg)
    
    def auto_shot(self):
        d = f.auto_dmg(self.dex,self.weapon, self.weapon_delay)
        d = int(f.random_dmg(d))
        if np.random.random()<f.pcr:
            d = int(d * self.dcr)
        if np.random.random()<f.pdh:
            d = int(d*1.25)
        return d