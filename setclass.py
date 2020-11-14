import numpy as np
from copy import copy


def property(thin,bold,window):
    #0，1，2：水平，竖直，倾斜；0，1,2：细,粗,窗户
    ans_thin = []
    ans_bold = []
    ans_window = []
    for line in thin:
        if line[0] == line[2]:  #水平
            line.extend((0,0))
            ans_thin.append(line)

        elif line[1] == line[3]:
            line.extend((1,0))
            ans_thin.append(line)
        else:
            line.extend((2,0))
            ans_thin.append((line))
    for line in bold:
        if line[0] == line[2]:
            line.extend((0,1))
            ans_bold.append(line)
        elif line[1] == line[3]:
            line.extend((1,1))
            ans_bold.append(line)
        else:
            line.extend((2,1))  
            ans_bold.append(line)
    for line in window:
        if line[0] == line[2]:
            line.extend((0,2))
            ans_window.append(line)
        elif line[1] == line[3]:
            line.extend((1,2))
            ans_window.append((line))
        else:
            line.extend((2,2))
            ans_window.append((line))
    return ans_thin,ans_bold,ans_window
        
