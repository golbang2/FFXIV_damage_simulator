# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 14:10:48 2022

@author: atgol
"""
import ffxiv_calculate_damage as f
import numpy as np

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
        self.dotbuff_storm_mod = 1.
        self.dotbuff_storm_dhmod = 0.
        self.dotbuff_storm_crmod = 0.
        
        self.dot_caustic = 0
        self.dotbuff_caustic_mod = 1.
        self.dotbuff_caustic_dhmod = 0.
        self.dotbuff_caustic_crmod = 0.
        
        self.available_straight = 0
        self.available_blast = 0
        self.available_blood = 3
        
        self.stack_coda = 0
        self.stack_wanderer = 0
        self.soul = 0
        self.stack_army = 0
        
        self.calculate_gc(0)
        self.initialize_cooldown()
        
        self.global_cooldown=0
        
    def initialize_cooldown(self):
        self.cool_wanderer = 0
        self.cool_mage = 0
        self.cool_army = 0
        self.cool_raging = 0
        self.cool_radient = 0
        self.cool_barrage = 0
        self.cool_battle = 0
        self.cool_blood = 0 
        self.cool_empyreal = 0
    
    def buff(self):
        print(self.buff_barrage)
        print(self.buff_battle)
        print(self.buff_raging)
        print(self.buff_radient)
        print(self.wanderer)
        print(self.mage)
        print(self.army)
        
    def cooldown(self):
        print(self.cool_army)
        print(self.cool_barrage)
        print(self.cool_battle)
        print(self.cool_blood)
        print(self.cool_empyreal)
        print(self.cool_mage)
        print(self.cool_radient)
        print(self.cool_raging)
        print(self.cool_wanderer)
        
    def check_buff(self):
        pcr = self.pcr
        pdh = self.pdh
        buff = 1.
        if self.wanderer>0:
            pcr +=0.02
        if self.mage>0:
            buff *=1.01
        if self.army>0:
            pdh +=0.03
        
        if self.buff_battle>0:
            pdh+=0.2
        if self.buff_raging>0:
            buff *=1.15
        if self.buff_radient>0:
            buff *=(1+self.radient_coda*2)
            
        return buff, pcr, pdh
        
    def calculate_dmg(self,potency):
        buff, pcr, pdh = self.check_buff()
            
        d1 = int(potency * self.atk * self.dt)
        d2 = int(int(d1*int(self.wd))*self.jobmod/100)
        d3 = d2
        
        if np.random.random()<pcr:
            d3 = int(d3 * self.dcr)
            print('Critical!')
        if np.random.random()<pdh:
            d3 = int(d3*1.25)
            print('Direct Hit!')
        
        dmg = f.random_dmg(d3)*buff
        
        return int(dmg)
    
    def calculate_DOT(self,potency,buff,pcr,pdh):
        d1 = potency*self.atk*f.f_det(self.dt)/100
        d2 = d1 * self.spd*self.wd*self.jobmod
        d3 = int(f.random_dmg(d2))
        
        if np.random.random()<pcr:
            d3 = int(d3 * self.dcr)
            print('Critical!')
        if np.random.random()<pdh:
            d3 = int(d3*1.25)
            print('Direct Hit!')
        d3 = d3 * buff
        
        return d3
    
    def auto_shot(self):
        buff, pcr, pdh = self.check_buff()
        d = f.auto_dmg(self.dex,self.weapon, self.weapon_delay)
        d = int(f.random_dmg(d))
        if np.random.random()<pcr:
            d = int(d * self.dcr)
        if np.random.random()<pdh:
            d = int(d*1.25)
        d = d*buff
        return d
    
    def burst_shot(self):
        if self.global_cooldown<=0:
            dmg = self.calculate_dmg(220)
            if self.straight:
                if self.barrage>0:
                    dmg = self.calculate_dmg(280)+self.calculate_dmg(280)+self.calculate_dmg(280)
                    self.barrage = 0
                else:
                    dmg = self.calculate_dmg(280)
            else:
                if np.random.random()<0.8:
                    self.straight = 1
            
            self.weapon_skill()
            
            return dmg
        
    def apex_arrow(self):
        if self.global_cooldown<=0:
            if self.soul>20:
                dmg = self.calculate_dmg(self.soul*5)
                self.weapon_skill()
                if self.soul>80:
                    self.available_blast=1
                return dmg
        
    def blast_arrow(self):
        if self.global_cooldown<=0:
            if self.available_blast:
                dmg = self.calculate_dmg(600)
                self.weapon_skill()
                return dmg
        
    def stormbite(self):
        if self.global_cooldown<=0:
            dmg = self.calculate_dmg(100)
            self.dot_storm = 45.
            self.weapon_skill()
            self.dot_storm_tick = 3.
            
            self.dotbuff_storm_mod, self.dotbuff_storm_crmod, self.dotbuff_storm_dhmod = self.check_buff()
            
            if np.random.random()<0.8:
                self.straight = 1
            
            return dmg
        
    def causticbite(self):
        if self.global_cooldown<=0:
            dmg = self.calculate_dmg(150)
            self.dot_caustic = 45.
            self.weapon_skill()
            self.dot_caustic_tick = 3.
            
            self.dotbuff_caustic_mod, self.dotbuff_caustic_crmod, self.dotbuff_caustic_dhmod = self.check_buff()
            
            if np.random.random()<0.8:
                self.straight = 1
            
            return dmg
        
    def iron_jaws(self):
        if self.global_cooldown<=0:
            dmg = self.calculate_dmg(100)
            self.caustic = 45
            self.storm = 45
            self.weapon_skill()
            self.start_caustic = self.elapsed
            self.start_storm = self.elapsed
            
            self.dotbuff_storm_mod, self.dotbuff_storm_crmod, self.dotbuff_storm_dhmod = self.check_buff()
            self.dotbuff_caustic_mod, self.dotbuff_caustic_crmod, self.dotbuff_caustic_dhmod = self.check_buff()
            
            if np.random.random()<0.8:
                self.straight = 1
            
            return dmg
        
    def raging(self):
        if (self.cool_raging<self.gc_ap and self.ngc>0):
            self.buff_raging=20.
            self.cool_raging = 120.
            self.ability()
            
    def battle_voice(self):
        if (self.cool_battle<self.gc_ap and self.ngc>0):
            self.buff_battle = 15
            self.cool_battle = 120
            self.ability()
        
    def barrage(self):
        if (self.cool_barrage<self.gc_ap and self.ngc>0):
            self.buff_barrage = 10.
            self.cool_barrage = 120.
            self.straight = 1
            self.ability()
            
    def radient(self):
        if (self.cool_radient<self.gc_ap and self.ngc>0):
            if (self.army>0 or self.wanderer>0 or self.mage>0):
                self.buff_radient = 15.
                self.cool_radient = 110.
                self.radient_coda = self.coda
                self.coda = 0
                self.ability()
                
    def blood(self):
        if (self.available_blood>0 and self.ngc>0): 
            dmg = self.calculate_dmg(110)
            self.available_blood-=1
            self.cool_blood =15.
            self.ability()
        return dmg
    
    def empyreal(self):
        if (self.cool_empyreal<self.gc_ap and self.ngc>0):
            dmg = self.calculate_dmg(220)
            self.song_effect()
            self.ability()
        return dmg
    
    def pitch(self):
        if (self.wanderer>0 and self.stack_wanderer>0):
            if self.stack_wanderer==1:
                dmg = self.calculate_dmg(100)
            elif self.stack_wanderer==2:
                dmg = self.calculate_dmg(220)
            elif self.stack_wanderer==3:
                dmg = self.calculate_dmg(360)
            self.ability()
            return dmg
        
    def wanderer_minuet(self):
        if self.cool_wanderer<self.gc_ap:
            self.wanderer = 45
            self.stack_coda +=1
            self.cool_wanderer = 120
            dmg = self.calculate_dmg(100)
            self.tick_song = 3.
            self.calculate_gc(0)
            
            self.mage = 0
            self.army = 0 
            
            self.ability()
            return dmg
    
    def mage_ballad(self):
        if self.cool_mage <self.gc_ap:
            self.mage = 30
            self.stack_coda +=1
            self.cool_mage = 120
            dmg = self.calculate_dmg(100)
            self.tick_song = 3.
            self.calculate_gc(0)
            
            self.wanderer = 0
            self.army = 0
            
            self.ability()
            return dmg
    
    def army_paeon(self):
        if self.cool_army <self.gc_ap:
            self.army = 45
            self.stack_coda +=1
            self.cool_mage = 120
            dmg = self.calculate_dmg(100)
            self.tick_song = 3.
            self.calculate_gc(0)
            
            self.wanderer = 0
            self.mage = 0
            
            self.ability()
            return dmg
    
    def tick(self,iteration=1):
        for i in range(iteration):
            self.elapsed += 0.01
            
            if self.wanderer>0:
                self.wanderer-=0.01
            elif self.mage>0:
                self.mage-=0.01
            elif self.army>0:
                self.army-=0.01
                
            self.dot_caustic-=0.01
            self.dot_storm-=0.01
            
            self.cool_army -= 0.01
            self.cool_barrage -= 0.01
            self.cool_battle -= 0.01
            self.cool_blood -= 0.01
            self.cool_mage -= 0.01
            self.cool_radient -= 0.01
            self.cool_raging -= 0.01
            self.cool_wanderer -= 0.01
            self.cool_empyreal -= 0.01
            
            self.buff_battle -= 0.01
            self.buff_radient -= 0.01
            self.buff_raging -= 0.01
            self.buff_barrage -= 0.01
            
            self.global_cooldown -= 0.01
                
            if self.tick_song<0.001:
                self.effect_over_tick(self.elapsed)
                self.tick_song = 3.
                
            if self.dot_caustic_tick<0.001:
                self.calculate_DOT(20,self.dotbuff_caustic_mod, self.dotbuff_caustic_dhmod, self.dotbuff_caustic_crmod)
                self.dot_caustic_tick = 3.
            if self.dot_storm_tick<0.001:
                self.calculate_DOT(25,self.dotbuff_storm_mod, self.dotbuff_storm_dhmod, self.dotbuff_storm_crmod)
                self.dot_storm_tick = 3.    
            
            if self.elapsed > self.left_time:
                self.done=1
            
    def effect_over_tick(self,elapsed):
        if np.random.random()<0.8:
            self.song_effect()
            
        
    def calculate_gc(self,stack_army):
        self.gc_ap = self.gc*(1-stack_army*0.04)
        
    def song_effect(self):
        if self.wanderer>0:
            if self.stack_wanderer<3:
                self.stack_wanderer+=1
                
        elif self.mage>0:
            self.cool_blood-=7.5

        elif self.army>0:
            if self.stack_army<4:
                self.stack_army+=1
                self.calculate_gc(self.stack_army)
                
        if self.soul<100:
            self.soul+=5
    
    def weapon_skill(self):
        self.ngc = 2
        self.global_cooldown = self.gc_ap
        self.last_act = self.elapsed
        
    def ability(self):
        self.ngc -=1
        self.tick(100)
        if self.ngc ==0:
            while self.global_cooldown>0:
                self.tick()
        

if __name__=='__main__':
    #https://etro.gg/gearset/cec981af-25c7-4ffb-905e-3024411b797a
    period = 300
    cr = 2229
    dt = 1381
    dh = 1662
    spd = 479
    stat = 2575
    wd = 120
    weapon_delay = 3.04

    main = 390
    sub = 400
    div = 1900
    
    pcr,dcr = f.f_crit(cr)
    pdh = f.f_dh(dh)
    gc = f.f_gc(spd)
    
    agent = bard(gc,cr,dh,dt,stat,wd,spd,period)