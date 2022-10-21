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
    
class Bard():
    def __init__(self,cr,dh,dt,stat,wd,spd,period, print_log =0):
        #super().__init__(cr,dh,dt,stat,wd,spd,period,print_log)
        
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
        
        self.initialize_buff()
        self.initialize_dot()
        self.initialize_skill()
        
        self.global_cooldown=0
        
        self.print_log = print_log
        self.time_multiply = 100
        self.time_per_tick = 1
        self.tick_per_act = 60
        
        self.event_log = deque()
        
        self.gc = f.f_gc(spd)*self.time_multiply
        self.calculate_gc(0)
        
        self.done =0
        
    def initialize_skill(self):
        self.cool_wanderer = 0
        self.cool_mage = 0
        self.cool_army = 0
        self.cool_raging = 0
        self.cool_radient = 0
        self.cool_barrage = 0
        self.cool_battle = 0
        self.cool_blood = 0 
        self.cool_empyreal = 0
        self.cool_sidewinder = 0
        
        self.available_straight = 0
        self.available_blast = 0
        self.available_blood = 3
        
        self.stack_coda = 0
        self.stack_wanderer = 0
        self.soul = 0
        self.stack_army = 0
    
    def initialize_buff(self):
        self.buff_barrage = 0
        self.buff_battle = 0
        self.buff_raging = 0
        self.buff_radient = 0
        
        self.buff_army = 0
        self.buff_mage = 0
        self.buff_wanderer = 0
        
    def initialize_dot(self):
        self.dot_storm = 0
        self.dotbuff_storm_mod = 1.
        self.dotbuff_storm_dhmod = 0.
        self.dotbuff_storm_crmod = 0.
        
        self.dot_caustic = 0
        self.dotbuff_caustic_mod = 1.
        self.dotbuff_caustic_dhmod = 0.
        self.dotbuff_caustic_crmod = 0.
    
    
    def buff(self):
        print('barrage:',self.buff_barrage*0.01)
        print('battle voice:',self.buff_battle*0.01)
        print('raging strikes:',self.buff_raging*0.01)
        print('radient finale:',self.buff_radient*0.01)
        print('wanderer minuet:', self.buff_wanderer*0.01)
        print('mage ballad:',self.buff_mage*0.01)
        print('army paeon:',self.buff_army*0.01)
        
    def cooldown(self):
        print('Raging strikes', self.cool_raging*0.01)
        print('Radient Finale',self.cool_radient*0.01)
        print('Battle voice',self.cool_battle*0.01)
        print('Barrage',self.cool_barrage*0.01)
        print('Sidewinder', self.cool_sidewinder*0.01)
        print('Bloodletter',self.cool_blood*0.01,', stack: ',self.available_blood)
        print('Empyreal Arrow',self.cool_empyreal*0.01)
        print('Wanderer minuet', self.cool_wanderer*0.01)
        print('Mage ballad',self.cool_mage*0.01)
        print('Army paeon',self.cool_army*0.01)
        
    def check_buff(self):
        pcr = self.pcr
        pdh = self.pdh
        buff = 1.
        if self.buff_wanderer>0:
            pcr +=0.02
        if self.buff_mage>0:
            buff *=1.01
        if self.buff_army>0:
            pdh +=0.03
        
        if self.buff_battle>0:
            pdh+=0.2
        if self.buff_raging>0:
            buff *=115 *0.01
        if self.buff_radient>0:
            buff *=(100+self.radient_coda*2) * 0.01
        return buff, pcr, pdh
        
    def calculate_dmg(self,potency,skill_name):
        buff, pcr, pdh = self.check_buff()
            
        d1 = int(potency * self.atk * self.dt)
        d2 = int(int(d1*int(self.wd))*self.jobmod*0.01)
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
        d1 = potency*self.atk*f.f_det(self.dt)*0.01
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
    
    def burst_shot(self):
        if self.global_cooldown>0:
            while self.global_cooldown>0:
                self.tick()
            
        if self.available_straight:
            self.available_straight = 0
            if self.buff_barrage>0:
                dmg = self.calculate_dmg(280,'Refulgent Arrow')+self.calculate_dmg(280,'Refulgent Arrow')+self.calculate_dmg(280,'Refulgent Arrow')
                self.buff_barrage = 0
            else:
                dmg = self.calculate_dmg(280,'Refulgent Arrow')
                
        else:
            dmg = self.calculate_dmg(220, 'Burst Shot')
            if np.random.random()<0.35:
                self.available_straight = 1
                if self.print_log:
                    print('Refulgent Arrow Available')
        
        self.weapon_skill()
        
        return dmg
        
    def apex_arrow(self):
        if self.global_cooldown>0:
            while self.global_cooldown>0:
                self.tick()
        if self.soul>20:
            dmg = self.calculate_dmg(self.soul*5,'Apex Arrow')
            self.soul = 0
            self.weapon_skill()
            if self.soul>80:
                self.available_blast=1
            return dmg
        
    def blast_arrow(self):
        if self.global_cooldown>0:
            while self.global_cooldown>0:
                self.tick()
        if self.available_blast:
            dmg = self.calculate_dmg(600,'Blast Arrow')
            self.weapon_skill()
            return dmg
        
    def stormbite(self):
        if self.global_cooldown>0:
            while self.global_cooldown>0:
                self.tick()
        dmg = self.calculate_dmg(100,'Stormbite')
        self.dot_storm = 45* self.time_multiply
        
        self.tick_dot_storm = 3* self.time_multiply
        
        self.dotbuff_storm_mod, self.dotbuff_storm_crmod, self.dotbuff_storm_dhmod = self.check_buff()
        
        if np.random.random()<0.35:
            self.available_straight = 1
            if self.print_log:
                print('Refulgent Arrow Available')
    
        self.weapon_skill()
        return dmg
        
    def causticbite(self):
        if self.global_cooldown>0:
            while self.global_cooldown>0:
                self.tick()
        dmg = self.calculate_dmg(150,'Causticbite')
        self.dot_caustic = 45 * self.time_multiply
        self.tick_dot_caustic = 3 * self.time_multiply
        self.dotbuff_caustic_mod, self.dotbuff_caustic_crmod, self.dotbuff_caustic_dhmod = self.check_buff()
        
        if np.random.random()<0.35:
            self.available_straight = 1
            if self.print_log:
                print('Refulgent Arrow Available')
    
        self.weapon_skill()
        return dmg
        
    def iron_jaws(self):
        if self.global_cooldown>0:
            while self.global_cooldown>0:
                self.tick()
        dmg = self.calculate_dmg(100,'Iron Jaws')
        self.dot_caustic = 45* self.time_multiply
        self.tick_dot_caustic = 3 * self.time_multiply
        self.dot_storm = 45* self.time_multiply
        self.tick_dot_storm = 3* self.time_multiply
        
        self.start_caustic = self.elapsed
        self.start_storm = self.elapsed
        
        self.dotbuff_storm_mod, self.dotbuff_storm_crmod, self.dotbuff_storm_dhmod = self.check_buff()
        self.dotbuff_caustic_mod, self.dotbuff_caustic_crmod, self.dotbuff_caustic_dhmod = self.check_buff()
        
        if np.random.random()<0.35:
            self.available_straight = 1
            if self.print_log:
                print('Refulgent Arrow Available')
        
        self.weapon_skill()
        return dmg
        
    def raging(self):
        if (self.cool_raging<=0 and self.ngc>0):
            self.buff_raging=20* self.time_multiply
            self.cool_raging = 120 * self.time_multiply
            
            if self.print_log:
                print('Raging Strikes time:', round(self.elapsed/self.time_multiply,2))
            self.event_log.append(('Raging Strikes','Buff', np.nan, np.nan,np.nan, round(self.elapsed/self.time_multiply,3)))
            self.ability()
            
    def battle(self):
        if (self.cool_battle<=0 and self.ngc>0):
            self.buff_battle = 15* self.time_multiply
            self.cool_battle = 120 * self.time_multiply
            
            if self.print_log:
                print('Battle Voice time:', round(self.elapsed/self.time_multiply,2))
            
            self.event_log.append(('Battle Voice','Buff', np.nan, np.nan,np.nan, round(self.elapsed/self.time_multiply,3)))
            self.ability()
        
    def barrage(self):
        if (self.cool_barrage<=0 and self.ngc>0):
            self.buff_barrage = 10* self.time_multiply
            self.cool_barrage = 120 * self.time_multiply
            self.available_straight = 1
            
            if self.print_log:
                print('Barrage time:', round(self.elapsed/self.time_multiply,2))
            
            self.event_log.append(('Barrage','Buff', np.nan, np.nan,np.nan, round(self.elapsed/self.time_multiply,3)))
            self.ability()
            
    def radient(self):
        if (self.cool_radient<=0 and self.ngc>0):
            if (self.buff_army>0 or self.buff_wanderer>0 or self.buff_mage>0):
                self.buff_radient = 15* self.time_multiply
                self.cool_radient = 110* self.time_multiply
                self.radient_coda = self.stack_coda
                self.stack_coda = 0
                
                if self.print_log:
                    print('Radient Finale time:', round(self.elapsed/self.time_multiply,2))
                self.event_log.append(('Radient Finale','Buff', np.nan, np.nan,np.nan, round(self.elapsed/self.time_multiply,3)))
                self.ability()
                
    def blood(self):
        if (self.available_blood ==0 and self.cool_blood>0):
            self.waiting(self.cool_blood)
        
        if (self.available_blood>0 and self.ngc>0): 
            if self.available_blood==3:
                self.cool_blood = 15 * self.time_multiply
            
            dmg = self.calculate_dmg(110,'Bloodletter')
            self.available_blood-=1
            self.ability()
            return dmg
    
    def empyreal(self):
        if self.cool_empyreal>0:
            self.waiting(self.cool_empyreal)
        
        if (self.cool_empyreal<=0 and self.ngc>0):
            dmg = self.calculate_dmg(220,'Empyreal Arrow')
            self.song_effect()
            self.cool_empyreal = 15* self.time_multiply
            self.ability()
            return dmg
    
    def sidewinder(self):
        if self.cool_sidewinder>0:
            self.waiting(self.cool_sidewinder)
        
        if (self.cool_sidewinder<=0 and self.ngc>0):
            dmg = self.calculate_dmg(300,'Sidewinder')
            self.cool_sidewinder = 60* self.time_multiply
            self.ability()
            return dmg
    
    def pitch(self):
        if (self.buff_wanderer>0 and self.stack_wanderer>0):
            if self.stack_wanderer==1:
                dmg = self.calculate_dmg(100,'Pitch Perfect')
            elif self.stack_wanderer==2:
                dmg = self.calculate_dmg(220,'Pitch Perfect')
            elif self.stack_wanderer==3:
                dmg = self.calculate_dmg(360,'Pitch Perfect')
            
            self.stack_wanderer = 0
            self.ability()
            return dmg
        
    def wanderer_minuet(self):
        if self.cool_wanderer>0:
            self.waiting(self.cool_wanderer)
        
        if self.cool_wanderer<=0:
            self.buff_wanderer = 45 * self.time_multiply
            self.stack_coda +=1
            self.cool_wanderer = 120* self.time_multiply
            self.tick_song = 3 * self.time_multiply
            self.calculate_gc(0)
            
            self.buff_mage = 0
            self.buff_army = 0 
            
            dmg = self.calculate_dmg(100,"Wanderer Minuet")
            self.ability()
            return dmg
    
    def mage_ballad(self):
        if self.cool_mage>0:
            self.waiting(self.cool_mage)
        
        if self.cool_mage <=0:
            self.buff_mage = 45* self.time_multiply
            self.stack_coda +=1
            self.cool_mage = 120* self.time_multiply

            self.tick_song = 3* self.time_multiply
            self.calculate_gc(0)
            
            self.buff_wanderer = 0
            self.buff_army = 0
            
            dmg = self.calculate_dmg(100,"Mage Ballad")
            self.ability()
            return dmg
    
    def army_paeon(self):
        if self.cool_army>0:
            self.waiting(self.cool_army)
        
        if self.cool_army <=0:
            self.buff_army = 45* self.time_multiply
            self.stack_coda +=1
            self.cool_army = 120* self.time_multiply
            
            self.tick_song = 3* self.time_multiply
            self.calculate_gc(0)
            
            self.buff_wanderer = 0
            self.buff_mage = 0
            
            dmg = self.calculate_dmg(100,"Army Paeon")
            self.ability()
            return dmg
    
    def tick(self,iteration=1):
        for i in range(iteration):
            self.elapsed += self.time_per_tick
            
            if self.buff_wanderer>0:
                self.buff_wanderer-=self.time_per_tick
            elif self.buff_mage>0:
                self.buff_mage-=self.time_per_tick
            elif self.buff_army>0:
                self.buff_army-=self.time_per_tick
                
                
            self.tick_autoshot-=self.time_per_tick
            self.dot_caustic-=self.time_per_tick
            self.dot_storm-=self.time_per_tick
            
            if self.cool_army>0:
                self.cool_army -= self.time_per_tick
            if self.cool_barrage>0:
                self.cool_barrage -= self.time_per_tick
            if self.cool_battle>0:
                self.cool_battle -= self.time_per_tick
            if self.cool_blood>0:
                self.cool_blood -= self.time_per_tick
            if self.cool_mage>0:
                self.cool_mage -= self.time_per_tick
            if self.cool_radient>0:
                self.cool_radient -= self.time_per_tick
            if self.cool_raging>0:
                self.cool_raging -= self.time_per_tick
            if self.cool_wanderer>0:
                self.cool_wanderer -= self.time_per_tick
            if self.cool_empyreal>0:
                self.cool_empyreal -= self.time_per_tick
            if self.cool_sidewinder>0:
                self.cool_sidewinder -= self.time_per_tick
            
            if self.buff_battle>0:
                self.buff_battle -= self.time_per_tick
            if self.buff_radient>0:
                self.buff_radient -= self.time_per_tick
            if self.buff_raging>0:
                self.buff_raging -= self.time_per_tick
            if self.buff_barrage>0:
                self.buff_barrage -= self.time_per_tick
            
            self.global_cooldown -= self.time_per_tick
                
            if (self.cool_blood <=0 and self.available_blood<3):
                self.available_blood+=1
                self.cool_blood += 15 *self.time_multiply
                
            if (self.buff_wanderer>0 or self.buff_mage>0 or self.buff_army>0):
                self.tick_song-=self.time_per_tick
                if self.tick_song<0.001:
                    self.effect_over_tick(self.elapsed)
                    self.tick_song = 3 * self.time_multiply
                
            if self.dot_caustic>0:
                self.tick_dot_caustic -= self.time_per_tick
                if self.tick_dot_caustic<=0:
                    self.calculate_DOT(20,self.dotbuff_caustic_mod, self.dotbuff_caustic_dhmod, self.dotbuff_caustic_crmod,"Caustic")
                    self.tick_dot_caustic = 3* self.time_multiply
                    
            if self.dot_storm>0:
                self.tick_dot_storm -= self.time_per_tick
                if self.tick_dot_storm<=0:
                    self.calculate_DOT(25,self.dotbuff_storm_mod, self.dotbuff_storm_dhmod, self.dotbuff_storm_crmod,"Storm")
                    self.tick_dot_storm = 3* self.time_multiply   
            
            if self.tick_autoshot<=0:
                self.tick_autoshot = 3* self.time_multiply
                self.auto_shot()
                
            if self.elapsed > self.left_time*self.time_multiply:
                self.done=1
            
    def effect_over_tick(self,elapsed):
        randomnumber = np.random.random()
        if randomnumber<0.8:
            self.song_effect()

        
    def calculate_gc(self,stack_army):
        self.gc_ap = self.gc*(1-stack_army*0.04)
        
    def song_effect(self):
        if self.buff_wanderer>0:
            if self.stack_wanderer<3:
                self.stack_wanderer+=1
                
        elif self.buff_mage>0:
            self.cool_blood -= 7.5 * self.time_multiply

        elif self.buff_army>0:
            if self.stack_army<4:
                self.stack_army+=1
                self.calculate_gc(self.stack_army)
                
        if self.soul<100:
            self.soul+=5
            
        if self.print_log:
            if self.buff_wanderer>0:
                print('Wanderer Repertoire:', self.stack_wanderer, 'time:',self.elapsed/self.time_multiply)
            if self.buff_mage>0:
                print('Mage Repertoire Blood available:', self.available_blood, 'Blood cooldown',self.cool_blood/self.time_multiply, 'time:',self.elapsed/self.time_multiply)
            if self.buff_army>0:
                print('Army Repertoire:',self.stack_army, 'Global cooldwn:', self.gc_ap,'time:',self.elapsed/self.time_multiply)
    
    def weapon_skill(self):
        self.ngc = 2
        self.global_cooldown = self.gc_ap
        self.tick(self.tick_per_act)
        
    def ability(self):
        self.ngc -=1
        self.tick(self.tick_per_act)
        if self.ngc ==0:
            while self.global_cooldown>0:
                self.tick()
                
    def waiting(self,cooldown):
        left_time = self.global_cooldown - self.tick_per_act * self.ngc
        if (cooldown>0 and cooldown<left_time):
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
        
        self.battery = 0
        self.heat = 0
    
    def initialize_cooldown(self):
        self.cool_drill = 0
        self.cool_airanchor = 0
        self.cool_chainsaw = 0
        self.cool_reassemble = 0
        self.cool_gaussround = 0
        self.cool_wildfire = 0
        self.cool_ricochet = 0
        self.cool_barrelstabilizer = 0
        
    def initialize_buff(self):
        self.buff_reassemble = 0
        self.buff_hypercharge = 0
        
    def drill(self):
        if self.cool_drill==0:
            dmg = self.calculate_dmg(580, 'Drill')
            self.cool_drill = self.gc * 8
            return dmg
        
    def airanchor(self):
        if self.cool_airanchor==0:
            dmg = self.calculate_dmg(580, 'Air Anchor')
            self.cool_airanchor = self.gc*16
            self.battery += 20
            if self.battery>100:
                self.battery = 100
            return dmg
        
    def chainsaw(self):
        if self.cool_chainsaw==0:
            dmg = self.calculate_dmg(580, 'Chainsaw')
            self.cool_chainsaw = self.gc *24
            self.battery += 20
            if self.battery>100:
                self.battery = 100
            return dmg
        
    def gaussround(self):
        if self.cool_gaussround==0:
            dmg = self.calculate_dmg(120, 'Gauss Round')
            self.cool_gaussround = 30 * self.time_multiply
            return dmg
            
    def ricochet(self):
        if self.cool_gaussround == 0:
            dmg = self.calculate_dmg(120, 'Ricochet')
            self.cool_ricochet = 30 * self.time_multiply
            return dmg
        
    def heatblast(self):
        if self.global_cooldown>0:
            while self.global_cooldown>0:
                self.tick()
        
        self.ngc = 1
        self.global_cooldown = 1.5 * self.time_multiply
        dmg = self.calculate_dmg(180,'Technical Finish')
        self.cool_gaussround -= 15 * self.time_multiply
        self.cool_ricochet -= 15 * self.time_multiply
        
        return dmg
    
    def splitshot(self):
        if self.global_cooldown>0:
            while self.global_cooldown>0:
                self.tick()
        dmg = self.calculate_dmg(200, 'Split Shot')
        
        self.heat +=5
        if self.heat>100:
            self.heat = 100
        
        self.weapon_skill()
        return dmg
    
    def slugshot(self):
        if self.global_cooldown>0:
            while self.global_cooldown>0:
                self.tick()
        dmg = self.calculate_dmg(280, 'Slug Shot')
        self.heat +=5
        
        if self.heat>100:
            self.heat = 100
        self.weapon_skill()
        return dmg
    
    def cleanshot(self):
        if self.global_cooldown>0:
            while self.global_cooldown>0:
                self.tick()
        dmg = self.calculate_dmg(360, 'Slug Shot')
        self.heat +=10
        
        if self.heat>100:
            self.heat = 100
        self.battery += 10
        
        if self.battery>100:
            self.battery = 100
        
        self.weapon_skill()
        return dmg
        
        
    def queen_armpunch(self):
        self.queen_cool = 1.56 * self.time_multiply
        dmg = self.calculate_dmg(120, 'Queen ArmPunch')
        return dmg
    
    def queen_dash(self):
        self.queen_cool = 3.17 * self.time_multiply
        dmg = self.calculate_dmg(240, 'Queen Dash')
        return dmg
    
    def queen_pilebunker(self):
        self.queen_cool = 2.05 * self.time_multiply
        dmg = self.calculate_dmg(680, 'Queen Pilebunker')
        return dmg
    
    def queen_collider(self):
        dmg = self.calculate_dmg(780, 'Queen Collider')
        return dmg
    
    def automaton_queen(self):
        self.queen_left = self.batter * 0.2 * self.time_multiply
        self.battery = 0
        self.ability()
        self.queen_dash()
        
    def wildfire(self):
        self.wildfire_left = 10 * self.time_multiply
        self.cool_wildfire = 120 * self.time_multiply
    
    def detonator(self, hit = 6):
        dmg = self.calculate_dmg(220 * hit, 'Wildfire')
        return dmg
        
    def tick(self,iteration=1):
        for i in range(iteration):
            self.elapsed += self.time_per_tick
                
            self.tick_autoshot-=self.time_per_tick
            
            self.cool_ -= self.time_per_tick
            
            self.buff_ -= self.time_per_tick
            
            self.global_cooldown -= self.time_per_tick
            
            self.wildfire_left -= self.time_per_tick
            if self.wildfire_left==0:
                self.detonator()
            
            if self.tick_autoshot<0.001:
                self.tick_autoshot = 3* self.time_multiply
                self.auto_shot()
                
                
            
                
                
            if self.elapsed > self.left_time:
                self.done=1
        
        
        
if __name__=='__main__':

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
    
    agent = Dancer(cr,dh,dt,dex,wd,spd,period,print_log = 1)

    #https://etro.gg/gearset/cec981af-25c7-4ffb-905e-3024411b797a
    period = 300
    cr = 2229
    dt = 1381
    dh = 1662
    spd = 479
    dex = 2575
    wd = 120
    weapon_delay = 3.04

    main = 390
    sub = 400
    div = 1900
    
    pcr,dcr = f.f_crit(cr)
    pdh = f.f_dh(dh)
    
    bard = Bard(cr,dh,dt,dex,wd,spd,period,print_log = 1)
