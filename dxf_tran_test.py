import ezdxf
from ezdxf.addons import Importer
import math
'''
门框
斜向家具、门、窗
家具方向
'''
def load_txt(filepath):
    with open(filepath, "r") as f:
        labels = ['bearing_wall:','not_bearing_wall:','window-door:','bed:','teapoy:','sofa:','toilets:','kitchen:','desk:','TV:','locker:','wash:']
        flag = ''
        ans = {'bearing_wall:':[],'not_bearing_wall:':[],'window-door:':[],'bed:':[],'teapoy:':[],'sofa:':[],'toilets:':[],'kitchen:':[],'desk:':[],'TV:':[],'locker:':[],'wash:':[]}
        for line in f.readlines():
            line = line.strip('\n').strip('\t')
            if line in labels:
                flag = line
                continue
            if flag in labels and line != '':
                ans[flag].append(eval(line))
    #print(ans)
    return ans

#def print_entity(e):
    #print("layer: %s\n" % e.dxf.layer)
    #print("dxftype: %s\n" % e.dxftype())
    #print("start point: %s\n" % e.dxf.start)
    #print("end point: %s\n" % e.dxf.end)

def model_importer(src_doc,target_doc):
    importer = Importer(src_doc,target_doc)
    names = []
    for i in src_doc.blocks:
        #print(i.name)
        names.append(i.name)
        importer.import_block(i.name)
    importer.finalize()
    return target_doc,names
'''
def show_entity(msp):
    for e in msp:
        print_entity(e)
'''

def creat_layer(doc,lis):
    i = 1
    for l in lis:
        doc.layers.new(name=l, dxfattribs={'linetype': 'DASHED', 'color': i})
        i += 1
    return doc

def wall_face(l,Thick,low,high):
    ans = []
    if l[1] != l[3]:
        ans.append([(l[0]-Thick/2,l[1]-Thick/2,low),(l[0]+Thick/2,l[1]-Thick/2,low),(l[2]+Thick/2,l[3]+Thick/2,low),(l[2]-Thick/2,l[3]+Thick/2,low)])
        ans.append([(l[0]-Thick/2,l[1]-Thick/2,high),(l[0]+Thick/2,l[1]-Thick/2,high),(l[2]+Thick/2,l[3]+Thick/2,high),(l[2]-Thick/2,l[3]+Thick/2,high)])
        ans.append([(l[0]-Thick/2,l[1]-Thick/2,high),(l[0]+Thick/2,l[1]-Thick/2,high),(l[0]+Thick/2,l[1]-Thick/2,low),(l[0]-Thick/2,l[1]-Thick/2,low)]) #上
        ans.append([(l[0]-Thick/2,l[1]-Thick/2,high),(l[2]-Thick/2,l[3]+Thick/2,high),(l[2]-Thick/2,l[3]+Thick/2,low),(l[0]-Thick/2,l[1]-Thick/2,low)]) #左
        ans.append([(l[2]-Thick/2,l[3]+Thick/2,high),(l[2]+Thick/2,l[3]+Thick/2,high),(l[2]+Thick/2,l[3]+Thick/2,low),(l[2]-Thick/2,l[3]+Thick/2,low)]) #下
        ans.append([(l[0]+Thick/2,l[1]-Thick/2,high),(l[2]+Thick/2,l[3]+Thick/2,high),(l[2]+Thick/2,l[3]+Thick/2,low),(l[0]+Thick/2,l[1]-Thick/2,low)])
    else:
        ans.append([(l[0]-Thick/2,l[1]-Thick/2,low),(l[0]-Thick/2,l[1]+Thick/2,low),(l[2]+Thick/2,l[3]+Thick/2,low),(l[2]+Thick/2,l[3]-Thick/2,low)])
        ans.append([(l[0]-Thick/2,l[1]-Thick/2,high),(l[0]-Thick/2,l[1]+Thick/2,high),(l[2]+Thick/2,l[3]+Thick/2,high),(l[2]+Thick/2,l[3]-Thick/2,high)])
        ans.append([(l[0]-Thick/2,l[1]-Thick/2,high),(l[0]-Thick/2,l[1]+Thick/2,high),(l[0]-Thick/2,l[1]+Thick/2,low),(l[0]-Thick/2,l[1]-Thick/2,low)])
        ans.append([(l[0]-Thick/2,l[1]-Thick/2,high),(l[2]+Thick/2,l[3]-Thick/2,high),(l[2]+Thick/2,l[3]-Thick/2,low),(l[0]-Thick/2,l[1]-Thick/2,low)])
        ans.append([(l[2]+Thick/2,l[3]-Thick/2,high),(l[2]+Thick/2,l[3]+Thick/2,high),(l[2]+Thick/2,l[3]+Thick/2,low),(l[2]+Thick/2,l[3]-Thick/2,low)])
        ans.append([(l[0]-Thick/2,l[1]+Thick/2,high),(l[2]+Thick/2,l[3]+Thick/2,high),(l[2]+Thick/2,l[3]+Thick/2,low),(l[0]-Thick/2,l[1]+Thick/2,low)])
    return ans

def draw_wall_3d(msp,lis,layer,Thick=10,low=0,high=60):
    pf = msp.add_polyface(dxfattribs={'layer': layer})
    for l in lis:
        ans = wall_face(l,Thick,low,high)
        for i in ans:
            pf.append_face(i)
    return msp

def draw_door_fram(msp,lis,layer,Thick=10,low=0,high=60):
    pf = msp.add_polyface(dxfattribs={'layer': layer})
    for l in lis:
        ans = wall_face(l,Thick,low,high)
        for i in ans:
            pf.append_face(i)
    return msp

def draw_wd(msp,lis,layer,Thick=10,low=0,high=60):
    for l in lis:
        long = abs(l[0]-l[2])+abs(l[1]-l[3])
        rotate, ang = 0, 0
        if abs(l[0]-l[2])<abs(l[1]-l[3]):
            rotate = 0
        ang = math.atan2((l[1]-l[3]),(l[0]-l[2]))/math.pi*180
        #print(ang)
        if long>1000 or long<600:            
            msp.add_blockref('推拉窗5 - 带贴面 - 900 x 1200mm-330476-_三维_',insert =(int((l[0]+l[2])/2),int((l[1]+l[3])/2)),dxfattribs={'xscale': (long-100)/920,'yscale':1,'zscale': 1,'rotation':rotate+ang})
            msp = draw_wall_3d(msp,[l],layer='A-WALL',Thick=220,low=0,high=1000)
            msp = draw_wall_3d(msp,[l],layer='A-WALL',Thick=220,low=2000,high=3000)
        else:
            msp.add_blockref('单嵌板木门 12 - 800 x 2100mm-373023-_三维_',insert =(int((l[0]+l[2])/2),int((l[1]+l[3])/2)),dxfattribs={'xscale': (long-50)/820,'yscale': 1,'zscale': 1,'rotation':rotate+ang})
            msp = draw_wall_3d(msp,[l],layer='A-WALL',Thick=100,low=2000,high=3000)
    return msp

def draw_furn(msp,lis,name,high = 0):
    sizes = {'三人沙发8 - W2010_D890_H850-349890-_三维_':[2010,890],
            '玻璃茶几 - 矩形2 - W1300_D700_H400-350883-_三维_':[1300,700],
            '西餐桌椅组合 - 1200x850x750mm 松木-353545-_三维_':[1200,850],
            '地柜1 - W1830 _D410_H400mm-355695-_三维_':[1830,410],
            '双人床5 - W1680_D2256-343117-_三维_':[1680,2256],
            '连体式座便器 - 污水出口到墙 305-339689-_三维_':[501,733],
            '西餐桌椅组合 - 1200x850x750mm 松木-353545-_三维_':[1200,850],
            '地柜1 - W1830 _D410_H400mm-355695-_三维_':[1830,410],
            '梳妆台柜 - 双门洗涤台 - 1234 x 590 x 800mm-365402-_三维_':[1234,590],
            '电视 - 平板 - 1270mm-354731-_三维_':[1830,410],
            '小厨房-中 - 1372mm-364451-_三维_':[1372,410]
            }
            
    for l in lis:
        dxfattrib={'xscale': 1,'yscale':1,'zscale': 1,'rotation':0}
        w,d = abs(l[0]-l[2]),abs(l[1]-l[3])
        '''
        if w < d:
            dxfattrib['rotation'] = 90'''
        if name in sizes.keys():
            if (w < d and sizes[name][0]<sizes[name][1]) or (w > d and sizes[name][0]>sizes[name][1]):
                #dxfattrib['xscale'] = w/sizes[name][0]
                #dxfattrib['yscale'] = d/sizes[name][1]
                pass
            else:
                dxfattrib['rotation'] += 90
                #dxfattrib['xscale'] = w/sizes[name][1]
                #dxfattrib['yscale'] = d/sizes[name][0]
            if not 0.7*(sizes[name][0]+sizes[name][1])<(w+d)<1.5*(sizes[name][0]+sizes[name][1]):
                continue
        if name == '双人床5 - W1680_D2256-343117-_三维_':
            dxfattrib['xscale'] = 0.8
            dxfattrib['yscale'] = 0.8
            msp.add_blockref(name,insert =(int((l[0]+l[2])/2+300),int((l[1]+l[3])/2),high),dxfattribs=dxfattrib)
        else:
            msp.add_blockref(name,insert =(int((l[0]+l[2])/2),int((l[1]+l[3])/2),high),dxfattribs=dxfattrib)
    return msp

def draw_dxf(txt_path,save_path,src_dxf=r'.\template\wifi_dxf.dxf'):
    src_doc = ezdxf.readfile(src_dxf)
    doc = ezdxf.new()
    doc, names = model_importer(src_doc,doc)
    msp = doc.modelspace()
    #name = '130'
    ans = load_txt(txt_path)
    #print(ans)
    labels = ['bearing_wall:','not_bearing_wall:','window-door:','bed:','teapoy:','sofa:','toilets:','kitchen:','desk:','tv:','locker:','wash:']
    msp = draw_wall_3d(msp,ans['bearing_wall:'],layer='A-WALL',Thick=220,low=0,high=3000)
    msp = draw_wall_3d(msp,ans['not_bearing_wall:'],layer='A-WALL',Thick=100,low=0,high=3000)
    msp = draw_wd(msp,ans['window-door:'],layer='A-WALL',Thick=6,low=0,high=60)
    msp = draw_furn(msp,ans['bed:'],'双人床5 - W1680_D2256-343117-_三维_')
    msp = draw_furn(msp,ans['teapoy:'],'玻璃茶几 - 矩形2 - W1300_D700_H400-350883-_三维_')
    msp = draw_furn(msp,ans['sofa:'],'三人沙发8 - W2010_D890_H850-349890-_三维_')
    msp = draw_furn(msp,ans['toilets:'],'连体式座便器 - 污水出口到墙 305-339689-_三维_')
    msp = draw_furn(msp,ans['kitchen:'],'小厨房-中 - 1372mm-364451-_三维_')
    msp = draw_furn(msp,ans['desk:'],'西餐桌椅组合 - 1200x850x750mm 松木-353545-_三维_')
    msp = draw_furn(msp,ans['TV:'],'地柜1 - W1830 _D410_H400mm-355695-_三维_')
    msp = draw_furn(msp,ans['TV:'],'电视 - 平板 - 1270mm-354731-_三维_',high=400)
    msp = draw_furn(msp,ans['wash:'],'梳妆台柜 - 双门洗涤台 - 1234 x 590 x 800mm-365402-_三维_')
    doc.saveas(save_path)

if __name__ == '__main__':
    names = ['130','144','150','153','155','170','173','180','185','190','206','250']
    #main('144')
    #for name in names:
    #    main(name)
        #break
    #load_txt(r'C:\Users\zhangyichi\Desktop\location\150.txt')
    draw_dxf(src_dxf=r'D:\Projects\BK\dxf\house\house\dxf\wifi_dxf.dxf',txt_path=r'C:\Users\zhangyichi\Desktop\location\150.txt',save_path='150.dxf')