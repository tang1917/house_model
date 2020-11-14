import numpy as np
import cv2
from utils import *
from skeleton import Xihua
from width import defineWidth
from roughline import Hough
from detectwall import *
from copy import copy
import os
from decidewindow import selectedWindow,deleteSimilarWindow
from dxf_tran_test import draw_dxf
import time
from align import align
from dxf_class import DXF
from setclass import property

from crossline import deleteShortCross
import sys 
sys.path.append(r'.\others')
from link_wall import findwindow
from furniture import test_pic

def cvShow(img):
    cv2.namedWindow('img',0)
    cv2.imshow('img',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
class Wall:
    def __init__(self,path):
        self.path = path
        self.img_white_binary = bebinary(self.path)
        self.img_black_binary = white2black(self.img_white_binary)
        self.img_skeleton = Xihua(self.img_black_binary)
        self.x_lines,self.y_lines,self.slash_lines = Hough(self.img_skeleton)
        self.threshold_s,self.threshold_b,self.threshold_t,self.rate = defineWidth(self.img_skeleton,self.img_white_binary,self.x_lines,self.y_lines,self.slash_lines)

        self.bold_wall = []
        self.thin_wall = []
    #确定墙体类型
    def classwall(self):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
        self.img_white_binary = cv2.morphologyEx(self.img_white_binary, cv2.MORPH_CLOSE, kernel,iterations=1) 
        #print('x_lines=',x_lines)
        for line in self.x_lines:
            x1,y1,x2,y2 = line
            thin_lines,bold_lines = horizontalLines(x1,y1,x2,y2,self.img_white_binary,
                                                self.threshold_s,self.threshold_b,self.threshold_t)
            #print('x_thin_lines=',thin_lines)
            if len(bold_lines) > 0:
                bold_horizontal_wall = connect(*bold_lines)
               

                for m in bold_horizontal_wall:
                    self.bold_wall.append(m)
            if len(thin_lines) > 0:
                thin_horizontal_wall = connect(*thin_lines)

                for n in thin_horizontal_wall:

                    self.thin_wall.append(n)

        for line in self.y_lines:
            x1,y1,x2,y2 =  line
            thin_lines,bold_lines = columnLines(x1,y1,x2,y2,self.img_white_binary,
                                                    self.threshold_s,self.threshold_b,self.threshold_t)
            if len(bold_lines)>0:
                bold_column_wall = connect(*bold_lines)

                for m in bold_column_wall:

                    self.bold_wall.append(m)
            if len(thin_lines)>0:
                thin_column_wall = connect(*thin_lines)
                
                for n in thin_column_wall:

                    self.thin_wall.append(n)


        for line in self.slash_lines:
            x1,y1,x2,y2 = line
            thin_lines,bold_lines = slashLines(x1,y1,x2,y2,self.img_white_binary,
                                                    self.threshold_s,self.threshold_b,self.threshold_t)
            if len(bold_lines)>0:
                bold_slash_wall = connect(*bold_lines)
                for m in bold_slash_wall:
                    self.bold_wall.append(m)
            if len(thin_lines)>0:
                thin_slash_wall = connect(*thin_lines)
                for n in thin_slash_wall:
                    self.thin_wall.append(n)   
        return self.bold_wall,self.thin_wall
    def deleteCrossShortLine(self,bold_wall_temp,thin_wall_temp):
        #去除交叉点
        len_bold = len(bold_wall_temp)
        wall_s = bold_wall_temp
        wall_s.extend(thin_wall_temp)
        len_wall_s = len(wall_s)

        bold_wall=[]
        thin_wall=[]
        for i in range(len_wall_s-1):
            for j in range(i+1,len_wall_s):
                line1 = wall_s[i]
                line2 = wall_s[j]
                line1,line2= deleteShortCross(line1,line2,self.threshold_b)
            if i < len_bold:
                bold_wall.append(line1)
            else:
                thin_wall.append(line1)
        if j==(len_wall_s-1) and j>=len_bold:
            thin_wall.append(line2)
        return thin_wall,bold_wall
def house(root):
    for filename in os.listdir(root):
        if '150' in filename:

            print('***{} start'.format(filename))
            time_start = time.time()
            filepath = os.path.join(root,filename)
            savepath = os.path.join(r'.\result',filename)
            txtname = os.path.splitext(filename)[0]+'.txt'
            txtpath = os.path.join(r'.\location',txtname)
            dxfname = os.path.splitext(filename)[0]+'.dxf'
            dxfpath = os.path.join(r'.\dxf',dxfname)

            wall = Wall(filepath)
            #img = copy(wall.img_white_binary)
            
            
            img_bgr = cv2.imread(filepath)
            
            ans_bold_wall,ans_thin_wall = wall.classwall()
            #bold_wall_temp,thin_wall_temp = align(bold_wall_temp,thin_wall_temp)
            #ans_thin_wall,ans_bold_wall = wall.deleteCrossShortLine(ans_bold_wall,ans_thin_wall)
            
            #ans_thin_wall,ans_bold_wall =  singleWall(ans_thin_wall,ans_bold_wall,0) 

            ans_wall = copy(ans_bold_wall)  
            ans_wall.extend(ans_thin_wall) #所有最终确定的墙
            
            window_wall = findwindow(ans_thin_wall,ans_bold_wall,filepath) #候选的窗户和门
            ans_thin_wall,ans_bold_wall =  singleWall(ans_thin_wall,ans_bold_wall,0)
            for i,window in enumerate(window_wall):
                win_x_sorted = sorted([window[0],window[2]])
                if window[0]!=win_x_sorted[0]:
                    window_wall[i]=window[-2:]+window[:2]
                else:
                    if window[0]==window[2]:
                        win_y_sorted = sorted([window[1],window[3]])
                        if window[1] != win_y_sorted[0]:
                            window_wall[i] = window[-2:]+window[:2]
                        else:
                            window_wall[i] = window
                    else:
                        window_wall[i] = window
            #print('window_wall=',window_wall)
            #print('ans_wall=',ans_wall)
            deleted_window = []
            for window in window_wall:
                for wall_line in ans_wall:
                    #print('wall_line=',wall_line)
                    deleted_window = selectedWindow(window,wall_line,wall.threshold_s,wall.threshold_s,deleted_window)
            true_window = []
            for window in window_wall:
                if window not in deleted_window and (window not in true_window):
                    true_window.append(window)     #筛选后的窗户和门b
        
            ans_window = deleteSimilarWindow(true_window,wall.threshold_s)
            #对齐
            ans_thin_wall,ans_bold_wall,ans_window = property(ans_thin_wall,ans_bold_wall,ans_window)
            ans_thin_wall,ans_bold_wall,ans_window = align(ans_thin_wall,ans_bold_wall,ans_window,wall.threshold_s)

            ans_furniture = test_pic(img_bgr)
            result = wallShow(ans_thin_wall,ans_bold_wall,ans_window,ans_furniture,img_bgr)   
            #recard(ans_thin_wall,ans_bold_wall,ans_window,ans_furniture,txtpath,wall.rate)
            recard(ans_thin_wall,ans_bold_wall,ans_window,ans_furniture,txtpath,wall.rate)
            #print('wall.state=',wall.rate)
            #draw_dxf(txtpath,dxfpath)
            dxf = DXF(src_dxf=r'.\template\wifi_dxf.dxf',txt_path = txtpath,save_path=dxfpath)
            dxf.draw_dxf()
            cv2.imwrite(savepath,result)
            time_end = time.time()
            time_cost = time_end-time_start
            print('***{} done in {} seconds'.format(filename,time_cost))
        
       

if __name__ == "__main__":
    root = r'.\picture'
    house(root)

        



            
            










        






