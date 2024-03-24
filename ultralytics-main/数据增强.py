import cv2 as cv
import math
import numpy as np

def getRotImg(img, angle):
    rows, cols = img.shape[:2]
    sin = math.sin
    cos = math.cos
    radians = math.radians
    heightNew = int(cols * abs(sin(radians(angle))) + rows * abs(cos(radians(angle))))
    widthNew = int(rows * abs(sin(radians(angle))) + cols * abs(cos(radians(angle))))
    center = ((cols) / 2, (rows) / 2)

    M = cv.getRotationMatrix2D(center, angle, 1)  # 获得旋转矩阵

    M[0, 2] += (widthNew - cols) / 2
    M[1, 2] += (heightNew - rows) / 2

    dst = cv.warpAffine(img, M, (widthNew, heightNew))  # 仿射变换旋转图像
    return dst

def getFour_rotate(mask,angle):
    rows,cols = mask.shape[:2]
    # w=xywh[2]
    # h=xywh[3]
    # cols=w*cols
    # rows=h*rows
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
    return [[0,0],[widthNew,heightNew]]
    # return[d1,d2,d3,d4]

def getValid(lines):
    txt=[]
    for i in lines:
        if i!='\n':
            txt.append(i)
    return txt

def getFour_None(txt):
    four=[]
    for i in txt:
        a=i.split(' ')
        four.append([float(a[1]),float(a[2]),float(a[3]),float(a[4])])
    return four

def getxy_rotate(xy,angle,h,w,new_h,new_w):
    angle_rad = math.radians(angle)
    minx=50000
    miny = 50000
    for i in xy:
        zx,zy=i
        x=int(zx-w/2)
        y=int(zy-h/2)
        # 计算旋转后的点坐标
        new_x = x * math.cos(angle_rad) - y * math.sin(angle_rad)+new_w/2
        new_y = x * math.sin(angle_rad) + y * math.cos(angle_rad)+new_h/2
        minx=min(minx,new_x)
        miny=min(miny,new_y)

    return minx,miny

import os
import random
def elecforce():
    m=0
    for filename in os.listdir('elec3/images'):
        for c in range(360):
            angle=random.random()*360
            img=cv.imread('elec3/images/'+filename)
            img2=getRotImg(img,angle)

            with open('elec3/labels/'+filename[:-4]+'.txt',encoding='utf-8') as f:
                alllines=f.readlines()

            txt=getValid(alllines)
            # print(txt)
            bq=txt[0][0]
            four = getFour_None(txt)
            # print(four)
            h,w=img.shape[:2]
            new_h,new_w=img2.shape[:2]
            newwrite=''
            for i in four:
                zx=int((i[0]-i[2]/2)*w)
                zy=int((i[1]-i[3]/2)*h)
                yx=int((i[0]+i[2]/2)*w)
                yy=int((i[1]+i[3]/2)*h)
                mask = img[zy:yy,zx:yx]
                d=getFour_rotate(mask,angle)
                d = np.array(d)
                new_x,new_y=getxy_rotate([[zx,zy],[zx,yy],[yx,zy],[yx,yy]], -angle, h, w,new_h,new_w)
                d[:, :1] = d[:, :1] + new_x
                d[:, 1:2] = d[:, 1:2] + new_y
                # cv.rectangle(img2,d[0],d[1],(0,0,255),5)
                new_cent=(d[0]+d[1])/2
                new_w1=d[1][0]-d[0][0]
                new_h1=d[1][1]-d[0][1]
                newwrite=newwrite+bq+' '+str(new_cent[0]/new_w)+' '+str(new_cent[1]/new_h)+' '+str(new_w1/new_w)+' '+str(new_h1/new_h)+'\n'
            alpha=random.random()+0.5
            img2=cv.convertScaleAbs(img2,alpha=alpha,beta=0)
            cv.imwrite('elec3new/images/elec3force_'+str(m)+'.jpg',img2)
            with open('elec3new/labels/elec3force_'+str(m)+'.txt','w',encoding='utf-8') as f:
                f.write(newwrite)
            m+=1


        # print(newwrite)
    # for filename in os.listdir('pcb3/imgs'):
    #
    #     # angle = random.random() * 360
    #     img = cv.imread('pcb3/imgs/' + filename)
    #     img2 = getRotImg(img, angle)
    #
    #     with open('labels1/' + filename[:-4] + '.txt', encoding='utf-8') as f:
    #         alllines = f.readlines()
    #
    #     txt = getValid(alllines)
    #     print(txt)
    #     bq = txt[0][0]
    #     four = getFour_None(txt)
    #     print(four)
    #     h, w = img.shape[:2]
    #     new_h, new_w = img2.shape[:2]
    #     newwrite = ''
    #     for i in four:
    #         zx = int((i[0] - i[2] / 2) * w)
    #         zy = int((i[1] - i[3] / 2) * h)
    #         yx = int((i[0] + i[2] / 2) * w)
    #         yy = int((i[1] + i[3] / 2) * h)
    #         mask = img[zy:yy, zx:yx]
    #         d = getFour_rotate(mask, angle)
    #         d = np.array(d)
    #         new_x, new_y = getxy_rotate([[zx, zy], [zx, yy], [yx, zy], [yx, yy]], -angle, h, w, new_h, new_w)
    #         d[:, :1] = d[:, :1] + new_x
    #         d[:, 1:2] = d[:, 1:2] + new_y
    #         # cv.rectangle(img2,d[0],d[1],(0,0,255),5)
    #         new_cent = (d[0] + d[1]) / 2
    #         new_w1 = d[1][0] - d[0][0]
    #         new_h1 = d[1][1] - d[0][1]
    #     #     newwrite = newwrite + bq + ' ' + str(new_cent[0] / new_w) + ' ' + str(new_cent[1] / new_h) + ' ' + str(
    #     #         new_w1 / new_w) + ' ' + str(new_h1 / new_h) + '\n'
    #     alpha = random.random() + 0.5
    #     img2 = cv.convertScaleAbs(img, alpha=alpha, beta=0)
    #     cv.imwrite('img2/' + filename, img2)
    #     # with open('labels2/' + filename[:-4] + '.txt', 'w', encoding='utf-8') as f:
    #     #     f.write(newwrite)


def pcbforce():
    # for filename in os.listdir('xiao'):
    #     img=cv.imread('xiao/'+filename)
    #     img=cv.pyrDown(img)
    #     img = cv.pyrDown(img)
    #     cv.imwrite('xiao2/'+filename,img)
    #     print(img.shape)

    i=0
    for filename in os.listdir('pcb3/images'):
    #
        for c in range(200):
            # angle=random.random()*360
            img=cv.imread('pcb3/images/'+filename)
        #     img2=getRotImg(img,angle)
        #
        #     with open('elec2/labels/'+filename[:-4]+'.txt',encoding='utf-8') as f:
        #         alllines=f.readlines()
        #
        #     txt=getValid(alllines)
        #     # print(txt)
        #     bq=txt[0][0]
        #     four = getFour_None(txt)
        #     # print(four)
        #     h,w=img.shape[:2]
        #     new_h,new_w=img2.shape[:2]
        #     newwrite=''
        #     for i in four:
        #         zx=int((i[0]-i[2]/2)*w)
        #         zy=int((i[1]-i[3]/2)*h)
        #         yx=int((i[0]+i[2]/2)*w)
        #         yy=int((i[1]+i[3]/2)*h)
        #         mask = img[zy:yy,zx:yx]
        #         d=getFour_rotate(mask,angle)
        #         d = np.array(d)
        #         new_x,new_y=getxy_rotate([[zx,zy],[zx,yy],[yx,zy],[yx,yy]], -angle, h, w,new_h,new_w)
        #         d[:, :1] = d[:, :1] + new_x
        #         d[:, 1:2] = d[:, 1:2] + new_y
        #         # cv.rectangle(img2,d[0],d[1],(0,0,255),5)
        #         new_cent=(d[0]+d[1])/2
        #         new_w1=d[1][0]-d[0][0]
        #         new_h1=d[1][1]-d[0][1]
        #         newwrite=newwrite+bq+' '+str(new_cent[0]/new_w)+' '+str(new_cent[1]/new_h)+' '+str(new_w1/new_w)+' '+str(new_h1/new_h)+'\n'
        #     alpha=random.random()+0.5
        #     img2=cv.convertScaleAbs(img2,alpha=alpha,beta=0)
        #     cv.imwrite('elec2new/images/elec2force_'+str(i)+'.jpg',img2)
        #     with open('elec2new/labels/elec2force_'+str(i)+'.txt','w',encoding='utf-8') as f:
        #         f.write(newwrite)
            # print(newwrite)
        # i=0
        # for filename in os.listdir('pcb3/imgs'):
        #
        #     # angle = random.random() * 360
        #     img = cv.imread('pcb3/imgs/' + filename)
        #     # img2 = getRotImg(img, angle)
        #
        #     # with open('labels1/' + filename[:-4] + '.txt', encoding='utf-8') as f:
        #     #     alllines = f.readlines()
        #
        #     # txt = getValid(alllines)
        #     # print(txt)
        #     # bq = txt[0][0]
        #     # four = getFour_None(txt)
        #     # print(four)
        #     # h, w = img.shape[:2]
        #     # new_h, new_w = img2.shape[:2]
        #     # newwrite = ''
        #     # for i in four:
        #     #     zx = int((i[0] - i[2] / 2) * w)
        #     #     zy = int((i[1] - i[3] / 2) * h)
        #     #     yx = int((i[0] + i[2] / 2) * w)
        #     #     yy = int((i[1] + i[3] / 2) * h)
        #     #     mask = img[zy:yy, zx:yx]
        #     #     d = getFour_rotate(mask, angle)
        #     #     d = np.array(d)
        #     #     new_x, new_y = getxy_rotate([[zx, zy], [zx, yy], [yx, zy], [yx, yy]], -angle, h, w, new_h, new_w)
        #     #     d[:, :1] = d[:, :1] + new_x
        #     #     d[:, 1:2] = d[:, 1:2] + new_y
        #     #     # cv.rectangle(img2,d[0],d[1],(0,0,255),5)
        #     #     new_cent = (d[0] + d[1]) / 2
        #     #     new_w1 = d[1][0] - d[0][0]
        #     #     new_h1 = d[1][1] - d[0][1]
        #     #     newwrite = newwrite + bq + ' ' + str(new_cent[0] / new_w) + ' ' + str(new_cent[1] / new_h) + ' ' + str(
        #     #         new_w1 / new_w) + ' ' + str(new_h1 / new_h) + '\n'
        #     for c in range(230):
            alpha = random.random() + 0.5
            img2 = cv.convertScaleAbs(img, alpha=alpha, beta=0)
            cv.imwrite('pcb3new/images/pcb3force_' + str(i) + '.jpg', img2)
            with open('pcb3/labels/' + filename[:-4] + '.txt', encoding='utf-8') as f:
                t = f.read()
            # with open('pcb3new/labels/pcb3_' + str(i) + '.txt', 'r', encoding='utf-8') as f:
            #     pass
            with open('pcb3new/labels/pcb3force_' + str(i) + '.txt', 'w', encoding='utf-8') as f:
                f.write(t)
            i += 1

pcbforce()

        # with open('labels2/' + filename[:-4] + '.txt', 'w', encoding='utf-8') as f:
        #     f.write(newwrite)
