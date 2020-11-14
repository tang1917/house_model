import cv2 as cv
import numpy as np

# 读取txt中墙体数据
def load_txt(filepath):
    with open(filepath, "r") as f:
        flag = 0
        bearing_walls,not_bearing_walls = [],[]
        for line in f.readlines():
            line = line.strip('\n').strip('\t')
            if line == 'bearing_wall:':
                flag = 1
                continue
            elif line == 'not_bearing_wall:':
                flag = 2
                continue
            elif line == '':
                flag = 0
                continue

            if flag == 1:
                bearing_walls.append(eval(line))
            elif flag == 2:
                not_bearing_walls.append(eval(line))
        bearing_walls,not_bearing_walls = bearing_walls[1:],not_bearing_walls[1:]
        #print(bearing_walls)
        #print(not_bearing_walls)
    return bearing_walls,not_bearing_walls

# 获取两点之间曼哈顿距离
'''
输入：get_distance((point1_x,point1_y),(point2_x,point2_y))
输出：int型曼哈顿距离
'''
def get_distance(point1,point2):
    #print(abs(point1[0]-point2[0])+abs(point1[1]-point2[1]))
    return abs(point1[0]-point2[0])+abs(point1[1]-point2[1])

# 得到边缘检测图
'''
输入：待测图片路径
输出：边缘检测后图像array
'''
def get_win_door(filepath):
    image = cv.imread(filepath)
    #image = cv.imread('D:\Projects\BK\Dataset\house/144.jpg')
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    #cv.imshow("gray", gray)
    ret, binary = cv.threshold(gray,180,255,cv.THRESH_BINARY)
    #print("阈值：", ret)
    #cv.imshow("binary", binary)
    img = cv.GaussianBlur(binary,(3,3),0)
    #cv.imshow("Gaussian", img)
    canny = cv.Canny(img, 150, 200)
    #cv.imshow("final", canny)
    #cv.waitKey(0)
    return canny

# 获取可能需要填补的线段
'''
输入：[(368, 162, 385, 162), (422, 162, 487, 162), (479, 162, 637, 162)],就是txt里存的格式
输出：[[(368, 162), (422, 162)], [(368, 162), (487, 162)], [(368, 162), (479, 162)]],一个()表示一个点，一个[]表示一条线
'''
def get_near_P(lis,isbearing_walls=False):
    ans = []
    #print(lis)
    lis_temp = []
    for x in lis:
        lis_temp.append(x[:2])
        lis_temp.append(x[2:])
    for i in range(len(lis_temp)-1):
        for j in range(i+1,len(lis_temp)):
            dis = get_distance(lis_temp[i],lis_temp[j])
            if 5 <= dis <= 200 and lis_temp[i]+lis_temp[j] not in lis:
                ans.append([lis_temp[i],lis_temp[j]])
                if isbearing_walls:
                    ans.append([lis_temp[i],(lis_temp[i][0],lis_temp[j][1])])
                    ans.append([lis_temp[i],(lis_temp[j][0],lis_temp[i][1])])
                    ans.append([(lis_temp[i][0],lis_temp[j][1]),lis_temp[j]])
                    ans.append([(lis_temp[j][0],lis_temp[i][1]),lis_temp[j]])
    #print(ans)
    return ans

# 绘制线
'''
输入：plot_line(ima,near_P,name)，ima：cv读取的图片，near_P：get_near_p()函数输出，name：字符串，改变cv.imshow函数标题
输出：绘图
'''
def plot_line(ima,near_P,name):
    image = ima.copy()
    for line in near_P:
        final = cv.line(image,line[0],line[1],color=(255,255,0),thickness=5)
    cv.imshow(name,final)

# 绘制墙体
'''
输入：plot_wall(ima,lis,name)，ima为cv读取的图片；lis：[(368, 162, 385, 162), (422, 162, 487, 162)]，txt中格式；name：字符串，改变cv.imshow函数标题
输出：绘图，返回绘图后图像
'''
def plot_wall(ima,lis,name):
    image = ima.copy()
    for line in lis:
        temp = cv.line(image,(line[:2]),(line[2:]),color=(255,255,0),thickness=5)
    cv.imshow(name,temp)
    return temp

# 消除交叉处毛刺
'''
输入：lis：[(368, 162, 385, 162), (422, 162, 487, 162)]，txt中格式
输出：消除毛刺后lis：[(368, 162, 385, 162), (422, 162, 487, 162)]，txt中格式
'''
def wall_cross(lis):
    x = dict((a,lis.count(a)) for a in lis)
    while len(x) != 0:  
        x_c = [k for k,v in x.items() if max(x.values())==v]
        #print(x_c)
        for i in x_c:
            for k in list(x.keys()):
                if abs(i-k)<=6:
                    x.pop(k)
                    lis = [i if j ==k else j for j in lis]
    #print(dict((a,lis.count(a)) for a in lis))
    return lis

'''
输入：lis：[(368, 162, 385, 162), (422, 162, 487, 162)]，txt中格式
输出：消除毛刺后lis：[(368, 162, 385, 162), (422, 162, 487, 162)]，txt中格式
'''
def pretreat_wall(lis):
    lis_x, lis_y = [], []
    for temp in lis:
        lis_x.extend([temp[0],temp[2]])
        lis_y.extend([temp[1],temp[3]])
    #print(set(lis_x))
    lis_x = wall_cross(lis_x)
    lis_y = wall_cross(lis_y)
    lis = []
    for i in range(0,len(lis_x)-1,2):
        lis.append((lis_x[i],lis_y[i],lis_x[i+1],lis_y[i+1]))
    return lis

# 获取实际应该填补的线
'''
输入：[[(368, 162), (422, 162)], [(368, 162), (487, 162)], [(368, 162), (479, 162)]],一个()表示一个点，一个[]表示一条线
输出：[[(368, 162), (422, 162)], [(368, 162), (487, 162)], [(368, 162), (479, 162)]],一个()表示一个点，一个[]表示一条线
'''
def link_wall(ima,lis):
    '''
    ans = []
    for i in lis:
        if i[0][0]==i[1][0] or i[0][1]==i[1][1]:
            ans.append(i)'''
    ans = []
    thres = 7
    for i in lis:
        '''
        print(min(i[0][1],i[1][1]))
        print(max(i[0][1],i[1][1]))
        print(min(i[0][0],i[1][0]))
        print(max(i[0][0],i[1][0]))'''
        if i[0][0]==i[1][0] or i[0][1]==i[1][1]:
        #if i[1][0]-6<=i[0][0]<=i[1][0]+6 or i[1][1]-6<=i[0][1]<=i[1][1]+6:
            temp_img = ima[min(i[0][1],i[1][1])-thres:max(i[0][1],i[1][1])+thres,min(i[0][0],i[1][0])-thres:max(i[0][0],i[1][0])+thres]
            #print('zhi')
            #print(temp_img)
            sum_t = temp_img.sum(int(temp_img.shape[1]<=temp_img.shape[0]))
            #print(list(map(int,sum_t/255)))
            sum_t = sum_t/255
            for j in range(len(sum_t)):
                if sum_t[j] > 1: 
                    sum_t[j] = 1
            #print(sum_t)
            if sum_t.sum()/len(sum_t)>=0.9:
                ans.append(i)
        
        elif (i[0][1]<i[1][1] and i[0][0]<i[1][0]) or (i[0][1]>i[1][1] and i[0][0]>i[1][0]):
            temp_img = []
            root_x = min(i[0][1],i[1][1])
            root_y = min(i[0][0],i[1][0])
            width = abs(i[0][1] - i[1][1])
            high = abs(i[0][0] - i[1][0])
            for h in range(high):
                if root_x+int(h/high*width)-thres>=0 and root_x+int(h/high*width)+thres<ima.shape[1] and root_y+h<ima.shape[0]:
                    temp_img.append(ima[root_x+int(h/high*width)-5:root_x+int(h/high*width)+5,root_y+h])
            if len(temp_img) != 0:
                temp_img = np.array(temp_img) 
                sum_t = temp_img.sum(int(temp_img.shape[1]<=temp_img.shape[0]))
                sum_t = sum_t/255
                for j in range(len(sum_t)):
                    if sum_t[j] > 1: 
                        sum_t[j] = 1
                if sum_t.sum()/len(sum_t)>=0.95:
                    ans.append(i)
                
        else:
            temp_img = []
            root_x = max(i[0][1],i[1][1])
            root_y = min(i[0][0],i[1][0])
            width = abs(i[0][1] - i[1][1])
            high = abs(i[0][0] - i[1][0])
            for h in range(high):
                if root_x+int(h/high*width)-7>=0 and root_x+int(h/high*width)+7<ima.shape[1] and root_y+h<ima.shape[0]:
                    temp_img.append(ima[root_x-int(h/high*width)-7:root_x-int(h/high*width)+7,root_y+h])
            temp_img = np.array(temp_img)
            if len(temp_img) != 0:
                sum_t = temp_img.sum(int(temp_img.shape[1]<=temp_img.shape[0]))
                sum_t = sum_t/255
                for j in range(len(sum_t)):
                    if sum_t[j] > 1: 
                        sum_t[j] = 1
                if sum_t.sum()/len(sum_t)>=0.95:
                    ans.append(i)
    return ans

#def possibility_point(lis):


#filepath = "D:\Projects\BK\door\location_3.txt"
#print(get_distance((1,1),(0,0)))
#get_win_door('D:\Projects\BK\Dataset\house/144.jpg')
def main():
    txt_path = r"C:\Users\zhangyichi\Desktop\location\144.txt"
    bearing_walls, not_bearing_walls = load_txt(txt_path)
    ima = cv.imread(r'D:\Projects\BK\Dataset\house\144.jpg')
    canny = get_win_door(r'D:\Projects\BK\Dataset\house\144.jpg')
    #canny = cv.flip(canny,1)
    lines = bearing_walls+not_bearing_walls
    # 未预处理的墙体
    wall = plot_wall(canny,lines,'none_pre')
    #lines = pretreat_wall(lines)
    # 预处理后的墙体
    #bearing_walls = pretreat_wall(bearing_walls)
    #print(bearing_walls)
    #not_bearing_walls = pretreat_wall(not_bearing_walls)
    wall = plot_wall(ima,lines,'line')
    plot_wall(canny,bearing_walls,'bearing_walls')
    #plot_wall(canny,not_bearing_walls,'not_bearing_walls')
    #cv.waitKey(0)
    near_p_l = get_near_P(lines)
    near_p_b = get_near_P(bearing_walls,True)
    near_p_n = get_near_P(not_bearing_walls)
    near_p = get_near_P(bearing_walls,True) + get_near_P(not_bearing_walls) + get_near_P(lines)
    #print(len(near_p_b))
    #print(len(near_p_n))
    #linker = link_wall(canny, near_p_b) +link_wall(canny, near_p_n)
    linker = link_wall(canny, near_p)
    plot_line(wall,linker,'walls_link')
    #plot_line(canny,near_p_b,'bearing_walls_link')
    #plot_line(canny,near_p_n,'not_bearing_walls_link')
    cv.waitKey(0)


def wall(txt_path,ima_path):
    bearing_walls, not_bearing_walls = load_txt(txt_path)
    canny = get_win_door(ima_path)
    lines = bearing_walls+not_bearing_walls
    lines = pretreat_wall(lines)
    near_p_l = get_near_P(lines,True)
    linker = link_wall(canny, near_p_l)
    #plot_line(canny,linker,'walls_link')
    #plot_line(canny,near_p_b,'bearing_walls_link')
    #plot_line(canny,near_p_n,'not_bearing_walls_link')
    #cv.waitKey(0)

def findwindow(not_bearing_walls,bearing_walls,ima_path):
    #bearing_walls, not_bearing_walls = load_txt(txt_path)
    canny = get_win_door(ima_path)
    #ima = cv.imread(ima_path)
    lines = bearing_walls+not_bearing_walls
    lines = pretreat_wall(lines)
    #wall = plot_wall(ima,lines,'line')
    bearing_walls, not_bearing_walls = lines[:len(bearing_walls)],lines[len(bearing_walls):]
    near_p_l = get_near_P(bearing_walls,True) + get_near_P(not_bearing_walls) + get_near_P(lines)
    linker = link_wall(canny, near_p_l)
    #plot_line(wall,linker,'walls_link')
    #plot_line(canny,near_p_b,'bearing_walls_link')
    #plot_line(canny,near_p_n,'not_bearing_walls_link')
    #cv.waitKey(0)
    linker_1 = []
    for upda in linker:
        x1,y1,x2,y2 = upda[0][0],upda[0][1],upda[1][0],upda[1][1]
        s_u = [x1,y1,x2,y2]
        linker_1.append(s_u)
    return linker_1
#wall2(r'C:\Users\zhangyichi\Desktop\location\153.txt',r'D:\Projects\BK\Dataset\house\temp.jpg')
if __name__ == "__main__":
   main()