import numpy as np 
import cv2
from crossline import judgeLineType
from deleteSimilarLine import judgeXOverlap,judgeYOverlap

def selectedWindow(wline,wall,th,length,deleted_window):
    
    wline_h,wline_c,wline_s = judgeLineType(wline)
    wall_h,wall_c,wall_s = judgeLineType(wall)
    x1,y1,x2,y2 = wall
    m1,n1,m2,n2 = wline
    #print('th = ',th)
    #print('length = ',length)
    #都是竖线
    if wall_c and wline_c:
        #小于一定长度的线舍去
        if abs(n2-n1)<length and wline not in deleted_window:
            deleted_window.append(wline)
        if abs(x1-m1)<= th:
            overlap_state,y_overlap_list = judgeYOverlap(wline,wall)
            
            #overlap_state 没有重合为true有重合为False
            if not overlap_state:
                #print('wline=',wline)
                #print('wall=',wall)
                y_overlap_length = y_overlap_list[2]-y_overlap_list[1]
                #print('Y_OVERLAP_LENGTH=',y_overlap_length)
                if y_overlap_length>length and wline not in deleted_window:
                    deleted_window.append(wline)
    #都是横线
    if wall_h and wline_h:
        if abs(m2-m1)<length and wline not in deleted_window:
            deleted_window.append(wline)
        if abs(y1-n1)<=th:
            overlap_state,x_overlap_list = judgeXOverlap(wline,wall)
            if not overlap_state:
                x_overlap_length = x_overlap_list[2]-x_overlap_list[1]
                if x_overlap_length>length and wline not in deleted_window:
                    deleted_window.append(wline)
    #都是斜线
    if wall_s and wline_s:
        if np.sqrt((m1-m2)**2 + (n1-n2)**2)<2*length and wline not in deleted_window:
            deleted_window.append(wline)
        k_wall = (y2-y1)/(x2-x1)
        k_window = (n2-n1)/(m2-m1)
        if abs(k_wall-k_window)<=np.tan(np.pi/3):
            win_x_sorted = sorted([wline[0],wline[2]])
            if wline[0]==win_x_sorted[0]:
                win_sorted = wline
            else:
                win_sorted = wline[-2:]+wline[:2]
            #print('win_sorted=',win_sorted)
            m1,n1,m2,n2 = win_sorted
            if (np.sqrt((x1-m1)**2+(y1-n1)**2)<2*length or np.sqrt((x2-m2)**2+(y2-n2)**2)<2*length) and wline not in deleted_window:
                deleted_window.append(wline)
    #斜线横线
   
    if wall_h and wline_s:
        k_wline = (n2-n1)/(m2-m1)
        win_x_sorted = sorted([wline[0],wline[2]])
        if wline[0]==win_x_sorted[0]:
            win_sorted = wline
        else:
            win_sorted = wline[-2:]+wline[:2] 
        m1,n1,m2,n2 = win_sorted  
        if (np.sqrt((x1-m1)**2+(y1-n1)**2)<2*length or np.sqrt((x2-m2)**2+(y2-n2)**2)<2*length) and wline not in deleted_window and abs(k_wline) < np.tan(np.pi/4):   
            deleted_window.append(wline)
    
    #if wall_h and wline_s:

    #斜线竖线
    if wall_c and wline_s:
        k_wline = (n2-n1)/(m2-m1)
        #窗户按纵坐标排序
        win_y_sorted = sorted([wline[1],wline[3]])
        if wline[1]==win_y_sorted[0]:
            win_sorted = wline
        else:
            win_sorted = wline[-2:]+wline[:2]
              
        m1,n1,m2,n2 = win_sorted
        if (np.sqrt((x1-m1)**2+(y1-n1)**2)<2*length or np.sqrt((x2-m2)**2+(y2-n2)**2)<2*length) and wline not in deleted_window and abs(k_wline) > np.tan(np.pi/4):   
            deleted_window.append(wline)

    return deleted_window
def deleteSimilarWindow(windows,th):
    distance = 5
    for i,window in enumerate(windows):
        win_x_sorted = sorted([window[0],window[2]])
        if window[0]!=win_x_sorted[0]:
            windows[i]=window[-2:]+window[:2]
        else:
            if window[0]==window[2]:
                win_y_sorted = sorted([window[1],window[3]])
                if window[1] != win_y_sorted[0]:
                    windows[i] = window[-2:]+window[:2]
                else:
                    windows[i] = window
            else:
                windows[i] = window
    #print(windows)
    length = len(windows)
    deleted_window = []
    for i in range(length-1):
        for j in range(i+1,length):
            win_1 = windows[i]
            win_2 = windows[j]
            x1,y1,x2,y2 = win_1
            m1,n1,m2,n2 = win_2
            win_1_h,win_1_c,win_1_s = judgeLineType(win_1)
            
            win_2_h,win_2_c,win_2_s = judgeLineType(win_2)
            
                
            #都是横线
            if win_1_h and win_2_h:
                
                #距离是否小于阈值
                if abs(n1-y1)<th:
                    #判断是否重叠
                    overlap_state,x_overlap_list = judgeXOverlap(win_1,win_2)
                    if win_1 == [128, 676, 148, 676] and win_2 == [128, 676, 148, 676]:
                        print('***')
                        print(overlap_state,x_overlap_list)
                    if not overlap_state:   #重叠
                        if x_overlap_list[2]-x_overlap_list[1]>distance:
                            len1 = win_1[2]-win_1[0]
                            len2 = win_2[2]-win_2[0]
                            #删去长度较短的
                            if len1<=len2 and win_1 not in deleted_window:
                                deleted_window.append(win_1)
                            if len1>len2 and win_2 not in deleted_window:
                                deleted_window.append(win_2)
            #都是竖线
            if win_1_c and win_2_c:
                #距离是否小于阈值
                if abs(x1-m1)<th:
                    #判断是否重叠
                    overlap_state,y_overlap_list = judgeYOverlap(win_1,win_2)
                    if not overlap_state: #重叠
                        if y_overlap_list[2]-y_overlap_list[1] >distance:
                            len1 = win_1[3]-win_1[1]
                            len2 = win_2[3]-win_2[1]
                            #删去长度较短的
                            if len1<=len2 and win_1 not in deleted_window:
                                deleted_window.append(win_1)
                            if len1>len2 and win_2 not in deleted_window:
                                deleted_window.append(win_2)
            #斜线竖线
            if win_1_s and win_2_c:
                overlap_state,y_overlap_list = judgeYOverlap(win_1,win_2)
                if not overlap_state:
                    if y_overlap_list[2]-y_overlap_list[1]>distance:
                        if abs(m1-x1)<th or abs(m2-x2)<th and win_1 not in deleted_window:
                            deleted_window.append(win_1)
            #斜线横线
            if win_1_s and win_2_h:
                overlap_state,x_overlap_list = judgeXOverlap(win_1,win_2)
                if not overlap_state:
                    if x_overlap_list[2]-x_overlap_list[1] > distance:
                        if abs(n1-y1)<th or abs(n2-y2)<th and win_1 not in deleted_window:
                            deleted_window.append(win_1)
            #横线斜线
            if win_1_h and win_2_s:
                overlap_state,x_overlap_list = judgeXOverlap(win_1,win_2)
                if not overlap_state:
                    if x_overlap_list[2]-x_overlap_list[1] > distance:
                        if abs(n1-y1)<th or abs(n2-y2)<th and win_2 not in deleted_window:
                            deleted_window.append(win_2)  
            #竖线斜线
            if win_1_c and win_1_s:
                overlap_state,y_overlap_list = judgeYOverlap(win_1,win_2)
                if not overlap_state:
                    if y_overlap_list[2]-y_overlap_list[1]>distance:
                        if abs(m1-x1)<th or abs(m2-x2)<th and win_2 not in deleted_window:
                            deleted_window.append(win_2)    
            #斜线斜线
            if win_1_s and win_2_s:
                k_1 = (y1-y2)/(x1-x2)
                k_2 = (n1-n2)/(m1-m2)
        
                if abs(k_1-k_2) < np.tan(np.pi/6) and (abs(x1-m1)<th or abs(x2-m2)<th):
                    len1 = np.sqrt((x1-x2)**2+(y1-y2)**2)
                    len2 = np.sqrt((m1-m2)**2+(n1-n2)**2)
                    #删去长度较短的
                    if len1<=len2 and win_1 not in deleted_window:
                        deleted_window.append(win_1)
                    if len1>len2 and win_2 not in deleted_window:
                        deleted_window.append(win_2)
    get_window = []
    for window in windows:
        if window not in deleted_window:
            get_window.append(window)
    return get_window

if __name__ == '__main__':
    x1 = [0,1,10,1]
    x2 = [2,1,5,1]
    th = 1
    length = 1
    tes = selectedWindow(x1,x2,th,length)
    #print(tes)








