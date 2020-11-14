import numpy as np

def setcategory(thin,bold,window):
    thin_column={}
    thin_horizontal={}
    bold_column={}
    bold_horizontal={}
    thin_wall = []
    bold_wall = []
    window_wall = []
    for line in thin:
        #水平，细
        if line[4]==1:
            if line[1] not in thin_horizontal.keys():
                thin_horizontal[line[1]]=[]
                thin_horizontal[line[1]].append(line[:4])
            else:
                thin_horizontal[line[1]].append(line[:4])
        #竖直，细
        elif line[4]==0:
            if line[0] not in thin_column.keys():
                thin_column[line[0]]=[]
                thin_column[line[0]].append(line[:4])
            else:
                thin_column[line[0]].append(line[:4])
        else:
            thin_wall.append(line[:4])
    bold.extend(window)
    for line in bold:
        #水平，粗
        if line[4]==1:
            if line[1] not in bold_horizontal.keys():
                bold_horizontal[line[1]]=[]
                bold_horizontal[line[1]].append(line[:4])
            else:
                bold_horizontal[line[1]].append(line[:4])
        elif line[4]==0:
        #竖直，粗
            if line[0] not in bold_column.keys():
                bold_column[line[0]]=[]
                bold_column[line[0]].append(line[:4])
            else:
                bold_column[line[0]].append(line[:4])           
        else:
            bold_wall.append(line[:4])
    for k,collect in thin_horizontal.items():
        temp = []
        for line in collect:
            temp.extend([line[0],line[2]])
        m = max(temp)
        n = min(temp)
        ans = [n,k,m,k]
        thin_wall.append(ans)
    for k,collect in thin_column.items():
        temp=[]
        for line in collect:
            temp.extend([line[1],line[3]])
        m = max(temp)
        n = min(temp)
        ans = [k,n,k,m]
        thin_wall.append(ans)
    for k,collect in bold_horizontal.items():
        temp = []
        for line in collect:
            temp.extend([line[0],line[2]])
        m = max(temp)
        n = min(temp)
        ans = [n,k,m,k]
        bold_wall.append(ans)      
    for k,collect in bold_column.items():
        temp=[]
        for line in collect:
            temp.extend([line[1],line[3]])
        m = max(temp)
        n = min(temp)
        ans = [k,n,k,m]
        bold_wall.append(ans) 
    
    for line in window:
        window_wall.append(line[:4])
    return thin_wall,bold_wall,window_wall

    

