from roughline import *
from detectwall import *
from collections import Counter

def cvShow(img):
    cv2.namedWindow('img',0)
    cv2.imshow('img',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def defineWidth(img,img_binary,x_lines,y_lines,slash_lines):

    #周围直线集合
    num_gather = []
    x_gather = []
    y_gather = []
    x_sorted = sorted(x_lines,key = lambda x:x[1])
    y_sorted = sorted(y_lines,key = lambda x:x[0]) 

    x_up_value = x_sorted[0][1]
    x_bellow_value = x_sorted[-1][1]
    y_left_value = y_sorted[0][0]
    y_right_value = y_sorted[-1][0]
    #print('x_up=',x_up)
    for line in x_sorted:
        if line[1] == x_up_value or line[1]==x_bellow_value:
            x_gather.append(line)
    for line in y_sorted:
        if line[0] == y_left_value or line[0]== y_right_value:
            y_gather.append(line)

    for line in x_gather:
        x1,y1,x2,y2 = line
        while x1<=x2:
            num = horizontalWallCounter(x1,y1,x2,y2,img_binary)
            num_gather.append(num)
            x1 = x1+1
    for line in y_gather:
        x1,y1,x2,y2 = line
        while y1<=y2:
            num = columnWallCounter(x1,y1,x2,y2,img_binary)
            num_gather.append(num)
            y1 = y1+1
    most_num = Counter(num_gather).most_common(1)[0][0]
    rate = 220/most_num
    threshold_s = int(round(4/3*most_num))
    threshold_b = int(round(2/3*most_num))
    threshold_t = int(round(1/5*most_num))
    return threshold_s,threshold_b,threshold_t,rate