# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 02:48:21 2021

@author: luist
"""

# Import libraries
import cv2
import random
import numpy as np
import csv
import json
import argparse

#parser = argparse.ArgumentParser(description = 'Corrosion circuits marker tool')
#parser.add_argument('-ip','--ippath', type=str, help= 'Path to inspection points .txt files')
#parser.add_argument('-ps','--pspath', type= str, help = 'Path to pipe specs .txt files')
#parser.add_argument('-img','--imagepath', type=str, help = 'Path to drawings .jpg file')
#args = parser.parse_args()


#Ask user for the drawing he wants to work with
def get_drawfile():
    ans = input ('Type drawing name file: ')
    return ans

ans = get_drawfile()
filepath = 'boxes/' + str(ans) + '.json'
imagepath = 'data/images/' +str(ans) + '.jpg'

#Setting paths 
image = cv2.imread(imagepath)

# Open directionaries
with open(filepath, 'r') as fp:
    data = json.load(fp)

# Show the specs found
for key, value in data.items() :
    print ('Specs found: ', key)
    
#Ask user the code to look for

def get_user():
    user = input('Type the pipe code you wish to visualize: ')
    print ('Looking for: ', user)
    return user

def get_user2():
    user2 = input('Type the pipe code you wish to visualize: ')
    print ('Looking for: ', user2)
    return user2

# define function get color:
def get_color():
    
    r = 0
    g = 0
    b = 0

    inp = input ('Pick marker color: \n"r" for red \n"g" for green \n"b" for blue \n ====>')
     
    if inp == 'r':
        r = 255
        g = 0
        b = 0
        print ('Red marker')
        
    if inp == 'g':
        r = 0
        g = 255
        b = 0
        print('green marker')
    
    if inp == 'b':
        r = 0
        g = 0
        b = 255
        print ('blue marker')
        
    if inp != 'r' and inp != 'g' and inp != 'b' :
        print('invalid color, using default red line color')
        r = 255
        g = 0
        b = 0
    
    return b, g, r

#define function get boxes
def get_boxes(user, b, g, r):
    
    # Set variables
    i = 0
    down = 0
    up = 4
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    
    coord = []
    
    # Look for the code input
    if user in data:
        #print ('Valid input')
        coord = data[user]
        det = len(coord)/4
        
        #Look for all the coordinates
        while i < det:
            #get box coordinates
            draw = []
            draw = coord[down:up]
            x1 = draw[0]
            y1 = draw[1]
            x2 = draw[2]
            y2 = draw[3]
    
            cv2.rectangle(image, (x1, y1), (x2, y2), (b, g, r), 3)
            
            down = down+4
            up = up + 4
            i = i+1
        
    else:
        print ('No detections found in this drawing')

user = get_user()
b, g, r = get_color()
get_boxes (user, b, g, r)


image_to_show = np.copy(image)

mouse_pressed = False
s_x = s_y = e_x = e_y = -1

def mouse_callback(event, x, y, flags, param):
    global image_to_show, s_x, s_y, e_x, e_y, mouse_pressed
    
    if event == cv2.EVENT_LBUTTONDOWN:
        mouse_pressed = True
        s_x, s_y = x, y
        image_to_show = np.copy(image)
    elif event == cv2.EVENT_MOUSEMOVE:
        if mouse_pressed:
            image_to_show = np.copy(image)
            cv2.rectangle(image_to_show, (s_x, s_y),(x, y), (255, 255, 0), 5)
    elif event == cv2.EVENT_LBUTTONUP:
        mouse_pressed = False
        e_x, e_y = x, y

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', 1280, 720)
cv2.setMouseCallback('image', mouse_callback)

while True:
    cv2.imshow('image', image_to_show)
    k = cv2.waitKey(1)
    
    if k == ord('a'):
        if s_y > e_y:
            s_y, e_y = e_y, s_y
        
        if s_x > e_x:
            s_x, e_x = e_x, s_x
        
        if e_y - s_y > 1 and e_x - s_x > 0:
            
            cut = image[s_y:e_y, s_x:e_x]
            hsv = cv2.cvtColor(cut, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(hsv, 0, 255,cv2.THRESH_BINARY_INV |cv2.THRESH_OTSU)
            indices = np.where(mask==255)
            #change to red color
            cut[indices[0], indices[1], :] = [b, g, r]
            image_to_show = np.copy(image)
        
    if k == ord('s'):
        cv2.imwrite('corr_circuits/marked_' + str(ans) +'.jpg', image_to_show)
        print('The drawing has been saved in "corr_circuits" folder')
        break
    
    if k == ord ('n'):
        s_x = s_y = e_x = e_y = -1
        user = get_user2()
        b, g, r = get_color()
        get_boxes (user, b, g, r)
        if s_y > e_y:
            s_y, e_y = e_y, s_y
        
        if s_x > e_x:
            s_x, e_x = e_x, s_x
        
        if e_y - s_y > 1 and e_x - s_x > 0:
            
            cutn = image[s_y:e_y, s_x:e_x]
            hsv = cv2.cvtColor(cutn, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(hsv, 0, 255,cv2.THRESH_BINARY_INV |cv2.THRESH_OTSU)
            indices = np.where(mask==255)
            #change to red color
            cutn[indices[0], indices[1], :] = [b, g, r]
            image_to_show = np.copy(image)
        
    elif k == 27:
        break
cv2.destroyAllWindows()
