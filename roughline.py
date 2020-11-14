import cv2
import numpy as np
from copy import copy
from deleteSimilarLine import slashSingleWall,columnSingleWall,horizontalSingleWall

def cvShow(img): 
    cv2.namedWindow('img',0)
    cv2.imshow('img',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def transition(img):
    img_c = copy(img)
    h,w = img_c.shape
    for i in range(h):
        for j in range(w):
            if img_c[i][j] > 100:
                img_c[i][j] = 0
            else:
                img_c[i][j] = 255
    return img_c



#找图中的竖线
def columnline(img,x1,y1,x2,y2): 
    all_storage = [] #所有竖线端点的坐标
    one_storage = [] #一条竖线端点的坐标
    count = 0 #上下间隔计数器
    state = True
    count_state = False   #记数器状态关闭
    gap = 4    #上下间断不大于4认为是同一条直线
    width = 2  #直线左右相邻的两个像素存在值是255的则认为是连续的
    minLength = 10 #直线的最小长度
    while y1<y2:
        
        condition = (img[y1,x1-width:x1+width+1]==255).any() #判断是否是直线上的点
        if state and condition:
            start = y1              #起点
            one_storage.append(x1)  #直线的一个端点
            #print('y1',y1)
            one_storage.append(y1)
            state = not state
        if not state and not condition:
            count_state = True    #计数器状态打开
            count = count + 1
            if count == gap:
                count = 0          #记数器归零
                if y1 - gap -start <= minLength:
                    one_storage = []
                    state = not state  #转换状态
                    count_state = False                  
                else: 
                    one_storage.append(x1) #直线的另一个端点
                    one_storage.append(y1-gap)
                    all_storage.append(one_storage) #保存这条直线的信息到列表中
                    state = not state  #转换状态
                    one_storage = [] #清空直线信息
                    count_state = False #记数器状态关闭
        if count_state and condition:
            count = 0
            count_state = False          #计数器状态关闭
        y1 = y1+1
    return all_storage

#找图中的横线
def row(img,x1,y1,x2,y2):
    all_storage = [] #所有横线端点的坐标
    one_storage = [] #一条横线端点的坐标
    count = 0 #上下间隔计数器
    state = True
    count_state = False   #记数器状态关闭
    gap = 4    #允许直线的最大间隔是4
    width = 2  #允许直线上下偏移两个像素值
    minLength = 10 #直线的最小长度
    while x1<x2:
        
        condition = (img[y1-width:y1+width+1,x1]==255).any() #判断是否是直线上的点
        if state and condition:
            start = x1              #起点
            one_storage.append(x1)  #直线的一个端点
            #print('y1',y1)
            one_storage.append(y1)
            state = not state
        if not state and not condition:
            count_state = True    #计数器状态打开
            count = count + 1
            if count == gap:
                count = 0          #记数器归零
                if x1 - gap -start <= minLength:     #直线小于最小长度
                    one_storage = []
                    state = not state  #转换状态
                    count_state = False                  
                else: 
                    one_storage.append(x1-gap) #直线的另一个端点
                    one_storage.append(y1)
                    all_storage.append(one_storage) #保存这条直线的信息到列表中
                    state = not state  #转换状态
                    one_storage = [] #清空直线信息
                    count_state = False #记数器状态关闭
        if count_state and condition:
            count = 0
            count_state = False          #计数器状态关闭
        x1 = x1+1
    return all_storage

#找图中的斜线
def slash(img,x1,x2,k,b):
    h,w = img.shape
    all_storage = [] #所有斜线端点的坐标
    one_storage = [] #一条斜线端点的坐标
    count = 0 #上下间隔计数器
    state = True
    count_state = False   #记数器状态关闭
    gap = 4    #允许直线的最大间隔是4
    width = 1  #允许直线上下偏移两个像素值
    minLength = 10 #直线的最小长度
    while x1<x2:
        y1 = round(k*x1+b)
        y1 = int(y1)
        if y1-width>=0 and y1+width+1<h:
            if x1-width >=0 and x1+width+1<= x2:            
                condition = (img[y1-width:y1+width+1,x1-width:x1+width+1]==255).any() #允许直线左右偏移两个像素

            
                
            else: 
                condition = img[y1,x1] == 255
            if condition and state:
                start_x = x1
                start_y = y1
                one_storage.append(x1)
                one_storage.append(y1)
                state = not state
            if not condition and not state:
                count = count+1
                count_state = True
                if count == gap:
                    count = 0 
                    y1_old = round(k*(x1-gap)+b)
                    y1_old = int(y1_old)
                    lenth = np.sqrt(((x1-gap-start_x)**2+(y1_old-start_y)**2))
                    if lenth < minLength:
                        one_storage = []
                        state = not state  #转换状态
                        count_state = False                  
                    else:
                        one_storage.append(x1-gap) #直线的另一个端点
                        one_storage.append(y1_old)
                        all_storage.append(one_storage) #保存这条直线的信息到列表中
                        state = not state  #转换状态
                        one_storage = [] #清空直线信息
                        count_state = False #记数器状态关闭  
            if count_state and condition:
                count_state = False
                count = 0 
        x1 = x1+1
    return all_storage                                     

def Hough(img):
    img = transition(img)
    h,w = img.shape
    minLineLength = 15
    maxLineGap = 20
    lines = cv2.HoughLinesP(img,1,np.pi/180,minLineLength,maxLineGap)
    lines = np.squeeze(lines)
    standard = 30

    #img_rgb = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    existed_y = []
    existed_x = []
    existed_slash = []
    all_x = []
    all_y = []
    for x1,y1,x2,y2 in lines:
        if x1 == x2 and x1 not in existed_x:           #避免横坐标相同的直线段重复检测
            existed_x.append(x1)
            y1 = 0
            y2 = h
            #print('x1,y1,x2,y2',x1,y1,x2,y2)
            column_lines = columnline(img,x1,y1,x2,y2)
            if len(column_lines) > 0:
                all_y.append(column_lines)
        if y1 == y2 and y1 not in existed_y:
            existed_y.append(y1)
            x1 = 0
            x2 = w
            #cv2.line(img_rgb,(x1,y1),(x2,y2),(0,0,255),1)
            row_lines = row(img,x1,y1,x2,y2)
            if len(row_lines)>0:
                all_x.append(row_lines)
        if x1!=x2 and y1!=y2:
            k = (y1-y2)/(x1-x2)
            b = -k*x1 + y1
            x1 = 0
            y1 = round(k*x1+b)
            x2 = w
            y2 = round(k*x2+b)
            slash_lines = slash(img,x1,x2,k,b)
            existed_slash.append(slash_lines)
 

  
    list_x = []
    list_y = []
    list_slash = []
    for lines in all_x:
        for line in lines:
            list_x.append(line)
    for lines in all_y:
        for line in lines:
            list_y.append(line)
    for lines in existed_slash:
        for line in lines:
            list_slash.append(line)
    list_x = horizontalSingleWall(list_x)
    list_y = columnSingleWall(list_y)
    list_slash = slashSingleWall(list_slash)
    #print('****list_slash=',list_slash)
    #print('list_x=',list_x)
    #print('list_y=',list_y)
    return list_x,list_y,list_slash

def draw_line(x_lines,y_lines,b_lines,img_rgb):
    for x_line in x_lines:
        x1,y1,x2,y2 = x_line
        cv2.line(img_rgb,(x1,y1),(x2,y2),(0,0,255),1)
    for y_line in y_lines:
        x1,y1,x2,y2 = y_line
        cv2.line(img_rgb,(x1,y1),(x2,y2),(0,0,255),1)
    for element in b_lines:
        x1,y1,x2,y2 = element
        cv2.line(img_rgb,(x1,y1),(x2,y2),(0,0,255),1)
    cvShow(img_rgb)
    cv2.imwrite(r'E:\picture\beike\result_3.jpg',img_rgb)

def recard(x_lines,y_lines,b_lines):
    with open(r'E:\picture\beike\location.txt','w') as f:
        f.write('x1,y1,x2,y2\n')
    with open(r'E:\picture\beike\location.txt','a') as f:
        f.write('column:\n')
        for y_line in y_lines:
            for one in y_line:
                f.write(str(one))
                f.write('\n')
        f.write('row:\n')
        for x_line in x_lines:
            for one in x_line:
                f.write(str(one))
                f.write('\n')
        f.write('slash:\n')
        for element in b_lines:
            f.write(str(element[:4]))
            f.write('\n')


def singleWall(x):
    single_horizontal_line = []
    single_column_line  = []
    slash_line = []
    if x[0][0] == x[0][2]:
        single_horizontal_line = horizontalSingleWall(x)
    elif x[0][1] == x[0][3]:
        single_column_line = columnSingleWall(x)
    else:
        slash_line = x
    single = single_horizontal_line
    single.extend(single_column_line)
    single.extend(slash_line)
    return single
    

if __name__ == '__main__':
    img = cv2.imread(r'E:\picture\beike\xi_3.jpg',0)
    #cvShow(img)
    #binary_img = transition(img)
    x_lines,y_lines,b_lines = Hough(img)
    img_rgb = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    draw_line(x_lines,y_lines,b_lines,img_rgb)
    #recard(x_lines,y_lines,b_lines)
