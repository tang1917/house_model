from roughline import Hough
import cv2
import numpy as np
from copy import copy


def columnWallCounter(x1,y1,x2,y2,img_binary):
    x_c = copy(x1)
    num = 0
    while img_binary[y1][x1] == 255:
        num = num + 1
        x1 = x1+1
    x1 = x_c
    while img_binary[y1][x2] == 255:
        num = num + 1
        x2 = x2-1
    x2 = x_c
    return num

def horizontalWallCounter(x1,y1,x2,y2,img_binary):
    y_c = copy(y1)
    num = 0
    while img_binary[y1][x1] == 255:
        num = num+1
        y1 = y1+1
    y1  = y_c
    while img_binary[y2][x1] == 255:
        num = num+1
        y2 = y2-1
    y2 = y_c
    return num

def slashWallCounter(x1,y1,k,b,img_binary):
 
    x_c = copy(x1)
    y_c = copy(y1)
    num = 0
    
    while img_binary[y1][x1] > 100:
      
        num = num+1
        x1 = x1-1
        y1 = int(round(k*x1+b))
      
    x1 = x_c
    y1 = y_c
    while img_binary[y1][x1] > 100:
        num = num+1
        x1 = x1+1
        y1 = int(round(k*x1+b))

    num = int(np.sqrt(num**2+(num*k)**2))
    x1 = x_c

    return num

def connect(*pw):
    '''
      输入：小段的墙
      输出：连接后的墙
      功能：将首尾有连接的小段，连成完整的大段
    '''
    length = len(pw)
    temp = []
    num = 0
    while num<=(length-2):
        if pw[num][-2:] == pw[num+1][:2]:
            pw[num+1][:2] = pw[num][:2]
        else:
            temp.append(pw[num])
        num = num+1
    #print(length)
    #print(num)
    temp.append(pw[num])
    return temp 

 


#纵向的
def columnLines(x1,y1,x2,y2,img_binary,threshold_s,threshold_b,threshold_t):

    gap = 8       #长度大于gap才认为是一段墙
    #threshold_s = 20
    #threshold_b = 10
    #threshold_t = 4
    b_state = True
    t_state = True
    s_state = True
    bold_wall_column = []
    thin_wall_column = []
    b_temp = []
    t_temp = []
    s_temp = [] 
    wall_dict = {1:thin_wall_column,2:bold_wall_column}    
    x_c = copy(x1)
    
    #找到上边界
    while img_binary[y1][x1] == 255: 
        y1 = y1 - 1
    #print('y1',y1)
    y1 = y1+1
    #找到下边界
    while img_binary[y2][x1] == 255:
        y2 = y2+1
    
    #print('x1,y1,x2,y2',x1,y1,x2,y2)
    #分类
    while y1<=y2:  
            
        num = columnWallCounter(x1,y1,x2,y2,img_binary)
        #if x1 == 324 and y2==626 and y1>610:
            #print('324',num)
            #print('s_state',s_state)
            #print('y2',y2)
        #特殊墙
        if num > threshold_s and s_state:
            #print('**(x1,y1)',x1,y1)

            s_temp.extend((x1,y1))
            s_state = not s_state

            #上一个状态
            s_num_up = columnWallCounter(x1,y1-gap,x2,y2,img_binary)
            #print(s_num_up)
            #print(x1,y1)
            if s_num_up <= threshold_t:
                s_up_state = 0  #没有墙与起点连接
            elif s_num_up<=threshold_b:
                s_up_state = 1  #与起点连接的是细墙
            elif s_num_up <= threshold_s:
                s_up_state =  2  #与起点连接的是粗墙
            else:
                s_up_state = 3 #与起点相连的是特殊墙
                '''
                i = 2
                while s_num_up(x1,y1-i*gap,x2,y2,img_binary) > threshold_s:
                    i = i+1
                    if s_num_up <= threshold_t:
                        s_up_state = 0
                    elif s_num_up<=threshold_b:
                        s_up_state = 1
                    else:
                        s_up_state =  2
                '''
                
        if (not s_state and num<=threshold_s) or (y1 == y2 and not s_state):
            #print('(x1,y1)**',x1,y1)
            s_temp.extend((x1,y1))
            #print('x1,y1',x1,y1)
            s_state = not s_state
            #print('s_temp',s_temp)
            #下一个状态
            #？？？ 
            #下一个状态
            s_num_below = columnWallCounter(x1,y1+gap,x2,y2,img_binary)
            if s_num_below <= threshold_t:  #没有墙与结束点连接
                s_below_state = 0 
            elif s_num_below <= threshold_b: #与结束点连接的是细墙
                s_below_state = 1
            elif s_num_below <= threshold_s:  #与结束点连接的是粗墙
                s_below_state = 2
            else:
                s_below_state = 3             #与结束点连接的是特殊墙


            #存储在相应类别中            
            #先找与右端相连接的墙的类型，如果是特殊墙或0再找左边的墙，直到找到粗墙细墙或0停止，若是0默认为细墙
            if s_below_state == 0 or s_below_state == 3:
                i = 1   
                while s_num_up > threshold_s:                
                    i = i+1
                    s_num_up = columnWallCounter(x1,y1+i*gap,x2,y2)
                if s_num_up > threshold_b:
                    wall_dict[2].append(s_temp)
                    s_temp = []
                elif s_num_up >threshold_t:
                    wall_dict[1].append(s_temp)
                    s_temp = []
                else:
                    wall_dict[1].append(s_temp)
                    s_temp=[]
            else:
                wall_dict[s_below_state].append(s_temp)
                s_temp = []
        #粗墙
        if num<=threshold_s and num > threshold_b and b_state:
            b_temp.extend((x1,y1))
            b_state = False
            b_count = 1   #长度计数器
            '''
            #判断上下连接部分的状态
            b_num_up = columnWallCounter(x1,y1-gap,x2,y2,img_binary)
            if b_num_up > threshold_s:
                b_up_state = 3
            elif b_num_up >threshold_b:
                b_up_state = 2
            elif b_num_up >threshold_t:
                b_num_up = 1
            else b_num_up = 0
            '''

        if not b_state and not (num<=threshold_s and num > threshold_b) or (y1 == y2 and not b_state):
            b_temp.extend((x1,y1))
            b_state = True
            #大于长度阈值
            if b_count > gap:
                wall_dict[2].append(b_temp)
                b_temp = []
            #小于长度阈值
            else:
                #向下搜索找其类别，遇到特殊墙或者零，则选择不断向上搜索,遇到符合的类别或0停下，如果遇到0停下，默认为细墙
                b_below_num = columnWallCounter(x1,y1+gap,x2,y2,img_binary)
                if b_below_num <= threshold_s and b_below_num > threshold_b:
                    wall_dict[2].append(b_temp)
                    b_temp = []
                elif b_below_num <= threshold_b and b_below_num > threshold_t:
                    wall_dict[1].append(b_temp)
                    b_temp = []
                else:
                    b_up_num = columnWallCounter(x1,y1-gap,x2,y2,img_binary)
                    i = 1
                    while b_up_num > threshold_s:
                        i = i+1
                        b_up_num = columnWallCounter(x1,y1-i*gap,x2,y2,img_binary)
                    if b_up_num > threshold_b:
                        wall_dict[2].append(b_temp)
                        b_temp = []
                    elif b_up_num >threshold_t:
                        wall_dict[1].append(b_temp)
                        b_temp = []
                    else:
                        wall_dict[2].append(b_temp)
                        b_temp = []              

        #计算长度
        if not b_state and num<=threshold_s and num > threshold_b:
            b_count = b_count + 1

        #细墙
        if num <= threshold_b and num>threshold_t and t_state:
            t_temp.extend((x1,y1))
            t_state = False
            t_count = 1
        if not (num <= threshold_b and num>threshold_t) and not t_state or (y1 == y2 and not t_state):
            t_temp.extend((x1,y1))
            t_state = True
            if t_count > gap:
                wall_dict[1].append(t_temp)
                t_temp = []
            else:                                           
                #向下搜索找其类别，遇到特殊墙或者零，则选择不断向上搜索,遇到符合的类别或0停下，如果遇到0停下，默认为细墙
                t_below_num = columnWallCounter(x1,y1+gap,x2,y2,img_binary)
                if t_below_num <= threshold_s and t_below_num > threshold_b:
                    wall_dict[2].append(t_temp)
                    t_temp = []
                elif t_below_num <= threshold_b and t_below_num > threshold_t:
                    wall_dict[1].append(t_temp)
                    t_temp = []
                else:
                    t_up_num = columnWallCounter(x1,y1-gap,x2,y2,img_binary)
                    i = 1
                    while t_up_num > threshold_s:
                        i = i+1
                        t_up_num = columnWallCounter(x1,y1-i*gap,x2,y2,img_binary)
                    if t_up_num > threshold_b:
                        wall_dict[2].append(t_temp)
                        t_temp = []
                    elif t_up_num >threshold_t:
                        wall_dict[1].append(t_temp)
                        t_temp = []
                    else:
                        wall_dict[1].append(t_temp)
                        t_temp = []

        if num <= threshold_b and num>threshold_t and not t_state:
            t_count = t_count+1

        y1 = y1+1   
    
    return wall_dict[1],wall_dict[2]

#横向的
def horizontalLines(x1,y1,x2,y2,img_binary,threshold_s,threshold_b,threshold_t):
    gap = 8   #长度大于gap才认为是一段墙
    #threshold_s = 20
    #threshold_b = 10
    #threshold_t = 4
    b_state = True
    t_state = True
    s_state = True
    bold_wall_horizontal = []
    thin_wall_horizontal = []
    b_temp = []
    t_temp = []
    s_temp = []
    wall_dict = {1:thin_wall_horizontal,2:bold_wall_horizontal}
    
    y_c = copy(y1)
    #找到左边界
    while img_binary[y1][x1] == 255:
        x1 = x1-1
    x1 = x1+1
    #找到右边界
    while img_binary[y1][x2] == 255:
        x2 = x2+1
    
    
    while x1<=x2:
        num = horizontalWallCounter(x1,y1,x2,y2,img_binary)
        #特殊墙
        if num >threshold_s and s_state:
            s_temp.extend((x1,y1))
            s_state = not s_state
            
            #上一个状态
            s_num_up = horizontalWallCounter(x1-gap,y1,x2,y2,img_binary)
            if s_num_up <= threshold_t:
                s_up_state = 0 #没有墙与起点连接
            elif s_num_up <= threshold_b:
                s_up_state = 1      #与起点相连的是细墙
            elif s_num_up <= threshold_s:
                s_up_state = 2       #与起点相连的是粗墙
            else:
                s_up_state = 3        #与起点相连的是特殊墙
        if not s_state and num<=threshold_s or (x1 == x2 and not s_state):
            s_temp.extend((x1,y1))
            s_state = not s_state
            #print('s_temp',s_temp)
            
            #下一个状态
            s_num_below = horizontalWallCounter(x1+gap,y1,x2,y2,img_binary)
            if s_num_below <= threshold_t:  #没有墙与结束点连接
                s_below_state = 0 
            elif s_num_below <= threshold_b: #与结束点连接的是细墙
                s_below_state = 1
            elif s_num_below <= threshold_s:  #与结束点连接的是粗墙
                s_below_state = 2
            else:
                s_below_state = 3             #与结束点连接的是特殊墙
                
            #存储在相应类别中            
            #先找与右端相连接的墙的类型，如果是特殊墙或0再找左边的墙，直到找到粗墙细墙或0停止，若是0默认为细墙
            if s_below_state == 0 or s_below_state == 3:
                i = 1   
                while s_num_up > threshold_s:                
                    i = i+1
                    s_num_up = horizontalWallCounter(x1-i*gap,y1,x2,y2)
                if s_num_up > threshold_b:
                    wall_dict[2].append(s_temp)
                    s_temp = []
                elif s_num_up >threshold_t:
                    wall_dict[1].append(s_temp)
                    s_temp = []
                else:
                    wall_dict[1].append(s_temp)
                    s_temp=[]
            else:
                wall_dict[s_below_state].append(s_temp)
                s_temp = []
        #粗墙
        if num<=threshold_s and num>threshold_b and b_state:
            b_temp.extend((x1,y1))
            b_state = False
            b_count = 1   #长度记数器
        if not b_state and not (num<=threshold_s and num>threshold_b) or (x1 == x2 and not b_state):
            b_temp.extend((x1,y1))
            b_state = True
            #长度大于阈值
            if b_count > gap:
                wall_dict[2].append(b_temp)
                b_temp = []
            #长度小于阈值
            else:
            #先找与右端相连接的墙的类型，如果是特殊墙或0再找左边的墙，直到找到粗墙细墙或0停止，若是0默认为细墙
                #print('**',b_temp)
                b_below_num = horizontalWallCounter(x1+gap,y1,x2,y2,img_binary)
                if b_below_num <= threshold_s and b_below_num>threshold_b:
                    wall_dict[2].append(b_temp)
                    b_temp = []
                elif b_below_num <= threshold_b and b_below_num >threshold_t:
                    wall_dict[1].append(b_temp)
                    b_temp = []
                else:
                    b_up_num = horizontalWallCounter(x1-gap,y1,x2,y2,img_binary)
                    i = 1
                    while b_up_num >threshold_s:
                        i = i+1
                        b_up_num = horizontalWallCounter(x1-i*gap,y1,x2,y2,img_binary)
                    if b_up_num > threshold_b:
                        wall_dict[2].append(b_temp)
                        b_temp = []
                    elif b_up_num >threshold_t:
                        wall_dict[1].append(b_temp)
                        b_temp = []
                    else:
                        wall_dict[2].append(b_temp)
                        b_temp = []
        #计算长度
        if not b_state and num<= threshold_s and num>threshold_b:
            b_count = b_count+1
        
        #细墙
        if num<=threshold_b and num>threshold_t and t_state:
            t_temp.extend((x1,y1))
            t_state = False
            t_count = 1
        if not (num<=threshold_b and num>threshold_t) and not t_state or (x1==x2 and not t_state):
            t_temp.extend((x1,y1))
            t_state = True
            if t_count >gap:
                wall_dict[1].append(t_temp)
                t_temp = []
            else:

                #向下搜索找其类别，遇到特殊墙或者零，则选择不断向上搜索,遇到符合的类别或0停下，如果遇到0停下，默认为细墙
                t_below_num = horizontalWallCounter(x1+gap,y1,x2,y2,img_binary)
                if t_below_num <= threshold_s and t_below_num > threshold_b:
                    wall_dict[2].append(t_temp)
                    t_temp = []
                elif t_below_num <= threshold_b and t_below_num > threshold_t:
                    wall_dict[1].append(t_temp)
                    t_temp = []
                else:
                    t_up_num = horizontalWallCounter(x1-gap,y1,x2,y2,img_binary)
                    i = 1
                    while t_up_num > threshold_s:
                        i = i+1
                        t_up_num = horizontalWallCounter(x1,y1-i*gap,x2,y2,img_binary)
                    if t_up_num > threshold_b:
                        wall_dict[2].append(t_temp)
                        t_temp = []
                    elif t_up_num >threshold_t:
                        wall_dict[1].append(t_temp)
                        t_temp = []
                    else:
                        wall_dict[1].append(t_temp)
                        t_temp = []
        if num <= threshold_b and num>threshold_t and not t_state:
            t_count = t_count+1

        
        x1 = x1+1
    
    return wall_dict[1],wall_dict[2]
#斜墙
def slashLines(x1,y1,x2,y2,img_binary,threshold_s,threshold_b,threshold_t):
    #直线方向的斜率
    m = (y1-y2)/(x1-x2)
    #与直线垂直方向的斜率
    k = -1/m
    b_k = y1 - k*x1   
    b_m = y1 - m*x1
    gap = 2       #长度大于gap才认为是一段墙

    b_state = True
    t_state = True
    s_state = True
    bold_wall_column = []
    thin_wall_column = []
    b_temp = []
    t_temp = []
    s_temp = [] 
    wall_dict = {1:thin_wall_column,2:bold_wall_column}    
    #??
    y1 = int(round(m*x1+b_m))
    #x_c = copy(x1)
    
    #找到左边界
    while img_binary[y1][x1] == 255:
        x1 = x1-1
        y1 = int(round(m*x1+b_m))
    x1 = x1+1
    #找到右边界
    while img_binary[y2][x2] == 255:
        x2 = x2+1
        y2 = int(round(m*x2+b_m))
    #print('(x1,y1,x2,y2)',x1,y1,x2,y2)
    
    while x1<=x2:
        num= slashWallCounter(x1,y1,k,b_k,img_binary)
        #特殊墙
        if num >threshold_s and s_state:
            s_temp.extend((x1,y1))
            s_state = not s_state
            
            #上一个状态,没有包括y超出边界的情况
            x1_update = x1 - gap
            y1_update = int(round(m*x1_update+b_m))
            b_update = y1_update - x1_update*k
            s_num_up = slashWallCounter(x1_update,y1_update,k,b_update,img_binary)
            if s_num_up <= threshold_t:
                s_up_state = 0 #没有墙与起点连接
            elif s_num_up <= threshold_b:
                s_up_state = 1      #与起点相连的是细墙
            elif s_num_up <= threshold_s:
                s_up_state = 2       #与起点相连的是粗墙
            else:
                s_up_state = 3        #与起点相连的是特殊墙
        if not s_state and num<=threshold_s or (x1==x2 and not s_state):
            s_temp.extend((x1,y1))
            s_state = not s_state
            #print('s_temp',s_temp)
            
            #下一个状态
            x1_update = x1 + gap
            y1_update = int(round(m*x1_update+b_m))
            b_update = y1_update - x1_update*k            
            s_num_below = slashWallCounter(x1_update,y1_update,k,b_update,img_binary)
            if s_num_below <= threshold_t:  #没有墙与结束点连接
                s_below_state = 0 
            elif s_num_below <= threshold_b: #与结束点连接的是细墙
                s_below_state = 1
            elif s_num_below <= threshold_s:  #与结束点连接的是粗墙
                s_below_state = 2
            else:
                s_below_state = 3             #与结束点连接的是特殊墙
                
            #存储在相应类别中            
            #先找与右端相连接的墙的类型，如果是特殊墙或0再找左边的墙，直到找到粗墙细墙或0停止，若是0默认为细墙
            if s_below_state == 0 or s_below_state == 3:
                i = 1   
                while s_num_up > threshold_s:                
                    i = i+1
                    x1_update = x1-i*gap
                    y1_update = int(round(m*x1_update +b_m))
                    b_update = y1_update - x1_update*k
                    s_num_up = slashWallCounter(x1_update,y1_update,k,b_update,img_binary)
                  
                if s_num_up > threshold_b:
                    wall_dict[2].append(s_temp)
                    s_temp = []
                elif s_num_up >threshold_t:
                    wall_dict[1].append(s_temp)
                    s_temp = []
                else:
             
                    wall_dict[1].append(s_temp)
                    s_temp=[]
            else:
                wall_dict[s_below_state].append(s_temp)
                s_temp = []
        #粗墙
        if num<=threshold_s and num>threshold_b and b_state:
            b_temp.extend((x1,y1))
            b_state = False
            b_count = 1   #长度记数器
        if not b_state and not (num<=threshold_s and num>threshold_b) or (x1==x2 and not b_state):
            b_temp.extend((x1,y1))
            b_state = True
            #长度大于阈值
            if b_count > gap:
                wall_dict[2].append(b_temp)
                b_temp = []
            #长度小于阈值
            else:
            #先找与右端相连接的墙的类型，如果是特殊墙或0再找左边的墙，直到找到粗墙细墙或0停止，若是0默认为细墙
                #print('**',b_temp)
                x1_update = x1+gap
                y1_update = int(round(m*x1_update+b_m))
                b_update = y1_update - k*x1_update
                b_below_num = slashWallCounter(x1_update,y1_update,k,b_update,img_binary)
                if b_below_num <= threshold_s and b_below_num>threshold_b:
                    wall_dict[2].append(b_temp)
                    b_temp = []
                elif b_below_num <= threshold_b and b_below_num >threshold_t:
                    wall_dict[1].append(b_temp)
                    b_temp = []
                else:
                    x1_update = x1-gap
                    y1_update = int(round(m*(x1-gap)+b_m))
                    b_update = y1_update - k*x1_update
                    b_up_num = slashWallCounter(x1_update,y1_update,k,b_update,img_binary)
                    i = 1
                    while b_up_num >threshold_s:
                        i = i+1
                        x1_update = x1 - i*gap
                        y1_update = int(round(m*(x1-i*gap)+b_m))
                        b_update = y1_update - k*x1_update
                        b_up_num = slashWallCounter(x1_update,y1_update,k,b_update,img_binary)
                    if b_up_num > threshold_b:
                        wall_dict[2].append(b_temp)
                        b_temp = []
                    elif b_up_num >threshold_t:
                        wall_dict[1].append(b_temp)
                        b_temp = []
                    else:
                        wall_dict[2].append(b_temp)
                        b_temp = []
        #计算长度
        if not b_state and num<= threshold_s and num>threshold_b:
            b_count = b_count+1


        #细墙
        if num<=threshold_b and num>threshold_t and t_state:
            t_temp.extend((x1,y1))
            t_state = False
            t_count = 1
        if not (num<=threshold_b and num>threshold_t) and not t_state or (x1==x2 and not t_state):
            t_temp.extend((x1,y1))
            t_state = True
            if t_count >gap:
                wall_dict[1].append(t_temp)
                t_temp = []
            else:

                #向下搜索找其类别，遇到特殊墙或者零，则选择不断向上搜索,遇到符合的类别或0停下，如果遇到0停下，默认为细墙
                x1_update = x1+gap
                y1_update = int(round(m*(x1+gap)+b_m))
                b_update= y1_update-k*x1_update
                t_below_num = slashWallCounter(x1_update,y1_update,k,b_update,img_binary)
                if t_below_num <= threshold_s and t_below_num > threshold_b:
                    wall_dict[2].append(t_temp)
                    t_temp = []
                elif t_below_num <= threshold_b and t_below_num > threshold_t:
                    wall_dict[1].append(t_temp)
                    t_temp = []
                else:
                    x1_update = x1-gap
                    y1_update = int(round(m*(x1-gap)+b_m))
                    b_update= y1_update-k*x1_update
                    t_up_num= slashWallCounter(x1_update,y1_update,k,b_update,img_binary)
                    i = 1
                    while t_up_num > threshold_s:
                        i = i+1
                        x1_update = x1-i*gap
                        y1_update = int(round(m*(x1-i*gap)+b_m))
                        b_update = y1_update - k*x1_update
                        t_up_num = slashWallCounter(x1_update,y1_update,k,b_update,img_binary)
                    if t_up_num > threshold_b:
                        wall_dict[2].append(t_temp)
                        t_temp = []
                    elif t_up_num >threshold_t:
                        wall_dict[1].append(t_temp)
                        t_temp = []
                    else:
                        wall_dict[1].append(t_temp)
                        t_temp = []
        if num <= threshold_b and num>threshold_t and not t_state:
            t_count = t_count+1

        x1 = x1+1
        y1 = int(round(m*x1+b_m))
        b_k = y1 - k*x1
  
    return wall_dict[1],wall_dict[2]