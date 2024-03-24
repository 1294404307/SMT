# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 13:21:53 2023

@author: 12944
"""
import cv2
import cv2 as cv
import numpy as np
import math
from ultralytics import YOLO
model=YOLO(r'D:\runs\weight\new3\best60epoch.pt')
import time

def getRotImg(img,angle):
    rows,cols = img.shape[:2]
    sin = math.sin
    cos = math.cos 
    radians = math.radians
    heightNew=int(cols*abs(sin(radians(angle)))+rows*abs(cos(radians(angle))))
    widthNew=int(rows*abs(sin(radians(angle)))+cols*abs(cos(radians(angle))))
    center = ((cols)/2,(rows)/2)
     
    M = cv.getRotationMatrix2D(center,angle,1)#获得旋转矩阵

    M[0,2] +=(widthNew-cols)/2  
    M[1,2] +=(heightNew-rows)/2 
     
    dst  = cv.warpAffine(img,M,(widthNew,heightNew))#仿射变换旋转图像
    return dst

def getFour(mask,angle):
    rows,cols = mask.shape[:2]
    sin = math.sin
    cos = math.cos 
    radians = math.radians
    h1 = int(cols*abs(sin(radians(angle))))
    h2 = int(rows*abs(cos(radians(angle))))
    w1 = int(cols*abs(cos(radians(angle))))
    w2 = int(rows*abs(sin(radians(angle))))

    heightNew = h1+h2
    widthNew = w1+w2
    if 0<=angle<90 or 180<=angle<270:
        d1=[w1,0]
        d2=[0,h1]
        d3=[w2,heightNew]
        d4=[widthNew,h2]
    elif 90<=angle<180 or 270<=angle<360:
        d1=[w2,0]
        d2=[0,h2]
        d3=[w1,heightNew]
        d4=[widthNew,h1]
    return[d1,d2,d3,d4]


def printf(tgraph,lst,mask):
    for i in lst:
        print("宽：",i[2]-i[0],"长：",i[3]-i[1],"角度：",i[4],"max_val：",i[5])
        dingd = getFour(mask, i[4])
        dingd = np.array(dingd)
        dingd[:,:1]=dingd[:,:1]+i[0]
        dingd[:,1:2]=dingd[:,1:2]+i[1]
    
        cv.polylines(tgraph,[dingd],True,(0,255,255),2)

    # cv.imshow('w',tgraph)
def printf_append(tgraph,lst,mask,sumlst):
    tlst=[]
    for i in lst:
        print("宽：", i[2] - i[0], "长：", i[3] - i[1], "角度：", i[4], "max_val：", i[5])
        dingd2 = getFour(mask, i[4])
        dingd = np.array(dingd2)
        dingd[:, :1] = dingd[:, :1] + i[0]
        dingd[:, 1:2] = dingd[:, 1:2] + i[1]

        cv.polylines(tgraph, [dingd], True, (0, 255, 255), 2)
        tlst.append((min(dingd[0][0],dingd[1][0],dingd[2][0],dingd[3][0]),
                     min(dingd[0][1],dingd[1][1],dingd[2][1],dingd[3][1]),
                     max(dingd[0][0],dingd[1][0],dingd[2][0],dingd[3][0]),
                     max(dingd[0][1],dingd[1][1],dingd[2][1],dingd[3][1]),i[4],i[5]))
    sumlst.append(tlst)
def findOneElecInElec(graph,lst,angle):
    lst2=[]
    for i in lst:
        max_val=0
        max_loc=[]
        gdrot=0
        for rot in range(0,int(angle)):
            mask=cv.imread('template/of'+i[5]+'mask.jpg')
            tplgraph=cv.imread('template/of'+i[5]+'.jpg')
            mask=getRotImg(mask,rot)
            tplgraph=getRotImg(tplgraph,rot)
            Mask = cv.bilateralFilter(mask, 9, 75, 75)
            w = int(min(i[2] + 1 + offsetNum, graph.shape[1])) - \
                int(max(0, i[0] - offsetNum))
            h = int(min(i[3] + 1 + offsetNum, graph.shape[0])) - \
                int(max(i[1] - offsetNum, 0))
            th, tw = tplgraph.shape[:2]
            if th >= h or tw >= w:
                continue
            result = cv.matchTemplate(
                graph[int(max(i[1] - offsetNum, 0)):int(min(i[3] + 1 + offsetNum, graph.shape[0])),
                int(max(0, i[0] - offsetNum)):int(min(i[2] + 1 + offsetNum, graph.shape[1]))],
                tplgraph, cv.TM_CCORR_NORMED, mask=Mask)
            mmin_val, mmax_val, mmin_loc, mmax_loc = cv.minMaxLoc(result)
            if mmax_val>max_val:
                max_val=mmax_val
                max_loc=mmax_loc
                gdrot=rot
        if max_loc==[]:
            continue
        if int(max(i[1] - offsetNum, 0)) != 0 and int(max(0, i[0] - offsetNum)) != 0:

            lst2.append(
                (int(max(max_loc[0] + i[0] - offsetNum, 0)), int(max(max_loc[1] + i[1] - offsetNum, 0)),
                 int(min(max_loc[0] + tw + i[0] - offsetNum, graph.shape[1])), int(min(max_loc[1] -
                                                                                       offsetNum + th + i[1],
                                                                                       graph.shape[0])), gdrot, (i[5])))
        elif int(max(i[1] - offsetNum, 0)) == 0 and int(max(0, i[0] - offsetNum)) != 0:
            lst2.append((int(max(max_loc[0] + i[0] - offsetNum, 0)), int(max(max_loc[1] + i[1], 0)),
                         int(min(max_loc[0] + tw + i[0] - offsetNum, graph.shape[1])), int(min(max_loc[1] +
                                                                                               th + i[1],
                                                                                               graph.shape[0])), gdrot,
                         (i[5])))
        elif int(max(i[1] - offsetNum, 0)) != 0 and int(max(0, i[0] - offsetNum)) == 0:
            lst2.append((int(max(max_loc[0] + i[0], 0)), int(max(max_loc[1] + i[1] - offsetNum, 0)),
                         int(min(max_loc[0] + tw + i[0], graph.shape[1])), int(min(max_loc[1] -
                                                                                   offsetNum + th + i[1],
                                                                                   graph.shape[0])), gdrot, (i[5])))
        else:
            lst2.append((int(max(max_loc[0] + i[0], 0)), int(max(max_loc[1] + i[1], 0)),
                         int(min(max_loc[0] + tw + i[0], graph.shape[1])), int(min(max_loc[1] +
                                                                                   th + i[1], graph.shape[0])), gdrot,
                         (i[5])))
    return lst2

def findOnePcbInPcb(graph,lst,n,offsetNum):
    lst2=[]
    for i in lst:
        mask=cv.imread('template/of'+i[5][:-1]+str(n)+'mask.jpg')
        tplgraph=cv.imread('template/of'+i[5][:-1]+str(n)+'.jpg')
        Mask = cv.bilateralFilter(mask, 9, 75, 75)
        w = int(min(i[2] + 1 + offsetNum, graph.shape[1])) - \
            int(max(0, i[0] - offsetNum))
        h = int(min(i[3] + 1 + offsetNum, graph.shape[0])) - \
            int(max(i[1] - offsetNum, 0))
        th, tw = tplgraph.shape[:2]
        if th >= h or tw >= w:
            continue
        result = cv.matchTemplate(
            graph[int(max(i[1] - offsetNum, 0)):int(min(i[3] + 1 + offsetNum, graph.shape[0])),
            int(max(0, i[0] - offsetNum)):int(min(i[2] + 1 + offsetNum, graph.shape[1]))],
            tplgraph, cv.TM_CCORR_NORMED, mask=Mask)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        print(max_val)
        if int(max(i[1] - offsetNum, 0)) != 0 and int(max(0, i[0] - offsetNum)) != 0:
            lst2.append(
                (int(max(max_loc[0] + i[0] - offsetNum, 0)), int(max(max_loc[1] + i[1] - offsetNum, 0)),
                 int(min(max_loc[0] + tw + i[0] - offsetNum, graph.shape[1])), int(min(max_loc[1] -
                                                                                            offsetNum + th + i[1],
                                                                                            graph.shape[0])), 0,(i[5])))
        elif int(max(i[1] - offsetNum, 0)) == 0 and int(max(0, i[0] - offsetNum)) != 0:
            lst2.append((int(max(max_loc[0] + i[0] - offsetNum, 0)), int(max(max_loc[1] + i[1], 0)),
                         int(min(max_loc[0] + tw + i[0] - offsetNum, graph.shape[1])), int(min(max_loc[1] +
                                                                                                    th + i[1],
                                                                                                    graph.shape[0])), 0,(i[5])))
        elif int(max(i[1] - offsetNum, 0)) != 0 and int(max(0, i[0] - offsetNum)) == 0:
            lst2.append((int(max(max_loc[0] + i[0], 0)), int(max(max_loc[1] + i[1] - offsetNum, 0)),
                         int(min(max_loc[0] + tw + i[0], graph.shape[1])), int(min(max_loc[1] -
                                                                                   offsetNum + th + i[1],
                                                                                   graph.shape[0])), 0, (i[5])))
        else:
            lst2.append((int(max(max_loc[0] + i[0], 0)), int(max(max_loc[1] + i[1], 0)),
                         int(min(max_loc[0] + tw + i[0], graph.shape[1])), int(min(max_loc[1] +
                                                                                   th + i[1], graph.shape[0])), 0,(i[5])))
    return lst2

def xuanzepcb(lst,vis):
    lst2=[]
    if vis==1:
        for i in lst:
            if i[2]-i[0]>75:
                lst2.append(i)
    elif vis==0:
        for i in lst:
            if i[2]-i[0]<75 and i[2]-i[0]>45:
                lst2.append(i)
    return lst2



stand = 0.2
standncc = 0.9
offsetNum = 10
offsetNumpcb=5
count=2
base = 3

allname=['elec1','pcb1','elec2','elec3','pcb3']

def match2():
    result = model.predict(source=r'needdetect2', show=False, save=False)


def match():
    elesumlst = []
    pcbsumlst = []
    t1=time.time()
    result=model.predict(source=r'needdetect',show=False,save=True)
    t3=time.time()
    print("t3-t1:",t3-t1)
    elelst=[]
    ele2lst=[]
    ele3lst=[]
    pcblst=[]
    pcb3lst=[]
    for i in range(2):
        for (xyxy,conf,iname) in zip(result[i].boxes.xyxy.int(),result[i].boxes.conf,result[i].boxes.cls.int()):
            if float(conf)<=0.4:
                continue
            if allname[int(iname)][:5]=='elec1':
                elelst.append([int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3]), 0, allname[int(iname)]])
            elif allname[int(iname)][:5]=='elec2':
                ele2lst.append([int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3]), 0, allname[int(iname)]])
            elif allname[int(iname)][:5]=='elec3':
                ele3lst.append([int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3]), 0, allname[int(iname)]])
            elif allname[int(iname)][:4]=='pcb3':
                pcb3lst.append([int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3]), 0, allname[int(iname)]])
            else:
                pcblst.append([int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3]), 0, allname[int(iname)]])
    ele1sumlst=[]
    ele2sumlst=[]
    ele3sumlst=[]
    pcb1sumlst=[]
    pcb2sumlst=[]
    pcb3sumlst=[]
    pcb1sumlst = xuanzepcb(pcblst, 1)
    pcb2sumlst = xuanzepcb(pcblst, 0)
    graph=cv.imread('needdetect/elec1.jpg')
    ele1sumlst=findOneElecInElec(graph,elelst,181)
    ele2sumlst = findOneElecInElec(graph, ele2lst,360)
    # ele3sumlst = findOneElecInElec(graph,ele3lst,180)
    graph2 = cv.imread('needdetect/pcb1.jpg')
    pcb1sumlst=findOnePcbInPcb(graph2,pcb1sumlst,1,offsetNumpcb)

    pcb2sumlst=findOnePcbInPcb(graph2,pcb2sumlst,2,offsetNumpcb)
    pcb3sumlst=findOnePcbInPcb(graph2,pcb3lst,3,offsetNumpcb)


    t2=time.time()
    print("t2-t3",t2-t3)
    mask = cv.imread('template/ofelec1mask.jpg')
    # printf(graph, ele1sumlst, mask)
    printf_append(graph, ele1sumlst, mask, elesumlst)
    mask = cv.imread('template/ofelec2mask.jpg')
    # printf(graph, ele2sumlst, mask)
    printf_append(graph, ele2sumlst, mask, elesumlst)
    # mask = cv.imread('template/ofelec3mask.jpg')
    # # printf(graph, ele3sumlst, mask)
    # printf_append(graph, ele3sumlst, mask, elesumlst)
    cv.imwrite('jianceele.jpg',graph)
    mask = cv.imread('template/ofpcb1mask.jpg')
    printf(graph2, pcb1sumlst, mask)
    mask = cv.imread('template/ofpcb2mask.jpg')
    printf(graph2, pcb2sumlst, mask)
    mask = cv.imread('template/ofpcb3mask.jpg')
    printf(graph2, pcb3sumlst, mask)
    cv.imwrite('jiancepcb.jpg',graph2)
    # elesumlst.append(ele1sumlst)
    # elesumlst.append(ele2sumlst)
    # elesumlst.append(ele3sumlst)
    pcbsumlst.append(pcb1sumlst)
    pcbsumlst.append(pcb2sumlst)
    pcbsumlst.append(pcb3sumlst)

    return elesumlst,pcbsumlst,graph2,graph
    # return sumlst
    #
    print(sumlst)
    # mask = cv.imread('template/ofelec1mask.jpg')
    # printf(graph,sumlst,mask)
    # cv.waitKey(0)



if __name__ == '__main__':
    match()
    # name=["dz"]
    # graph=cv.imread('template/elec1.jpg')
    # lst1,lst2=match()
    # for i in lst:
    #     print(i)
        # print()