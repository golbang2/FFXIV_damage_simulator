# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 20:17:23 2022

@author: atgol
"""

import numpy as np
import pandas as pd

class read_from_csv():
    def __init__(self,path = "D:/game_plan/FFXIV/Jomusse_first.csv"):
        self.activation_log = pd.read_csv(path)
        self.activation_log = self.activation_log.fillna(0)
        
        potency_list = []
        auto_list = []
        
        for i in range(len(self.activation_log)-1,0,-1):
            if (self.activation_log['Event'][i][:8]=='Jo Musse' or self.activation_log['Event'][i][4:12] == 'Jo Musse'):
                self.activation_log = self.activation_log.drop(index=i)
            
        for i in self.activation_log['Event']:
            if i[:2]=='드릴':
                potency_list.append(570)
            if i[:3]=='사슬닻':
                potency_list.append(570)
            if i[:3]=='회전톱':
                potency_list.append(570)
            if i[:4]=='열분열탄':
                potency_list.append(380)
            if i[:5]=='열슬러그탄':
                potency_list.append(380)
            if i[:4]=='열정밀탄':
                potency_list.append(460)
            if i[:4]=='열기분사':
                potency_list.append(170)
            if i[:3]=='가우스':
                potency_list.append(120)
            if i[:4]=='도탄사격':
                potency_list.append(120)
            if i[2:5]=='퀸펀치':
                potency_list.append(120)
            if i[2:5]=='퀸파일':
                potency_list.append(650)
            if i[2:5]=='퀸충돌':
                potency_list.append(750)
            if i[:4]=='자동공격':
                potency_list.append(100)
            
            if i[:4]=='자동공격':
                auto_list.append(1)
            else:
                auto_list.append(0)
                
        self.activation_log.insert(4,'potency',potency_list)
        self.activation_log.insert(2,'auto_attack',auto_list)
        
        