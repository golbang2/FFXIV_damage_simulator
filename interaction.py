# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 04:45:27 2022

@author: ty
"""

import pyautogui
import time
import numpy as np
from PIL import ImageGrab, Image
from matplotlib import pyplot as plt
import cv2
import win32gui, win32com.client
import os
from win32api import GetSystemMetrics

def act_number(action_number,frame):
    if action_number==1:
        pyautogui.keyDown('a')
        pyautogui.keyDown('s')
        time.sleep(1/frame)
        pyautogui.keyUp('a') 
        pyautogui.keyUp('s') 
    if action_number==2:
        pyautogui.keyDown('s')
        time.sleep(1/frame)
        pyautogui.keyUp('s') 
    if action_number==3:
        pyautogui.keyDown('s')
        pyautogui.keyDown('a')
        time.sleep(1/frame)
        pyautogui.keyUp('s') 
        pyautogui.keyUp('a') 
    if action_number==4:
        pyautogui.keyDown('a')
        time.sleep(1/frame)
        pyautogui.keyUp('a') 
    if action_number==5:
        time.sleep(1/frame)
    if action_number==6:
        pyautogui.keyDown('d') 
        time.sleep(1/frame)
        pyautogui.keyUp('d')
    if action_number==7:
        pyautogui.keyDown('w')
        pyautogui.keyDown('a')
        time.sleep(1/frame)
        pyautogui.keyDown('w')
        pyautogui.keyUp('a')
    if action_number==8:
        pyautogui.keyDown('w') 
        time.sleep(1/frame)
        pyautogui.keyUp('w')
    if action_number==9:
        pyautogui.keyDown('w') 
        pyautogui.keyDown('d') 
        time.sleep(1/frame)
        pyautogui.keyUp('w')
        pyautogui.keyUp('d')     
    if action_number==0:
        pyautogui.keyDown('enter') 
        time.sleep(1/frame)
        pyautogui.keyUp('enter')

def select_random_action():
    return np.random.randint(1,10)

def resize_img(img,rect):
    img = np.array(img)
    if (rect[1]+31<0 or rect[0]+8<0):
        print('Move window location')
    img = img[rect[1]+31:rect[3]-8,rect[0]+8:rect[2]-8]
    return img

def capture_screen(rect,img_size = (512,320)):
    img = ImageGrab.grab()
    img = resize_img(img,rect)
    img = cv2.resize(img,img_size, interpolation=cv2.INTER_AREA)
    return img

def get_window_rect(process_name = 'Vampire Survivors'):
    window_handle = win32gui.FindWindow(None, process_name)
    window_rect   = win32gui.GetWindowRect(window_handle)
    return window_rect

def save_img(img,name,path):
    img = Image.fromarray(img,'RGB')
    make_folder(path)
    img.save(path+name+'.png')

def capture_per_frame(rect,path, img_size = (512,320),sec=600):
    for i in range(sec*frame):
        time.sleep(1/frame)
        img = capture_screen(rect,img_size)
        save_img(img,str(i),path)

def call_window(process_name = 'Vampire Survivors'):
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')
    window_handle = win32gui.FindWindow(None, process_name)
    win32gui.SetForegroundWindow(window_handle)

def start_record(path,process_name ,sec = 600):
    call_window(process_name)
    rect = get_window_rect()
    capture_per_frame(rect,path ,sec)

def load_state_img(path = './game_state/'):
    state_list = os.listdir(path)
    image_list = []
    for i in state_list:
        img = Image.open(path+i)
        image_list.append(img)
    return image_list

def make_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def check_state(img_array,screen):
    if np.min(screen[40:40+15,168:168+177]==np.array(img_array[0])[40:40+15,168:168+177]):
        state = 'character'
    elif np.min(screen[215:215+15,235:235+40]==np.array(img_array[1])[215:215+15,235:235+40]):
        state = 'gameover'
    elif np.min(screen[45:45+15,210:210+40]==np.array(img_array[2])[45:45+15,210:210+40]):
        state = 'levelup'
    elif np.min(screen[40:40+15,200:200+40]==np.array(img_array[3])[40:40+15,200:200+40]):
        state = 'map'
    elif np.min(screen[40:40+15,220:220+40]==np.array(img_array[4])[40:40+15,220:220+40]):
        state = 'results'            
    elif np.min(screen[70:70+25,200:200+60]==np.array(img_array[5])[70:70+25,200:200+60]):
        state = 'start'
    elif np.min(screen[45:45+15,185:185+140]==np.array(img_array[6])[45:45+15,185:185+140]):
        state = 'treasure'
    else:
        state = 'play'
    return state

def capture_with_state(rect, path, img_array, done, img_size=(512,320)):
    i = 0
    while not done:
        time.sleep(1/frame)
        img = capture_screen(rect,img_size)
        save_img(img,str(i),path)
        state = check_state(img_array,img)
        i+=1
        return state

def delete_folder(path='../logs/'):
    file_list = os.listdir(path)
    for i in file_list:
        os.remove(path+i)

if __name__=='__main__':
    frame = 10
    img_size = (512,320)
    log_path= 'd:/logs/'
    game_state_path = 'd:/logs/FFXIV'
    game_name = 'Final Fantasy XIV'
    resolution = (GetSystemMetrics(0),GetSystemMetrics(1))
    
    rect = get_window_rect(game_name)
    state_img = load_state_img(game_state_path)
    
    #start_record(log_path)