# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from __future__ import division
from PIL import Image
from os import listdir
from os.path import isfile, join
from facepp import API, File
import pickle

MAX = 500
INIT = False
API_KEY = 'dau1SUsWiztCOodnFOfdM_ydjEzUiZG_'
API_SECRET = 'SL950sSRkiHrZYTOB8qwIoUpZdGxaEZF'
faceset_token = u'44fda4fcfd6c473869dc0e077e2805e3'
path = 'faces\\'

srv = locals().get('SERVER')
api = API(API_KEY, API_SECRET, srv = srv)

#if adding all the pictures in the directory for the first time#
if INIT:
    pics = listdir(path)
    toks = []
    for img in pics:
        i = Image.open(path + img)
        width,height = i.size
        if (width > MAX or height > MAX):
            resize_ratio = min(MAX/width, MAX/height)
            i = i.resize((int(width * resize_ratio), int(height * resize_ratio)), Image.ANTIALIAS)
        res = api.detect(image_file = File(path+img))
        if res['faces']:
            toks += [res['faces'][k]['face_token'] for k in range(len(res['faces']))]

    ft = str(toks[0])
    log = []
    for i in range(1,len(toks)):
        ft += ',' + str(toks[i])
        if i%4 ==0:
            log += api.faceset.addface(face_tokens = ft, faceset_token = faceset_token)
            ft= ""
    res= api.faceset.addface(face_tokens = ft, faceset_token = u'44fda4fcfd6c473869dc0e077e2805e3')
    
#Code for each new face#
#new_face = 'untitled9.jpg'
#temp = api.detect(image_file = File(path+new_face))
#if temp['faces']:
#    new_face_token = temp['faces'][0]['face_token']
#    w = api.search(face_token = new_face_token, faceset_token = faceset_token)
#    who = w['results']['face_token'], w['results']['confidence']
    
    
#sample hashtable for labeling results received from the api.search() function#  
id_dictionary = {'bc0d0542ba5d41b81c5b14eeda7dd596': "ET", 
                 '12f490bf7350969a11577cf0b9cd05ab': 'coworker'
                 }

#Applying the above code to all the files in the new directory#
#returns the name of the file: The face token it matches, and its confidence#
path = 'faces1\\'
new_faces = listdir(path)
result_dict = {}
for f in new_faces:
    temp = api.detect(image_file = File(path+f))
    if temp['faces']:
        new_face_token = temp['faces'][0]['face_token']
        w = api.search(face_token = new_face_token, faceset_token = faceset_token)
        who = w['results'][0]['face_token'], w['results'][0]['confidence']
        result_dict[f] = who
    else:
        print('unidentified face')