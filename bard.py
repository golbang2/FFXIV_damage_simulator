# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 14:10:48 2022

@author: atgol
"""
import ffxiv_calculate_damage as f
import numpy as np

class bard():
    def __init__(self,gc,cr,dh,dt,stat,wd,spd,period, print_log =0):
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
        self.autoshot_tick = 0
        
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
        
        self.print_log = print_log
        self.time_per_tick = 0.01
        
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
        self.cool_sidewinder = 0
    
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
        
    def calculate_dmg(self,potency,skill_name):
        buff, pcr, pdh = self.check_buff()
            
        d1 = int(potency * self.atk * self.dt)
        d2 = int(int(d1*int(self.wd))*self.jobmod/100)
        d3 = d2
        
        is_crit, is_dh = False, False
        
        if np.random.random()<pcr:
            d3 = int(d3 * self.dcr)
            is_crit = True
        if np.random.random()<pdh:
            d3 = int(d3*1.25)
            is_dh = True
        
        dmg = f.random_dmg(d3)*buff
        
        if self.print_log:
            print(skill_name, int(dmg), 'Crit:', is_crit, 'DirectHit:', is_dh, 'time: ', round(self.elapsed,2))
            
        
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
            print('DOT_',skill_name, int(dmg), 'Crit:', is_crit, 'DirectHit:', is_dh, 'time: ', round(self.elapsed,2))
        
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
            print('AutoShot', int(dmg), 'Crit:', is_crit, 'DirectHit:', is_dh, 'time: ', round(self.elapsed,2))
        return dmg
    
    def burst_shot(self):
        if self.global_cooldown<=0:
            dmg = self.calculate_dmg(220, 'Burst Shot')
            if self.available_straight:
                if self.barrage>0:
                    dmg = self.calculate_dmg(280,'Refulgent Arrow')+self.calculate_dmg(280,'Refulgent Arrow')+self.calculate_dmg(280,'Refulgent Arrow')
                    self.barrage = 0
                else:
                    dmg = self.calculate_dmg(280,'Refulgent Arrow')
            else:
                if np.random.random()<0.35:
                    self.available_straight = 1
                    if self.print_log:
                        print('buff_straight')
            
            self.weapon_skill()
            
            return dmg
        
    def apex_arrow(self):
        if self.global_cooldown<=0:
            if self.soul>20:
                dmg = self.calculate_dmg(self.soul*5,'Apex Arrow')
                self.weapon_skill()
                if self.soul>80:
                    self.available_blast=1
                return dmg
        
    def blast_arrow(self):
        if self.global_cooldown<=0:
            if self.available_blast:
                dmg = self.calculate_dmg(600,'Blast Arrow')
                self.weapon_skill()
                return dmg
        
    def stormbite(self):
        if self.global_cooldown<=0:
            dmg = self.calculate_dmg(100,'Stormbite')
            self.dot_storm = 45.
            
            self.dot_storm_tick = 3.
            
            self.dotbuff_storm_mod, self.dotbuff_storm_crmod, self.dotbuff_storm_dhmod = self.check_buff()
            
            if np.random.random()<0.35:
                self.available_straight = 1
                if self.print_log:
                    print('buff_straight')
        
            self.weapon_skill()
            return dmg
        
    def causticbite(self):
        if self.global_cooldown<=0:
            dmg = self.calculate_dmg(150,'Causticbite')
            self.dot_caustic = 45.
            self.dot_caustic_tick = 3.
            self.dotbuff_caustic_mod, self.dotbuff_caustic_crmod, self.dotbuff_caustic_dhmod = self.check_buff()
            
            if np.random.random()<0.35:
                self.available_straight = 1
                if self.print_log:
                    print('buff_straight')
        
            self.weapon_skill()
            return dmg
        
    def iron_jaws(self):
        if self.global_cooldown<=0:
            dmg = self.calculate_dmg(100,'Iron Jaws')
            self.caustic = 45
            self.storm = 45
            
            self.start_caustic = self.elapsed
            self.start_storm = self.elapsed
            
            self.dotbuff_storm_mod, self.dotbuff_storm_crmod, self.dotbuff_storm_dhmod = self.check_buff()
            self.dotbuff_caustic_mod, self.dotbuff_caustic_crmod, self.dotbuff_caustic_dhmod = self.check_buff()
            
            if np.random.random()<0.35:
                self.available_straight = 1
                if self.print_log:
                    print('buff_straight')
            
            self.weapon_skill()
            return dmg
        
    def raging(self):
        if (self.cool_raging<0 and self.ngc>0):
            self.buff_raging=20.
            self.cool_raging = 120.
            self.ability()
            
            if self.print_log:
                print('Raging Strikes time:', round(self.elapsed,2))
            
    def battle(self):
        if (self.cool_battle<0 and self.ngc>0):
            self.buff_battle = 15
            self.cool_battle = 120
            self.ability()
            
            if self.print_log:
                print('Battle Voice time:', round(self.elapsed,2))
        
    def barrage(self):
        if (self.cool_barrage<0 and self.ngc>0):
            self.buff_barrage = 10.
            self.cool_barrage = 120.
            self.straight = 1
            self.ability()
            
            if self.print_log:
                print('Barrage time:', round(self.elapsed,2))
            
    def radient(self):
        if (self.cool_radient<0 and self.ngc>0):
            if (self.army>0 or self.wanderer>0 or self.mage>0):
                self.buff_radient = 15.
                self.cool_radient = 110.
                self.radient_coda = self.coda
                self.stack_coda = 0
                self.ability()
                
                if self.print_log:
                    print('Radient Finale time:', round(self.elapsed,2))
                
    def blood(self):
        if (self.available_blood>0 and self.ngc>0): 
            dmg = self.calculate_dmg(110,'Bloodletter')
            self.available_blood-=1
            self.cool_blood =15.
            self.ability()
        return dmg
    
    def empyreal(self):
        if (self.cool_empyreal<0 and self.ngc>0):
            dmg = self.calculate_dmg(220,'Empyreal Arrow')
            self.song_effect()
            self.ability()
        return dmg
    
    def sidewinder(self):
        if (self.cool_sidewinder<0 and self.ngc>0):
            dmg = self.calculate_dmg(300,'Sidewinder')
            self.ability()
        return dmg
    
    def pitch(self):
        if (self.wanderer>0 and self.stack_wanderer>0):
            if self.stack_wanderer==1:
                dmg = self.calculate_dmg(100,'Pitch Perfect')
            elif self.stack_wanderer==2:
                dmg = self.calculate_dmg(220,'Pitch Perfect')
            elif self.stack_wanderer==3:
                dmg = self.calculate_dmg(360,'Pitch Perfect')
            self.ability()
            return dmg
        
    def wanderer_minuet(self):
        if self.cool_wanderer<0:
            self.wanderer = 45
            self.stack_coda +=1
            self.cool_wanderer = 120
            self.tick_song = 3.
            self.calculate_gc(0)
            
            self.mage = 0
            self.army = 0 
            
            self.ability()
            
            dmg = self.calculate_dmg(100,"Wanderer Minuet")
            return dmg
    
    def mage_ballad(self):
        if self.cool_mage <0:
            self.mage = 30
            self.stack_coda +=1
            self.cool_mage = 120

            self.tick_song = 3.
            self.calculate_gc(0)
            
            self.wanderer = 0
            self.army = 0
            
            self.ability()
            dmg = self.calculate_dmg(100,"Mage Ballad")
            return dmg
    
    def army_paeon(self):
        if self.cool_army <0:
            self.army = 45
            self.stack_coda +=1
            self.cool_mage = 120
            
            self.tick_song = 3.
            self.calculate_gc(0)
            
            self.wanderer = 0
            self.mage = 0
            
            self.ability()
            dmg = self.calculate_dmg(100,"Army Paeon")
            return dmg
    
    def tick(self,iteration=1):
        for i in range(iteration):
            
            self.elapsed += self.time_per_tick
            
            if self.wanderer>0:
                self.wanderer-=self.time_per_tick
            elif self.mage>0:
                self.mage-=self.time_per_tick
            elif self.army>0:
                self.army-=self.time_per_tick
                
                
            self.autoshot_tick-=self.time_per_tick
            self.dot_caustic-=self.time_per_tick
            self.dot_storm-=self.time_per_tick
            
            self.cool_army -= self.time_per_tick
            self.cool_barrage -= self.time_per_tick
            self.cool_battle -= self.time_per_tick
            self.cool_blood -= self.time_per_tick
            self.cool_mage -= self.time_per_tick
            self.cool_radient -= self.time_per_tick
            self.cool_raging -= self.time_per_tick
            self.cool_wanderer -= self.time_per_tick
            self.cool_empyreal -= self.time_per_tick
            self.cool_sidewinder -= self.time_per_tick
            
            self.buff_battle -= self.time_per_tick
            self.buff_radient -= self.time_per_tick
            self.buff_raging -= self.time_per_tick
            self.buff_barrage -= self.time_per_tick
            
            self.global_cooldown -= self.time_per_tick
                
            if (self.cool_blood <0 and self.available_blood<3):
                self.available_blood+=1
                self.cool_blood = 15
                
            if (self.wanderer>0 or self.mage>0 or self.army>0):
                self.tick_song-=self.time_per_tick
                if self.tick_song<0.001:
                    self.effect_over_tick(self.elapsed)
                    self.tick_song = 3.
                
            if self.dot_caustic>0:
                self.dot_caustic_tick -= self.time_per_tick
                if self.dot_caustic_tick<0.001:
                    self.calculate_DOT(20,self.dotbuff_caustic_mod, self.dotbuff_caustic_dhmod, self.dotbuff_caustic_crmod,"Caustic")
                    self.dot_caustic_tick = 3.
                    
            if self.dot_storm>0:
                self.dot_storm_tick -= self.time_per_tick
                if self.dot_storm_tick<0.001:
                    self.calculate_DOT(25,self.dotbuff_storm_mod, self.dotbuff_storm_dhmod, self.dotbuff_storm_crmod,"Storm")
                    self.dot_storm_tick = 3.    
            
            if self.autoshot_tick<0.001:
                self.autoshot_tick = 3
                self.auto_shot()
                
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
        self.tick(60)
        
    def ability(self):
        self.ngc -=1
        self.tick(60)
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
    
    agent = bard(gc,cr,dh,dt,stat,wd,spd,period,print_log = 1)