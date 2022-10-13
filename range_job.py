# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 22:57:55 2022

@author: atgol
"""

import functions as f
import numpy as np
import pandas as pd
from collections import deque

class Character():
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

    def calculate_dmg(self,potency,skill_name , fix_cr = 0 , fix_dh = 0):
        buff, pcr, pdh = self.check_buff()
            
        d1 = int(potency * self.atk * self.dt)
        d2 = int(int(d1*int(self.wd))*self.jobmod/100)
        is_crit, is_dh = False, False
        if (np.random.random()<pcr or fix_cr):
            d2 = int(d2 * self.dcr)
            is_crit = True
        if (np.random.random()<pdh or fix_dh):
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
    
class Dancer(Character):
    def __init__(self,cr,dh,dt,stat,wd,spd,period, print_log =0, opening = -15):
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
        self.elapsed = opening
        self.tick_autoshot = 0
    
        self.buff_ = 0
        self.buff_standard = 0
        self.buff_technical = 0
        
        self.ab_silken_symmetry = 0
        self.ab_fourfold_feather = 0
        self.ab_silken_flow = 0
        
        self.esprit = 0
        
        self.print_log = print_log
        self.time_multiply = 100
        self.time_per_tick = 1
        self.tick_per_act = 60
        
        self.gc = f.f_gc(spd)*self.time_multiply
        self.tick_esprit = self.gc
        
        
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
        self.esprit +=5
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
        self.esprit +=5
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
            self.esprit +=10
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
                    
            self.esprit +=10
            self.weapon_skill()
            return dmg
        
    def standard_finish(self):
        if self.cool_standard<=0:
            if self.global_cooldown>0:
                while self.global_cooldown>0:
                    self.tick()
        
            self.cool_standard = 30* self.time_multiply
            self.tick((1.5+1*2)*self.time_multiply)
            self.buff_standard = 60 * self.time_multiply
            self.global_cooldown = 1.5 * self.time_multiply
            dmg = self.calculate_dmg(720, 'Standard Finish')
            self.ngc = 1
            return dmg
            
    def opening_standard_finish(self):
            if self.global_cooldown>0:
                while self.global_cooldown>0:
                    self.tick()
            
            self.cool_standard = 30* self.time_multiply
            self.tick(15*self.time_multiply)
            self.buff_standard = 60 * self.time_multiply
            self.global_cooldown = 1.5 * self.time_multiply
            dmg = self.calculate_dmg(720, 'Standard Finish')
            self.ngc = 1
            return dmg
            
    def technical_finish(self):
        if self.cool_technical<=0:
            if self.global_cooldown>0:
                while self.global_cooldown>0:
                    self.tick()
            self.cool_technical = 120 * self.time_multiply
            self.tick((1.5+1*4)*self.time_multiply)
            self.buff_technical = 15 * self.time_multiply
            self.ngc = 1
            self.global_cooldown = 1.5 * self.time_multiply
            dmg = self.calculate_dmg(1200,'Technical Finish')
            self.ab_tillana = 1
            return dmg
        
    def saber_dance(self):
        if self.esprit >= 50:
            if self.global_cooldown>0:
                while self.global_cooldown>0:
                    self.tick()
            self.esprit -=50
            dmg = self.calculate_dmg(480, 'Saber Dance')
            self.weapon_skill()
            return dmg
            
    def tillana(self):
        if self.ab_tillana:
            if self.global_cooldown>0:
                while self.global_cooldown>0:
                    self.tick()
            self.ngc = 1
            self.global_cooldown = 1.5 * self.time_multiply
            self.buff_standard = 60 * self.time_multiply
            dmg = self.calculate_dmg(360)
            self.ab_tillana = 0
            return dmg
        
    def starfall_dance(self):
        if self.ab_starfall:
            if self.global_cooldown>0:
                while self.global_cooldown>0:
                    self.tick()
                    
            self.ab_starfall = 0
            dmg = self.calculate_dmg(600,'Starfall Dance',1,1)
            self.weapon_skill()
            return dmg
    
    def flourish(self):
        if (self.cool_flourish<=0 and self.ngc>0):
            self.ab_fountainfall = 1
            self.ab_reverse_cascade = 1
            self.ab_third = 1
            self.ab_fourth = 1
            self.cool_flourish = 60 * self.time_multiply
            self.ability()
    
    def devilment(self):
        if (self.cool_devilment<=0 and self.ngc>0):
            self.buff_devilment = 20 * self.time_multiply
            self.cool_devilment = 120 * self.time_multiply
            self.ab_starfall = 1
    
    def fandance(self):
        if (self.ab_fourfold_feather>0 and self.ngc>0): 
            dmg = self.calculate_dmg(150,'First FanDance')
            self.ab_fourfold_feather-=1
            if np.random.random()<0.5:
                self.ab_third = 1
                if self.print_log:
                    print('Third Fandance Available')
            self.ability()
            return dmg
    
    def fandance_third(self):
        if (self.ab_third>0 and self.ngc>0): 
            dmg = self.calculate_dmg(200,'Third FanDance')
            self.ab_third = 0
            self.ability()
            return dmg
    
    def fandance_fourth(self):
        if (self.ab_fourth>0 and self.ngc>0):
            dmg = self.calculate_dmg(300,'Fourth FanDance')
            self.ab_fourth = 0
            self.ability()
            return dmg
        
        def tick(self,iteration=1):
            for i in range(iteration):
                self.elapsed += self.time_per_tick
                    
                self.tick_autoshot-=self.time_per_tick
                
                self.cool_devilment -= self.time_per_tick
                self.cool_flourish -= self.time_per_tick
                self.cool_standard -= self.time_per_tick
                self.cool_technical -= self.time_per_tick
                
                self.buff_devilment -= self.time_per_tick
                self.buff_standard -= self.time_per_tick
                self.buff_technical -= self.time_per_tick
                
                self.global_cooldown -= self.time_per_tick
                
                if self.tick_esprit <=0:
                    self.tick_esprit = self.gc
                    self.esprit += 2.5
                
                if self.tick_autoshot<0.001:
                    self.tick_autoshot = 3* self.time_multiply
                    self.auto_shot()
                    
                if self.elapsed > self.left_time:
                    self.done=1
                    
class Machinist(Character):
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
    
    def initialize_cooldown(self):
        self.cool_drill = 0
        self.cool_airanchor = 0
        self.cool_chainsaw = 0
        self.cool_reassemble = 0
        self.cool_gaussround = 0
        self.cool_wildfire = 0
        self.cool_ricochet = 0
        self.cool_barrelstabilizer = 0
        
        '''
            if skill_name=='Drill':
                potency_list.append(570)
                gc_list.append(self.gc)
            elif skill_name=='Air Anchor':
                potency_list.append(570)
                gc_list.append(self.gc)
            elif skill_name=='Chain Saw':
                potency_list.append(570)
                gc_list.append(self.gc)
            elif skill_name== 'Heated Split Shot':
                potency_list.append(380)
                gc_list.append(self.gc)
            elif skill_name=='Heated Slug Shot':
                potency_list.append(380)
                gc_list.append(self.gc)
            elif skill_name=='Heated Clean Shot':
                potency_list.append(460)
                gc_list.append(self.gc)
            elif skill_name=='Heat Blast':
                potency_list.append(170)
                gc_list.append(1.5)
            elif skill_name=='Gauss Round':
                potency_list.append(120)
                gc_list.append(0)
            elif skill_name=='Ricochet':
                potency_list.append(120)
                gc_list.append(0)
            elif skill_name=='Arm Punch':
                potency_list.append(120)
                gc_list.append(0)
            elif skill_name=='Pile Bunker':
                potency_list.append(650)
                gc_list.append(0)
            elif skill_name=='Crowned Collider':
                potency_list.append(750)
                gc_list.append(0)
            elif skill_name=='Shot':
                potency_list.append(100)
                gc_list.append(0)
                '''
        
if __name__=='__main__':
    #https://etro.gg/gearset/cec981af-25c7-4ffb-905e-3024411b797a
    period = 300
    cr = 2193
    dt = 1507
    dh = 1626
    spd = 436
    dex = 2575
    wd = 120
    weapon_delay = 3.12

    main = 390
    sub = 400
    div = 1900
    
    pcr,dcr = f.f_crit(cr)
    pdh = f.f_dh(dh)
    
    agent = dancer(cr,dh,dt,dex,wd,spd,period,print_log = 1)