# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 21:56:43 2022

@author: atgol
"""
import numpy as np
import math

class bard():
    def __init__(self,gc,cr,dh,dt,stat,wd,spd,period):
        self.gc = gc
        self.pcr,self.dcr = f_crit(cr)
        self.pdh = f_dh(dh)
        self.dt = f_det(dt)
        self.dex = stat
        self.weapon = wd
        self.atk = f_atk(stat)
        self.wd = f_wd(wd)
        self.spd = f_spd(spd)
        self.jobmod = 1.1*1.2
        self.weapon_delay = 3.04
        self.left_time = period
        
        self.buff_barrage = 0
        self.buff_battle = 0
        self.buff_raging = 0
        self.buff_radient = 0
        
        self.army = 0
        self.mage = 0
        self.wanderer = 0
        
        self.dot_storm = 0
        self.dot_caustic = 0
        
        self.available_straight = 0
        self.available_blast = 0
        self.available_blood = 3
        
        self.stack_coda = 0
        self.stack_wanderer = 0
        self.soul = 0
        self.army_stack = 0
        
    def calculate_dmg(self,potency):
        buff = 1.
        pcr = self.pcr
        pdh = self.pdh
        
        if self.wanderer>0:
            pcr +=0.02
        if self.mage>0:
            buff=buff*1.01
        if self.army>0:
            pdh +=0.03
        
        if self.battle>0:
            pdh +=0.2
        if self.raging>0:
            buff = buff*1.15
        if self.radient>0:
            buff = buff*(1+self.coda*0.02)
        
        d1 = int(potency * self.atk * self.dt)
        d2 = int(int(d1*int(self.wd))*self.jobmod/100)
        d3 = d2
        
        if np.random.random()<pcr:
            d3 = int(d3 * self.dcr)
        if np.random.random()<pdh:
            d3 = int(d3*1.25)
        
        dmg = random_dmg(d3)*buff
        
        return int(dmg)
    
    def calculate_DOT(self,potency):
        d1 = potency*self.atk*f_det(dt)/100
        d2 = d1 * self.spd*self.wd*self.jobmod
        d3 = int(random_dmg(d2))
        
        if np.random.random()<pcr:
            d3 = int(d3 * self.dcr)
        if np.random.random()<pdh:
            d3 = int(d3*1.25)
        return d3
    
    def auto_shot(self):
        d = auto_dmg(self.dex,self.weapon, self.weapon_delay)
        d = int(random_dmg(d))
        if np.random.random()<pcr:
            d = int(d * self.dcr)
        if np.random.random()<pdh:
            d = int(d*1.25)
        return d
    
    def burst_shot(self):
        dmg = self.calculate_dmg(220)
        if self.straight:
            dmg = self.calculate_dmg(280)
        self.ngc = 2
        if self.barrage:
            dmg = 3*dmg
            self.barrage = 0
        return dmg
    
    def stormbite(self):
        dmg = self.calculate_dmg(100)
        self.storm = 45
        self.ngc = 2
        if self.barrage:
            dmg = 3*dmg
            self.barrage = 0
        return dmg
    
    def causticbite(self):
        dmg = self.calculate_dmg(150)
        self.caustic = 45
        self.ngc = 2
        if self.barrage:
            dmg = 3*dmg
            self.barrage = 0
        return dmg
    
    def iron_jaws(self):
        dmg = self.calculate_dmg(100)
        self.caustic = 45
        self.storm = 45
        self.ngc = 2
        if self.barrage:
            dmg = 3*dmg
            self.barrage = 0
        return dmg
    
    def raging(self):
        self.raging=20.
        self.raging_cool = 120.
    
    def barrage(self):
        self.buff_barrage = 10.
        self.barrage_cool = 120.
    def radient(self):
        if (self.army>0 or self.wanderer>0 or self.mage>0):
            self.buff_radient = 15.
            self.radient_cool=120.
            self.coda = 0
        

def f_crit(cr, sub=400, div = 1900):
    p_cr= int(200*(cr - sub)/div+50)
    d_cr = int(1400+(200*(cr-sub)/div))
    return p_cr/1000,d_cr/1000

def f_dh(dh, sub=400, div =1900):
    p_dh = int(550*(dh-sub)/div)
    return p_dh/1000
    
def f_det(dt, main=390, div = 1900):
    d_dt = int(1000+(140*(dt-main)/div))
    return d_dt/1000

def f_wd(wd,jobmod= 115,main = 390):
    return int(main*jobmod/1000+wd)

def f_atk(stat):
    return (125*(stat-292)/292+100)/100

def exp_dmg(prob,mod=1.25):
    return (1-prob)*1+prob*mod

def random_dmg(dmg):
    return (0.1*np.random.random()+0.95)*dmg

def f_spd(sp, sub = 400, div = 1900):
    return int(130*(sp-sub)/div+1000)/1000
    
def auto_dmg(stat,weapon,delay,main=390,job=115):
    atk = (100+int(165*(stat-390)/390))/100
    auto = int(int(390*115/1000)+weapon*delay/3)
    return int(atk*auto)


period = 300
gc = 2.47
cr = 1945
dh = 1594
dt = 1146
spd = 593
stat = 2347
wd = 115
weapon_delay = 3.04

main = 390
sub = 400
div = 1900

pot = 2.2
pcr,dcr = f_crit(cr)
pdh = f_dh(dh)

