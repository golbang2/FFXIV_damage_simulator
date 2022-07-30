# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 22:19:58 2022

@author: ty
"""

import pyautogui 
import time
import interaction
import datetime

def click(x,y,button = 'left',repeat = 2):
    time.sleep(global_delay)
    for i in range(repeat):
        pyautogui.mouseDown(x+window*1920,y,button = button)
        time.sleep(0.05)
        pyautogui.mouseUp(button=button)
    
def press_key(button,repeat=1):
    time.sleep(global_delay)
    for i in range(repeat):
        time.sleep(global_delay)
        pyautogui.keyDown(button)
        time.sleep(0.05)
        pyautogui.keyUp(button) 

def make(iteration,button='x', wait=19):
    interaction.call_window(process_name)
    for i in range(iteration):
        time.sleep(0.3)
        click(1342,698)
        time.sleep(1)
        press_key(button)
        time.sleep(wait)
        print(i)
        
def make2(iteration,button1 = 'r', button2 = 't', wait1= 37, wait2=31):
    interaction.call_window(process_name)
    for i in range(iteration):
        time.sleep(0.3)
        click(1342,698)
        time.sleep(1)
        press_key(button1)
        time.sleep(wait1)
        press_key(button2)
        time.sleep(wait2)
        print(i)

def quest(iteration):
    interaction.call_window(process_name)
    for i in range(iteration):
        click(365,420,'right') #에이리쿠르 위치
        click(842,541)
        click(842,541)
        click(648,622,repeat = 1)
        click(885,622,repeat = 2)
        click(845,584,repeat = 2)
        click(1530,413,'right') #모이스 위치
        click(957,550,repeat=2) #의뢰선택
        for j in range(2):
            click(1230,180,'right',repeat=2) #쿠키선택
            click(1230,180,repeat = 1)
            click(1254,218) #건네주기
            click(904,561,repeat = 3) #hq아이템
            click(877,333,repeat = 2) 
            click(923,531,repeat = 2) 
        click(1230,180,'right',repeat=2) #쿠키선택
        click(1230,180,repeat = 1)
        click(1254,218) #건네주기
        click(904,561,repeat = 3) #hq아이템
        click(877,333,repeat = 2) 
        time.sleep(1)
        print(i)

process_name = 'FINAL FANTASY XIV'

iteration = 100
position_x = 3285
position_y = 918
window = 0

pyautogui.position()
global_delay = 0.1

interaction.call_window('FINAL FANTASY XIV')
for i in range(2000):
    d1 = datetime.datetime.now()
    press_key('1')
    press_key('Q')
    d2 = datetime.datetime.now()
    ddt = (d2-d1).total_seconds()
    time.sleep(2.46-ddt)

