# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 14:10:48 2022

@author: atgol
"""
import ffxiv_calculate_damage as f
import numpy as np
import math

class bard():
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
        self.jobmod = 1.2*1.1
        self.weapon_delay = 3.04
        self.left_time = period
        self.elapsed = 0
        
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
        self.stack_army = 0
        
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
        
        if self.buff_battle>0:
            pdh +=0.2
        if self.buff_raging>0:
            buff = buff*1.15
        if self.buff_radient>0:
            buff = buff*(1+self.coda*0.02)
        
        d1 = int(potency * self.atk * self.dt)
        d2 = int(int(d1*int(self.wd))*self.jobmod/100)
        d3 = d2
        
        if np.random.random()<pcr:
            d3 = int(d3 * self.dcr)
        if np.random.random()<pdh:
            d3 = int(d3*1.25)
        
        dmg = f.random_dmg(d3)*buff
        
        return int(dmg)
    
    def calculate_DOT(self,potency):
        d1 = potency*self.atk*f.f_det(self.dt)/100
        d2 = d1 * self.spd*self.wd*self.jobmod
        d3 = int(f.random_dmg(d2))
        
        if np.random.random()<self.pcr:
            d3 = int(d3 * self.dcr)
        if np.random.random()<self.pdh:
            d3 = int(d3*1.25)
        return d3
    
    def auto_shot(self):
        d = f.auto_dmg(self.dex,self.weapon, self.weapon_delay)
        d = int(f.random_dmg(d))
        if np.random.random()<f.pcr:
            d = int(d * self.dcr)
        if np.random.random()<f.pdh:
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
        self.start_storm = self.elapsed
        if self.barrage:
            dmg = 3*dmg
            self.barrage = 0
        return dmg
    
    def causticbite(self):
        dmg = self.calculate_dmg(150)
        self.caustic = 45
        self.ngc = 2
        self.start_caustic = self.elapsed
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
        if (self.raging_cool==0 and self.ngc>0):
            self.raging=20.
            self.raging_cool = 120.
        
    def barrage(self):
        if (self.barrage_cool==0 and self.ngc>0):
            self.buff_barrage = 10.
            self.barrage_cool = 120.
            
    def radient(self):
        if (self.redient_cool==0 and self.ngc>0):
            if (self.army>0 or self.wanderer>0 or self.mage>0):
                self.buff_radient = 15.
                self.radient_cool=120.
                self.coda = 0
                
    def blood(self):
        if (self.available_blood>0 and self.ngc>0): 
            dmg = self.calculate_dmg(110)
            self.available_blood-=1
            self.blood_cool =15.
        return dmg
    
    def empyreal(self):
        if (self.empyreal_cool==0 and self.ngc>0):
            dmg = self.calculate_dmg(220)
            if self.wanderer>0:
                if self.stack_wanderer<3:
                    self.stack_wanderer+=1
            elif self.mage>0:
                if self.available_blood<3:
                    self.available_blood=+1
            elif self.army>0:
                if self.stack_army<4:
                    self.stack_army+=1
        return dmg
    
    def pitch(self):
        if (self.wanderer>0 and self.stack_wanderer>0):
            if self.stack_wanderer==1:
                dmg = self.calculate_dmg(100)
            elif self.stack_wanderer==2:
                dmg = self.calculate_dmg(220)
            elif self.stack_wanderer==3:
                dmg = self.calculate_dmg(360)
            return dmg
        
    def wanderer_minuet(self):
        if self.wanderer_cool==0:
            self.wanderer = 45
            self.stack_coda +=1
            self.wanderer_cool = 120
            dmg = self.calculate_dmg(100)
            self.start_wanderer = self.elapsed
            return dmg
    
    def mage_ballad(self):
        if self.mage_cool ==0:
            self.mage = 30
            self.stack_coda +=1
            self.mage_cool = 120
            dmg = self.calculate_dmg(100)
            self.start_mage = self.elapsed
            return dmg
    
    def army_paeon(self):
        if self.army_cool ==0:
            self.army = 45
            self.stack_coda +=1
            self.mage_cool = 120
            dmg = self.calculate_dmg(100)
            self.start_army = self.elapsed
            return dmg
    
    def tick(self):
        self.elapsed += 0.01
        self.
            
period = 300
#cr = 1945
cr = 2017
#dh = 1594
dt = 1097
#dt = 1146
dh = 1811
spd = 593
stat = 2347
wd = 115
weapon_delay = 3.2

main = 390
sub = 400
div = 1900

pot = 2.2
pcr,dcr = f.f_crit(cr)
pdh = f.f_dh(dh)
gc = f.f_gc(spd)