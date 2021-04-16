# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 23:05:31 2021

@author: luist
"""

import cv2
import random
import numpy
import csv
import pytesseract
import json
import os

#pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'

def listToString(s): 
    # initialize an empty string
    str1 = ""   
    # traverse in the string  
    for ele in s: 
        str1 += ele  
        # return string  
    return str1 
  

def draw_boxes(ippath, pspath, imagepath):
    
    image = cv2.imread(imagepath)
    w, h = image.shape[1], image.shape[0]
    dictg = {}
    
    ### Getting pipe specs

    coordps = []
    ps_file = open (pspath, "r")
    string = ps_file.read()
    string = string.replace('[','')
    string = string.replace(']','')
    listps = string.split(",")
    #print('pipe-specs: ', listps)
    

    for i in listps:
        coordps.append(int(i))
    
    numboxes = len(coordps)/4
    #print('Detections: ', int(numboxes))
    
    i = 0
    down = 0
    up = 4
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    
    while i < numboxes:
        
        #get box coordinates
        draw = []
        draw = coordps[down:up]
        x1 = draw[0]
        y1 = draw[1]
        x2 = draw[2]
        y2 = draw[3]
        
        #crop the box
        img = cv2.imread(imagepath)
        crop_img = img[y1:y2, x1:x2]
        w, h = crop_img.shape[1], crop_img.shape[0]
        #cv2.imshow("cropped", crop_img)
        #cv2.waitKey(0)
    
        if h > w:
            crop_img = cv2.rotate(crop_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
            custom_config = r'-c tessedit_char_whitelist=|ABCDEFGHIJKLMNOPQRSTUVWXYZlb0123456789.- --psm 6'
            text = pytesseract.image_to_string(crop_img, config=custom_config)
            if text[0] != 0 and text[0] != 1 :
                img = cv2.imread(imagepath)
                crop_img = img[y1:y2, x1:x2]
                crop_img = cv2.rotate(crop_img, cv2.ROTATE_90_CLOCKWISE)
                custom_config = r'-c tessedit_char_whitelist=|ABCDEFGHIJKLMNOPQRSTUVWXYZlb0123456789.- --psm 6'
                text = pytesseract.image_to_string(crop_img, config=custom_config)
                
                pos = 0
                cont = 0
                gstring = [] #get string
                
                # convert the pytesseract text to a list to remove last two characters
                for element in range(0, len(text)-2):
                    gstring.append(text[element])
                
                #convert the list we got into a string again
                string = listToString(gstring)
                #print('checking')
                #loop the string to look for the '-' and get the location of the pipe spec
                for element in range(len(string)):
                    if cont == 4:
                        break
                    if string[element] == '-':
                        cont = cont + 1
                    pos = pos + 1
                    
                #store the pipe spec with their respective coordinates 
                sliced = string[pos:pos+3]
                
                #Check if we have stored the pipe spec already
                if sliced in dictg:
                    dictg[sliced].append(x1)
                    dictg[sliced].append(y1)
                    dictg[sliced].append(x2)
                    dictg[sliced].append(y2)
                
                #store the pipe spec
                else:
                    dictg[sliced] = [x1, y1, x2, y2]
                down = down+4
                up = up + 4
                i = i+1
                
        else:
            custom_config = r'-c tessedit_char_whitelist=|ABCDEFGHIJKLMNOPQRSTUVWXYZlb0123456789.- --psm 6'
            text = pytesseract.image_to_string(crop_img, config=custom_config)
            #print(len(text))
            pos = 0
            cont = 0
            gstring = [] #get string
            
            # convert the pytesseract text to a list to remove last two characters
            for element in range(0, len(text)-2):
                gstring.append(text[element])
            
            #convert the list we got into a string again
            string = listToString(gstring)
            #print(len(string))
            
            #loop the string to look for the '-' and get the location of the pipe spec
            for element in range(len(string)):
                if cont == 4:
                    break
                if string[element] == '-':
                    cont = cont + 1
                pos = pos + 1
                
            #store the pipe spec with their respective coordinates 
            sliced = string[pos:pos+3]
            
            #Check if we have stored the pipe spec already
            if sliced in dictg:
                dictg[sliced].append(x1)
                dictg[sliced].append(y1)
                dictg[sliced].append(x2)
                dictg[sliced].append(y2)
            
            #store the pipe spec
            else:
                dictg[sliced] = [x1, y1, x2, y2]
            down = down+4
            up = up + 4
            i = i+1
      
    ####Getting inspection points
    
    coordip = []
    ip_file = open (ippath, "r")
    string = ip_file.read()
    string = string.replace('[','')
    string = string.replace(']','')
    string = string.replace("'",'')
    listip = string.split(",")
    
    #Check there are detections in the drawing
    if listip == ['No objects found']:
        #print('No inspection points found in this drawing')
        listip = []
    
    #print('inspection points: ', listip)
    
    for i in listip:
        coordip.append(int(i))
    
    numboxes = len(coordip)/4
    # print('Detections: ', int(numboxes))
    
    i = 0
    down = 0
    up = 4
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    
    
    while i < numboxes:
        
        #get box coordinates
        draw = []
        draw = coordip[down:up]
        x1 = draw[0]
        y1 = draw[1]
        x2 = draw[2]
        y2 = draw[3]
        
        #crop the box
        img = cv2.imread(imagepath)
        crop_img = img[y1:y2, x1:x2]
        #cv2.imshow("cropped", crop_img)
        #cv2.waitKey(0)
        # Add connected components section
        
        custom_config = r'-c tessedit_char_whitelist=|ABCDEFGHIJKLMNOPQRSTUVWXYZlb0123456789.- --psm 6'
        text = pytesseract.image_to_string(crop_img, config=custom_config)
        
        pos = 0
        cont = 0
        gstring = [] #get string
        
        # convert the pytesseract text to a list to remove last two characters
        for element in range(0, len(text)-2):
            gstring.append(text[element])
        
        #convert the list we got into a string again
        string = listToString(gstring)
         
        #loop the string to look for the '-' and get the location of the pipe spec
        for element in range(len(string)):
            if cont == 1:
                break
            if string[element] == '\n':
                cont = cont + 1
            pos = pos + 1
        
        sliced1 = string[pos-4:pos-1]
    
        if sliced1 in dictg:
            dictg[sliced1].append(x1)
            dictg[sliced1].append(y1)
            dictg[sliced1].append(x2)
            dictg[sliced1].append(y2)
        
        else:
            dictg[sliced1] = [x1, y1, x2, y2]
        
        sliced2 = string[pos:pos+3]
        
        if sliced2 in dictg:
            dictg[sliced2].append(x1)
            dictg[sliced2].append(y1)
            dictg[sliced2].append(x2)
            dictg[sliced2].append(y2)
        
        else:
            dictg[sliced2] = [x1, y1, x2, y2]
        down = down+4
        up = up + 4
        i = i+1
    #print (dictg)
    return dictg

ps = 'model/yolov5/runs/detect/pipe_specs/'
ip = 'model/yolov5/runs/detect/ins_points/'
img = 'model/yolov5/data/images/'

def get_pathps():
    pipe_specs = []
    for filename in os.listdir(ps):
        f = os.path.join(ps, filename)
        pipe_specs.append(f)
    return pipe_specs

def get_pathip():
    i_points = []
    for filename in os.listdir(ip):
        f = os.path.join(ip, filename)
        i_points.append(f)
    return i_points

def get_pathimg():
    img_path = []
    for filename in os.listdir(img):
        f = os.path.join(img, filename)
        img_path.append(f)
    return img_path

def get_string():
    nom = []
    for filename in os.listdir(img):
        f = filename[-7:-4]
        nom.append(f)
    return nom

nom = get_string()
ps_path = get_pathps()
ip_path = get_pathip()
image_path = get_pathimg()

#print(nom)
#print('pipe specs: ', pspath)    
#print('inspection points: ' , ippath)
#print('image path: ', imagepath)
#print(len(ps_path))
#print(len(ip_path))
cont = (len(image_path))
i = 0

while i<cont:
    imagepath = image_path[i]
    pspath = ps_path[i]
    ippath = ip_path[i]
    dictg = draw_boxes(ippath, pspath, imagepath)
    #print (dictg)
    #save json file 
    with open(nom[i] +'.json', 'w') as fp:
        json.dump(dictg, fp)
    i = i+1 