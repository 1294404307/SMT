# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 17:06:55 2023

@author: thejun
"""

import os

path1='images/train'
path11='labels/train'
i=1
for filename in os.listdir(path1):
    os.rename(path1+'/'+filename, path1+'/'+str(i).zfill(6)+'.jpg')
    os.rename(path11+'/'+filename[:-4]+'.txt',path11+'/'+str(i).zfill(6)+'.txt')
    i+=1
    
path2='images/valid'
path22='labels/valid'

for filename in os.listdir(path2):
    os.rename(path2+'/'+filename, path2+'/'+str(i).zfill(6)+'.jpg')
    os.rename(path22+'/'+filename[:-4]+'.txt',path22+'/'+str(i).zfill(6)+'.txt')
    i+=1

path3='images/test'
path33='labels/test'

for filename in os.listdir(path33):
    os.rename(path33+'/'+filename, path33+'/'+str(i).zfill(6)+'.txt')
    os.rename(path3+'/'+filename[:-4]+'.jpg',path3+'/'+str(i).zfill(6)+'.jpg')
    i+=1