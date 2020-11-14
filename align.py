import numpy as np
from deleteSimilarLine import set_collection
from crossline import removeCrossShortLine
from longconnect import setcategory
#返回同一水平或者同一竖直线的数目
def countList(lis,loca):
    sor = []
    line_count = dict()
    for line in lis:
        sor.append(line[loca])
    for line in lis:
        counts = sor.count(line[loca])
        #print('line=',line)
        line_count[str(line)] = counts
    return line_count

#把集合中出现最多的线段对齐
#0，1，2：水平，竖直，倾斜；0，1,2：细,粗,窗户
def align(thin_wall,bold_wall,window,th):
 
    bold = []
    thin = []
    ans_window=[]
 
    h_line = []
    c_line = []
    #斜线
    for line in bold_wall:
        if line[4]==2:
            bold.append(line)
        elif line[4]==0:
            h_line.append(line)
        else:
            c_line.append(line)
    for line in thin_wall:
        if line[4]==2:
            thin.append(line)
        elif line[4]==0:
            h_line.append(line)
        else:
            c_line.append(line)
    for line in window:
        if line[4] == 2:
            ans_window.append(line)
        elif line[4]==0:
            h_line.append(line)
        else:
            c_line.append(line)

    #水平对齐
    for location,lis in zip([0,1],[h_line,c_line]):
        dicts = countList(lis,location)

        all_sets = set_collection(lis,location,margin=10)
        for sets in all_sets:
            length = len(sets)
            for i in range(length):
                num_max = 0
                line_max = sets[0]
                if dicts[str(sets[i])]>num_max:
                    num_max = dicts[str(sets[i])]
                    line_max = sets[i]
            #与出现最多的线段对齐
            standard = line_max[location]
            for i in range(length):
                sets[i][location] = sets[i][location+2] = standard
                if sets[i][-1] == 0:
                    thin.append(sets[i])
                elif sets[i][-1] == 1:
                    bold.append(sets[i])
                else:
                    ans_window.append(sets[i])
    thin_wall,bold_wall,window_wall = removeCrossShortLine(thin,bold,ans_window,th)
    thin_wall,bold_wall,window_wall = setcategory(thin_wall,bold_wall,window_wall)
    return thin_wall,bold_wall,window_wall
