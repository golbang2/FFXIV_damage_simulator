# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 21:56:43 2022

@author: atgol
"""
import numpy as np
import math

def f_crit(cr, sub=400, div = 1900):
    p_cr= int(200*(cr - sub)/div+50)
    d_cr = int(1400+(200*(cr-sub)/div))
    return p_cr*0.001,d_cr*0.001

def f_dh(dh, sub=400, div =1900):
    p_dh = int(550*(dh-sub)/div)
    return p_dh/1000
    
def f_det(dt, main=390, div = 1900):
    d_dt = int(1000+(140*(dt-main)/div))
    return d_dt*0.001

def f_wd(wd,jobmod= 115,main = 390):
    return main*jobmod*0.001+wd

def f_atk(stat):
    return (125*(stat-292)/292+100)*0.01

def exp_dmg(prob,mod=1.25):
    return (1-prob)*1+prob*mod

def random_dmg(dmg):
    return (0.1*np.random.random()+0.95)*dmg

def f_spd(sp, sub = 400, div = 1900):
    return int(130*(sp-sub)/div+1000)*0.001
    
'''
def auto_dmg(stat,weapon,delay,main=390,job=115):
    atk = (100+int(165*(stat-main)/main))/100
    auto = int(int((390*115/1000)+weapon)*delay/3)
    return int(atk*auto)
'''

def auto_dmg(stat,weapon,delay,dt,spd,main=390,job=115):
    atk = (100+int(165*(stat-main)/main))*0.01
    auto = int(int((main*job/1000)+weapon)*delay/3)
    d1 = 100 * atk * dt
    d2 = d1 * spd * auto*0.01
    return d2

def f_gc(spd):
    return int(2500*(1000+math.ceil(130*(400-spd)/1900))/10000)*0.01
