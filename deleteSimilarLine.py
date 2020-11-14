
import cv2
import numpy as np


#两点之间距离
def sqrt(*num):
    if len(num) == 8:
        d1 = np.sqrt((num[0]-num[4])**2+(num[1]-num[5])**2)
        d2 = np.sqrt((num[2]-num[6])**2+(num[3]-num[7])**2)
        return d1,d2
    if len(num) == 4:
        single_d = np.sqrt((num[0]-num[2])**2+(num[1]-num[3])**2)
        return single_d


def slope(x):
    return (x[3]-x[1])/(x[2]-x[0])
def computeLength(x):
    return np.sqrt((x[3]-x[1])**2+(x[2]-x[0])**2)

#返回距离相近的集合
def set_collection(w,lineType,margin=5):  #lineType 0表示竖线，1表示横线
    sorted_w = sorted(w,key = lambda x:x[lineType])
    storage = []
    selected = []
    length = len(sorted_w)
    for i,element in enumerate(sorted_w):
        temp = []
        if element not in selected:
            temp.append(element)
            selected.append(element)
        k=i
        #判断列表中的最后一个元素
        if k==length-1:
            if sorted_w[k][lineType]-sorted_w[k-1][lineType]>margin:
                temp = []
                temp.append(sorted_w[-1])                
                storage.append(temp)

            break
        #横坐标小于一定阈值的放在一个集合中
        while sorted_w[k+1][lineType] - element[lineType] < margin and sorted_w[k+1] not in selected:
            temp.append(sorted_w[k+1])
            selected.append(sorted_w[k+1])
            element = sorted_w[k+1]
            k = k+1
            if k >= length-1:
                break
        if len(temp)>0:            
            storage.append(temp)        
    return storage



#判断两条在两个方向上是否有相交的投影
def judgeIntersect(list_1,list_2):
    '''
    输入两个列表
    输出boole值，若没有相同投影为真
    '''
    x_list = [list_1[0],list_1[2],list_2[0],list_2[2]]
    y_list = [list_1[1],list_1[3],list_2[1],list_2[3]]
    #print('y_list=',y_list)
    x_sorted = sorted(x_list)
    y_sorted = sorted(y_list)
    #print('y_sorted=',y_sorted)
    #若直线的两个端点坐标排序后仍在一起，认为是两条直线不相交
    x_case = (x_list[0] in x_sorted[:2] and x_list[1] in x_sorted[:2]) or (x_list[0] in x_sorted[-2:] and x_list[1] in x_sorted[-2:])
    #print(x_case)
    y_case = (y_list[0] in y_sorted[:2] and y_list[1] in y_sorted[:2]) or (y_list[0] in y_sorted[-2:] and y_list[1] in y_sorted[-2:])
    #print(y_case)
    case = x_case and y_case
    
    return case,x_case,y_case,x_sorted,y_sorted

#判断两条直线在x方向是是否有相交的投影
def judgeXOverlap(line_1,line_2):
    x_list = [line_1[0],line_1[2],line_2[0],line_2[2]]
    x_sorted = sorted(x_list)
    #若直线的两个端点排序后仍在一起，认为是没有重合的投影
    x_case = (x_list[0] in x_sorted[:2] and x_list[1] in x_sorted[:2]) or (x_list[0] in x_sorted[-2:] and x_list[1] in x_sorted[-2:])
    return x_case,x_sorted

def judgeYOverlap(line_1,line_2):
    y_list = [line_1[1],line_1[3],line_2[1],line_2[3]]
    y_sorted = sorted(y_list)
    #若直线的两个端点排序后仍在一起，认为是没有重合的投影
    y_case = (y_list[0] in y_sorted[:2] and y_list[1] in y_sorted[:2]) or (y_list[0] in y_sorted[-2:] and y_list[1] in y_sorted[-2:])
    return y_case,y_sorted


#删除相似斜线
def slashSingleWall(s):
    sorted_s = sorted(s,key = slope)
    
    distance = np.tan(np.pi/4)
    margin = 20
    min_length = 3
    length = len(sorted_s)
    selected_line = []
    storage = []
    single_line = []
    for i,element in enumerate(sorted_s):
        temp = []
        if element not in selected_line:
            temp.append(element)
            selected_line.append(element)
        k = i
        #判断列表中的最后一个元素
        if k == length-1:
            if abs(slope(sorted_s[k])-slope(sorted_s[k-1])) >= distance:            
                temp.append(slope(sorted_s[k]))            
            break   

        while abs(slope(element)-slope(sorted_s[k+1])) < distance and sorted_s[k+1] not in selected_line:
            temp.append(sorted_s[k+1])
            selected_line.append(sorted_s[k+1])
            element = sorted_s[k+1]
            k = k+1
            if k>=length-1:

                break
        if len(temp)>0:
            storage.append(temp)
    for gather in storage:
        delected_line = []
        length = len(gather)

        for i,line in enumerate(gather):  
            if computeLength(line)<min_length:
                delected_line.append(line)
            #直线的斜率与截距
            slope_line = slope(line)
            if abs(slope_line) < np.tan(np.pi/18):
                delected_line.append(line)
                #print('***line = ',line)
            if abs(slope_line) > np.tan(np.pi/9*4):
                delected_line.append(line)

            b_line = line[1]-slope_line*line[0]
            line_length = computeLength(line)
            k = i
            while k < length-1 and line not in delected_line :
                state,x_state,y_state,x_sorted,y_sorted = judgeIntersect(line,gather[k+1])  #判断是否有相交的投影
                if not state:
                    slope_com = slope(gather[k+1])
                    b_com = gather[k+1][1]-slope_com*gather[k+1][0]

                    #y方向投影相交，x方向投影不相交
                    if not y_state and  x_state:
                        y_middle = sum(y_sorted[1:3])/2
                        #y_middle = int(y_middle)
                        #slope_com = slope(gather[i+1])
                        #b_com = gather[i+1][1]-slope_com*gather[i+1][0]
                        x_line_middle = (y_middle-b_line)/slope_line
                        x_com_middle = (y_middle-b_com)/slope_com
                        measure = abs(x_line_middle-x_com_middle)
                        #距离小于阈值，保留长度较大的那一个
                        if measure < margin:
                            com_length = computeLength(gather[k+1])
                            if line_length<com_length:
                                break
                            else:
                                delected_line.append(gather[k+1])
                    else:
                        x_middle = sum(x_sorted[1:3])/2
                        y_line_middle = slope_line*x_middle+b_line
                        y_com_middle = slope_com*x_middle+b_com
                        measure = abs(y_line_middle-y_com_middle)
                        if measure<margin:
                            com_length = computeLength(gather[k+1])
                            if line_length<com_length:
                                break
                            else:
                                delected_line.append(gather[k+1])
                k=k+1
            if k==length-1 and i !=length-1:
                #print('line=',line)
                single_line.append(line)
            if i == length-1 and line not in delected_line:
                #print('line=',line)
                single_line.append(line)
    return single_line


#删除相似竖直线
def columnSingleWall(w,th=20):
 
    #删除相似线
    min_lenth = 8
    storage= set_collection(w,0,margin=20)
    single_line = []
    for gather in storage:
        delected_line = []
        length = len(gather)
        for i in range(length):
            line = gather[i]
            line_length = abs(line[3]-line[1])
            #小于一定长度的线删除
            if line_length <= min_lenth:
                delected_line.append(line)
            k = i
            while k < length-1 and line not in delected_line:
                y_state,y_sorted = judgeYOverlap(line,gather[k+1])
                #相交
                if (not y_state) and (y_sorted[2]-y_sorted[1]>th):
                    com_length = gather[k+1][3]-gather[k+1][1]
                    if line_length<com_length:
                        gather[k+1][1] = y_sorted[0]
                        gather[k+1][3] = y_sorted[3]
                        break
                    else:
                        #不完全重合，合并
                        if (y_sorted[2]-y_sorted[1]) < com_length:
                            line[1] = y_sorted[0]
                            line[3] = y_sorted[3]

                        delected_line.append(gather[k+1])
                k = k+1
            if k == length-1 and i != length-1:
                single_line.append(line)
            if i == length-1 and line not in delected_line:
                single_line.append(line)
        #break
    #print('single_line=',single_line)
    return single_line
                
#删除相似水平线
def horizontalSingleWall(w,th=20):
  
    #删除相似线
    min_lenth = 3
    storage= set_collection(w,1,margin=20)
    single_line = []
    for gather in storage:
        #print('gather=',gather)
        delected_line = []
        length = len(gather)
        for i in range(length):
            line = gather[i]
            line_length = abs(line[2]-line[0])
            #小于一定长度的线删除
            if line_length <= min_lenth:
                delected_line.append(line)
            k = i
            while k < length-1 and line not in delected_line:
                x_state,x_sorted = judgeXOverlap(line,gather[k+1])
                #相交
                if (not x_state) and (x_sorted[2]-x_sorted[1]>th):
                    com_length = gather[k+1][2]-gather[k+1][0]
                    if line_length<com_length:
                        gather[k+1][0]=x_sorted[0]
                        gather[k+1][2]=x_sorted[3]
                        break
                    else:
                        line[0] = x_sorted[0]
                        line[2]=  x_sorted[3]
                        delected_line.append(gather[k+1])

                k = k+1
            if k == length-1 and i != length-1:
                single_line.append(line)
            if i == length-1 and line not in delected_line:
                single_line.append(line)
        #break
        #print('single_line=',single_line)
        #print('delected=',delected_line)
    return single_line
