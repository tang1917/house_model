import numpy as np
import cv2
from deleteSimilarLine import judgeXOverlap,judgeYOverlap

def judgeLineType(line1):
    #判断直线属于哪种类型
    #水平直线？
    if line1[3] - line1[1] == 0:
        horizontal_line_state = True
    else:
        horizontal_line_state = False
    #竖直直线？
    if line1[2] - line1[0] == 0:
        column_line_state = True
    else:
        column_line_state = False
    #斜线？
    if line1[2] - line1[0] != 0 and line1[3] - line1[1] !=0:
        slash_line_state = True
      
    else:
        slash_line_state = False
 
    return horizontal_line_state,column_line_state,slash_line_state
def pointDistance(p1,p2):
    d = np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
    return d
def changeLine(segment1,segment2,p,th):
    if pointDistance(segment1[:2],p) <th:
        segment1[:2] = p
    if pointDistance(segment1[2:4],p)<th:
        segment1[2:4] = p
    if pointDistance(segment2[:2],p) <th:
        segment2[:2] = p
    if pointDistance(segment2[2:4],p) <th:
        segment2[2:4] = p
    return segment1,segment2

def deleteShortCross(line1,line2,th):
    h1_state,c1_state,s1_state = judgeLineType(line1)
    h2_state,c2_state,s2_state = judgeLineType(line2)
    '''
    te = line1[:4]
    te.sort()
    x1,y1,x2,y2 = te
    me = line2[:4]
    me.sort()
    m1,n1,m2,n2 = me
    '''
    x1,y1,x2,y2 = line1[:4]
    m1,n1,m2,n2 = line2[:4]
    buffer = 20

    if x2 < x1:
        print('********意外')
    if c1_state and y1>y2:
        print('y1>y2')
    if c2_state and n1>n2:
        print('n1>n2')
    
    #水平水平
    if h1_state and h2_state and y1 == n1:
        not_overlap,x_sort = judgeXOverlap(line1[:4],line2[:4])
        #不重合
        if not_overlap and x_sort[2]-x_sort[1]<3*buffer:
            #判断左右位置
            if line1[2] == x_sort[1]:
                line1[2] = x_sort[2]
            else:
                line1[0] = x_sort[1]
    if c1_state and c2_state and x1==m1:
        not_overlap,y_sort = judgeYOverlap(line1[:4],line2[:4])
        #不重合
        if not_overlap and y_sort[2]-y_sort[1]<3*buffer:
            #判断上下位置
            if line1[3] == y_sort[1]:
                line1[3]=y_sort[2]
            else:
                line1[1] = y_sort[1]

   
    #水平竖直
    if h1_state and c2_state:
        if m1 >= x1-buffer and m1 <= x2+buffer and n1<=y1+buffer and n2>=y1-buffer :
            p = [m1,y1]
            line1,line2 = changeLine(line1,line2,p,th)
 
                
    #竖直水平
    if c1_state and h2_state:
        if x2<=m2+buffer and x1>= m1-buffer and n1>=y1-buffer and n1<=y2+buffer:
            p = [x1,n1]
            line1,line2 = changeLine(line1,line2,p,th)
    #斜线水平
    if s1_state and h2_state:
        k = (y2-y1)/(x2-x1)
        b = y1-k*x1
        x_p = int(round((n1-b)/k))
        if (x_p <= x2 and x_p >= x1) and (x_p <= m2 and x_p >= m1):
            p = [x_p,n1]
            line1,line2 = changeLine(line1,line2,p,th)
    #斜线竖直
    if s1_state and c2_state:
        k = (y2-y1)/(x2-x1)
        b = y1-k*x1
        y_p = int(round(m1*k +b))
        y_small,y_big = sorted([y1,y2])
        n_small,n_big = sorted([n1,n2])
        if (y_p>=y_small and y_p<=y_big) and (y_p>=n_small and y_p <= n_big):
            p = [m1,y_p]
            line1,line2 = changeLine(line1,line2,p,th)
    #水平斜线
    if h1_state and s2_state:
        k = (n2-n1)/(m2-m1)
        b = n1 - k*m1
        x_p = int(round((y1-b)/k))
        if (x_p <= x2 and x_p >= x1) and (x_p <= m2 and x_p >= m1):
            p = [x_p,y1]
            line1,line2 = changeLine(line1,line2,p,th)
    #竖直斜线
    if c1_state and s2_state:
        k = (n2-n1)/(m2-m1)
        b = n1 - k*m1
        y_p=int(round(k*x1+b))
        y_small,y_big = sorted([y1,y2])
        n_small,n_big = sorted([n1,n2])
        if (y_p>=y_small and y_p<=y_big) and (y_p>=n_small and y_p <= n_big):
            p = [m1,y_p]
            line1,line2 = changeLine(line1,line2,p,th)
    #斜线斜线
    if s1_state and s2_state:
        k_1 = (y2-y1)/(x2-x1)
        b_1 = y1-k_1*x1
        k_2 = (n2-n1)/(m2-m1)
        b_2 = n1 - k_2*m1

        x_p = int(round((b_2-b_1)/(k_1-k_2+0.0000001)))
        y_p = int(round(k_1*x_p+b_1))
        y_small,y_big = sorted([y1,y2])
        n_small,n_big = sorted([n1,n2])
        y_cross_state = (y_p>=y_small and y_p<=y_big) and (y_p>=n_small and y_p <= n_big)
        x_cross_state = (x_p <= x2 and x_p >= x1) and (x_p <= m2 and x_p >= m1)
        if x_cross_state and y_cross_state:
            p = [x_p,y_p]
            line1,line2 = changeLine(line1,line2,p,th)
    return line1,line2

def removeCrossShortLine(thin,bold,window,th):
    '''
    输入承重墙，非承重墙，窗户，交叉线的最小阈值
    '''
    thin_collect = []
    bold_collect = []
    window_collect = []
    all_lines = thin
    all_lines.extend(bold)
    all_lines.extend(window)
    len_lines = len(all_lines)
    for i in range (len_lines-1):
        for j in range(i+1,len_lines):
            line1 = all_lines[i]
            line2 = all_lines[j]
            all_lines[i],all_lines[j] = deleteShortCross(line1,line2,th)
        if all_lines[i][-1] == 0:
            #thin_collect.append(all_lines[i][:4])
            thin_collect.append(all_lines[i])
        elif all_lines[i][-1]==1:
            #bold_collect.append(all_lines[i][:4])
            bold_collect.append(all_lines[i])
        else:
            window_collect.append(all_lines[i])
            #window_collect.append(all_lines[i][:4])
            
    line_last = all_lines[-1]
    if line_last[-1] ==0:
        #thin_collect.append(line_last[:4])
        thin_collect.append(line_last)
    elif line_last[-1] == 1:
        #bold_collect.append(line_last[:4])
        bold_collect.append(line_last)
    else:
        #window_collect.append(line_last[:4])
        window_collect.append(line_last)  
       
    return thin_collect,bold_collect,window_collect

if __name__=='__main__':
    line1 = [1,20,50,20]
    line2 = [4,10,4,70]
    line1,line2 = deleteShortCross(line1,line2,14)
    print(line1,line2)


        








