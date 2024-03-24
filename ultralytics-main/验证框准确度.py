# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 04:10:25 2023

@author: thejun
"""

import cv2 as cv
import os
# i=272
# for j in range(1,1290):
# # if i==272:
# # img=cv.imread(r'E:\pythonCode\ultralytics-main\data\images\train\ frame_0100.jpg',0)
#     # path=r'E:/pythonCode/ultralytics-main/data/images/train/frame_'+str(i).zfill(4)+'.jpg'
#     # path=r'E:/AllMyFiles/MyFiles/人工智能/昇腾数据集/举手、趴桌、站立、玩手机/pcb1/images/pcb1__'+str(i).zfill(4)+'.jpg'
#     path=r'lj22/images/frame_'+str(j).zfill(4)+'.jpg'
    
#     # "x": 36.71875,
#     #         "y": 12.708333333333318,
#     #         "width": 11.718750000000014,
#     #         "height": 8.125000000000025,
#     #         "rotation": 0,
#     #         "frame": 272,
#     #         "enabled": true,
#     #         "time": 18.133333333333333
    
#     # pathl=r'E:/pythonCode/ultralytics-main/data/labels/train/frame_'+str(i).zfill(4)+'.txt'
#     pathl=r'E:/AllMyFiles/MyFiles/人工智能/昇腾数据集/举手、趴桌、站立、玩手机/lj22/labels/frame_'+str(j).zfill(4)+'.txt'
#     img=cv.imread(path)
#     # if img==None:
#     #     continue
#     # with open(r'E:\pythonCode\ultralytics-main\data\labels\train\frame_0100.txt') as f:
#     try:
#         with open(pathl) as f:
        
#         # while (t=f.readline()):
#         #     a=a+t
#             a=f.readlines()
#         # a=f.readline()
#         # a=f.readline()
#         # a=f.readline()
#         # a=f.readline()
#         # a=f.readline()
#         # a=f.readline()
#         # a=f.readline()
#     except:
#         continue
#     try:
#         h,w=img.shape[:2]
#     except:
#         continue
#     for i in a:
#         if i=='\n':
#             continue
#         m=i.split(' ')
#         m[1]=float(m[1])
#         m[2]=float(m[2])
#         m[3]=float(m[3])
#         m[4]=float(m[4])
#         cv.rectangle(img, (int(w*(m[1]-m[3]/2)),int(h*(m[2]-m[4]/2))),(int(w*(m[1]+m[3]/2)),int(h*(m[2]+m[4]/2))),(0,0,255),3)
#     cv.imwrite('jj2/frame_'+str(j)+'.jpg',img)
    # a=a.split(' ')
    # print(img.shape)
    # h,w=img.shape
    # a[1]=float(a[1])
    # a[2]=float(a[2])
    # a[3]=float(a[3])
    # a[4]=float(a[4])
    # print(img.shape)
    # cv.rectangle(img, (int(w*(a[1]-a[3]/2)),int(h*(a[2]-a[4]/2))),(int(w*(a[1]+a[3]/2)),int(h*(a[2]+a[4]/2))),(0,0,0),3)
    # # img2=img.resize(640,640,refcheck=False)
    
    # # cv.rectangle(img, (150,260),(150,110)  , (255,255,0),3)
    # cv.imshow(str(i), img)
    
# for j in range(1,1290):
# if i==272:
# img=cv.imread(r'E:\pythonCode\ultralytics-main\data\images\train\ frame_0100.jpg',0)
    # path=r'E:/pythonCode/ultralytics-main/data/images/train/frame_'+str(i).zfill(4)+'.jpg'
    # path=r'E:/AllMyFiles/MyFiles/人工智能/昇腾数据集/举手、趴桌、站立、玩手机/pcb1/images/pcb1__'+str(i).zfill(4)+'.jpg'
wpath='elec3new'
for filename in os.listdir(wpath+'/imgs'):
    img=cv.imread(wpath+'/imgs'+'/'+filename)
    try:
        with open(wpath+'/labels/'+filename[:-4]+'.txt') as f:
            a=f.readlines()
    except:
        continue
    try:
        h,w=img.shape[:2]
    except:
        continue
    for i in a:
        if i=='\n':
            continue
        m=i.split(' ')
        m[1]=float(m[1])
        m[2]=float(m[2])
        m[3]=float(m[3])
        m[4]=float(m[4])
        cv.rectangle(img, (int(w*(m[1]-m[3]/2)),int(h*(m[2]-m[4]/2))),(int(w*(m[1]+m[3]/2)),int(h*(m[2]+m[4]/2))),(0,0,255),3)
    cv.imwrite('pic3/'+filename,img)