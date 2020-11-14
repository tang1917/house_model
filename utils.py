import cv2
import numpy as np
from copy import copy
import os
from deleteSimilarLine import slashSingleWall,horizontalSingleWall,columnSingleWall

def cvShow(img):
    cv2.namedWindow('img',0)
    cv2.imshow('img',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def white2black(img):
    img_c = copy(img)
    h,w = img_c.shape
    for i in range(h):
        for j in range(w):
            if img_c[i][j] >100:
                img_c[i][j] = 0
            else:
                img_c[i][j] = 255
    return img_c

def bebinary(path):
    img = cv2.imread(path)
    img_blur = cv2.GaussianBlur(img,(3,3),1)
    img_hsv = cv2.cvtColor(img_blur,cv2.COLOR_BGR2HSV)
    lowBlack = np.array([0,0,0])
    upBlack = np.array([180,255,46])
    imgBinary = cv2.inRange(img_hsv,lowBlack,upBlack)
    return imgBinary

 
def wallShow(thinwall,boldwall,windowwall,furniturewall,img_bgr):
    for line in boldwall:
        x1,y1,x2,y2 = line
        cv2.line(img_bgr,(x1,y1),(x2,y2),(0,0,255),2)
    for line in thinwall:
        x1,y1,x2,y2 = line
        cv2.line(img_bgr,(x1,y1),(x2,y2),(255,0,255),2)
    for line in windowwall:
        x1,y1,x2,y2 = line
        cv2.line(img_bgr,(x1,y1),(x2,y2),(0,255,255),2)
    for name,line in furniturewall.items():
        for line_1 in line:
            x1,y1,x2,y2 = line_1
        cv2.line(img_bgr,(x1,y1),(x2,y1),(0,255,0),2)
        cv2.line(img_bgr,(x1,y1),(x1,y2),(0,255,0),2)
        cv2.line(img_bgr,(x2,y2),(x1,y2),(0,255,0),2)
        cv2.line(img_bgr,(x2,y2),(x2,y1),(0,255,0),2)

    return img_bgr

'''
#only wall
def wallShow(thinwall,boldwall,img_bgr):
    for line in boldwall:
        x1,y1,x2,y2 = line
        cv2.line(img_bgr,(x1,y1),(x2,y2),(0,0,255),2)
    for line in thinwall:
        x1,y1,x2,y2 = line
        cv2.line(img_bgr,(x1,y1),(x2,y2),(255,0,255),2)
    return img_bgr
'''
def recard(thin_wall,bold_wall,windowDoor,furniturewall,filename,rate):
    if not os.path.exists(filename):
        os.system(r'touch {}'.format(filename))
    
    with open(filename,'w') as f:
        f.write('x1,y1,x2,y2\n')
        f.write('\nbearing_wall:\n')
    with open(filename,'a') as f:
        for line in bold_wall:
            x1,y1,x2,y2 = [int(k*rate) for k in line]
            f.write('\t')
            f.write(str((x1,y1,x2,y2)))
            f.write('\n')
        f.write('\n\n\nnot_bearing_wall:\n')
        for line in thin_wall:
            x1,y1,x2,y2 = [int(k*rate) for k in line]
            f.write('\t')
            f.write(str((x1,y1,x2,y2)))
            f.write('\n')
        f.write('\n\n\nwindow-door:\n')
        for line in windowDoor:
            x1,y1,x2,y2 = [int(k*rate) for k in line]
            f.write('\t')
            f.write(str((x1,y1,x2,y2)))
            f.write('\n')
        #f.write('\n\n\nfurniture:\n')
        for name,lines in furniturewall.items():
            for line in lines:
                f.write(name)
                f.write(':\n')
                x1,y1,x2,y2 = [int(k*rate) for k in line]
                f.write('\t')
                f.write(str((x1,y1,x2,y2)))
                f.write('\n')            

def singleWall(thin_wall,bold_wall,th):
    column_wall = []
    horizontal_wall = []
    slash_wall = []
    thin_single_wall = []
    bold_single_wall = []
    #非承重墙
    for line in thin_wall:
        x1,y1,x2,y2 = line
        if x1 == x2:
            column_wall.append(line)
        elif y1 == y2:
            horizontal_wall.append(line)
        else:
            slash_wall.append(line)
    if len(column_wall)>0:
        column_single_wall =  columnSingleWall(column_wall,th)
        thin_single_wall.extend(column_single_wall)
    if len(horizontal_wall)>0:
        horizontal_single_wall = horizontalSingleWall(horizontal_wall,th)
        thin_single_wall.extend(horizontal_single_wall)
    
    thin_single_wall.extend(slash_wall)
    

    #承重墙
    column_wall = []
    horizontal_wall = []
    slash_wall = []
    
    for line in bold_wall:
        x1,y1,x2,y2 = line
        if x1 == x2:
            column_wall.append(line)
        elif y1 == y2:
            horizontal_wall.append(line)
        else:
            slash_wall.append(line)
    if len(column_wall)>0:
        column_single_wall =  columnSingleWall(column_wall,th)
        bold_single_wall.extend(column_single_wall)
    if len(horizontal_wall)>0:
        horizontal_single_wall = horizontalSingleWall(horizontal_wall,th)
        bold_single_wall.extend(horizontal_single_wall)
   
    bold_single_wall.extend(slash_wall)    
    
    return thin_single_wall,bold_single_wall








    
