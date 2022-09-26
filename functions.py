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

def f_gc(spd):
    return int(2500*(1000+math.ceil(130*(400-spd)/1900))/10000)/100