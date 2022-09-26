# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 22:57:55 2022

@author: atgol
"""

import functions as f
import numpy as np
import pandas as pd
from collections import deque

class character():
    def __init__(self,cr,dh,dt,stat,wd,spd,period,print_log = 0):
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
        self.tick_autoshot = 0
        
        self.print_log = print_log
        self.time_multiply = 100
        self.time_per_tick = 1
        self.tick_per_act = 60
        
        
        self.global_cooldown=0
        self.gc = f.f_gc(spd)*self.time_multiply
        

    def calculate_dmg(self,potency,skill_name):
        buff, pcr, pdh = self.check_buff()
            
        d1 = int(potency * self.atk * self.dt)
        d2 = int(int(d1*int(self.wd))*self.jobmod/100)
        is_crit, is_dh = False, False
        if np.random.random()<pcr:
            d2 = int(d2 * self.dcr)
            is_crit = True
        if np.random.random()<pdh:
            d2 = int(d2*1.25)
            is_dh = True
        
        dmg = f.random_dmg(d2)*buff
        
        if self.print_log:
            print(skill_name, int(dmg), 'Crit:', is_crit, 'DirectHit:', is_dh, 'time: ', round(self.elapsed/self.time_multiply,2))
            
        self.event_log.append((skill_name, 'Direct', int(dmg), is_crit,is_dh, round(self.elapsed/self.time_multiply,3)))
        
        return int(dmg)
    
    def calculate_DOT(self,potency,buff,pcr,pdh,skill_name):
        d1 = potency*self.atk*f.f_det(self.dt)/100
        d2 = d1 * self.spd*self.wd*self.jobmod
        d3 = int(f.random_dmg(d2))
        
        is_crit, is_dh = False, False
        if np.random.random()<pcr:
            d3 = int(d3 * self.dcr)
            is_crit = True
        if np.random.random()<pdh:
            d3 = int(d3*1.25)
            is_dh = True
        dmg = d3 * buff
        
        if self.print_log:
            print('DOT',skill_name,'DOT', int(dmg), 'Crit:', is_crit, 'DirectHit:', is_dh, 'time: ', round(self.elapsed/self.time_multiply,2))
        
        self.event_log.append((skill_name, 'DOT',int(dmg), is_crit,is_dh, round(self.elapsed/self.time_multiply,3)))
        
        return dmg
    
    def auto_shot(self):
        buff, pcr, pdh = self.check_buff()
        d = f.auto_dmg(self.dex,self.weapon, self.weapon_delay)
        d = int(f.random_dmg(d))
        is_crit, is_dh = False, False
        if np.random.random()<pcr:
            d = int(d * self.dcr)
            is_crit = True
        if np.random.random()<pdh:
            d = int(d*1.25)
            is_dh = True
        dmg = d*buff
        
        if self.print_log:
            print('AutoShot', int(dmg), 'Crit:', is_crit, 'DirectHit:', is_dh, 'time: ', round(self.elapsed/self.time_multiply,2))
        
        self.event_log.append(('Autoshot','Auto', int(dmg), is_crit,is_dh, round(self.elapsed/self.time_multiply,3)))
        
        return dmg
    
    def weapon_skill(self, ngc = 2):
        self.ngc = ngc
        self.global_cooldown = self.gc
        self.tick(self.tick_per_act)
        
    def ability(self):
        self.ngc -=1
        self.tick(self.tick_per_act)
        if self.ngc ==0:
            while self.global_cooldown>0:
                self.tick()
                
    def waiting(self,cooldown):
        left_time = self.global_cooldown - self.tick_per_act * self.ngc
        if cooldown < left_time:
            self.tick(cooldown)
        
    def extract_log(self):
        df = pd.DataFrame(self.event_log,columns=['Skill', 'Type','Damage','Crit','Dhit','Time'])
        return df
    
    
class dancer(character):
    def __init__(self,cr,dh,dt,stat,wd,spd,period, print_log =0):
        super().__init__(cr,dh,dt,stat,wd,spd,period,print_log)
        
        self.pcr,self.dcr = f.f_crit(cr)
        self.pdh = f.f_dh(dh)
        self.dt = f.f_det(dt)
        self.dex = stat
        self.weapon = wd
        self.atk = f.f_atk(stat)
        self.wd = f.f_wd(wd)
        self.spd = f.f_spd(spd)
        self.jobmod = 1.2*1.1
        self.weapon_delay = 3.12
        self.left_time = period
        self.elapsed = 0
        self.tick_autoshot = 0
    
        self.buff_devilment = 0
        self.buff_standard = 0
        self.buff_technical = 0
        
        self.ab_silken_symmetry = 0
        self.ab_fourfold_feather = 0
        self.ab_silken_flow = 0
        
        self.espirit = 0
        
        self.print_log = print_log
        self.time_multiply = 100
        self.time_per_tick = 1
        self.tick_per_act = 60
        
        self.gc = f.f_gc(spd)*self.time_multiply
        
    def check_buff(self):
        pcr = self.pcr
        pdh = self.pdh
        buff = 1.
        
        if self.buff_devilment>0:
            pcr +=0.2
            pdh +=0.2
        
        if self.buff_standard>0:
            buff *=1.05
        if self.buff_technical>0:
            buff *=1.05
        
        return buff, pcr, pdh
    
    def cascade(self):
        if self.global_cooldown>0:
            while self.global_cooldown>0:
                self.tick()
                
        dmg = self.calculate_dmg(220, 'Cascade')
        if np.random.random()<0.5:
            self.ab_reverse_cascade = 1
            if self.print_log:
                print('Reverse Cascade Available')
        self.weapon_skill()
        return dmg
        
    def fountain(self):
        if self.global_cooldown>0:
            while self.global_cooldown>0:
                self.tick()
                
        dmg = self.calculate_dmg(280, 'Fountain')
        if np.random.random()<0.5:
            self.ab_fountainfall = 1
            if self.print_log:
                print('Fountainfall Available')
        self.weapon_skill()
        return dmg
    
    def reverse_cascade(self):
        if self.ab_reverse_cascade:
            if self.global_cooldown>0:
                while self.global_cooldown>0:
                    self.tick()
                    
            dmg = self.calculate_dmg(280, 'Reverse Cascade')
            if np.random.random()<0.5:
                self.ab_fourfold_feather += 1
                if self.print_log:
                    print('got Fourfold Feather')
            self.weapon_skill()
            return dmg
        
    def fountainfall(self):
        if self.ab_fountainfall:
            if self.global_cooldown>0:
                while self.global_cooldown>0:
                    self.tick()
                    
            dmg = self.calculate_dmg(340, 'fountainfall')
            if np.random.random()<0.5:
                self.ab_fourfold_feather += 1
                if self.print_log:
                    print('got Fourfold Feather')
            
            self.weapon_skill()
            return dmg
        
    def standard_finish(self):
        
        
    def technical_finish(self):
        
        
    def saber_dance(self):
        
    def tillana(self):
        
    def starfall_dance(self):
    
    def fandance(self):
        if (self.ab_fourfold_feather>0 and self.ngc>0): 
            dmg = self.calculate_dmg(150,'First Fandance')
            self.ab_fourfold_feather-=1
            if np.random.random()<0.5:
                self.ab_third = 1
                if self.print_log:
                    print('Third Fandance Available')
            self.ability()
            return dmg
    
    def fandance_third(self):
        if (self.ab_third>0 and self.ngc>0): 
            dmg = self.calculate_dmg(200,'Third Fandance')
            self.ab_third = 0
            self.ability()
        return dmg
    
    def fandance_fourth(self):
        if (self.ab_fourth>0 and self.ngc>0):
            dmg = self.calculate_dmg(300,'Fourth Fandance')
            self.ab_fourth = 0
            self.ability()
            return dmg