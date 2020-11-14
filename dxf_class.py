import ezdxf
from ezdxf.addons import Importer
import math
import time
import os
import copy
'''
门框
斜向家具、门、窗
家具方向
'''
class DXF(object):
    def __init__(self,src_dxf,txt_path,save_path):
        self.src_dxf = src_dxf
        self.txt_path = txt_path
        self.save_path = save_path
    def load_txt(self):
        with open(self.txt_path, "r") as f:
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
        self.location = ans
        return ans

    def model_importer(self,src_doc,target_doc):
        importer = Importer(src_doc,target_doc)
        names = []
        for i in src_doc.blocks:
            #print(i.name)
            names.append(i.name)
            importer.import_block(i.name)
        importer.finalize()
        return target_doc,names

    def wall_face(self,l,Thick,low,high):
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

    def draw_wall_3d(self,lis,layer,Thick=10,low=0,high=60):
        pf = self.msp.add_polyface(dxfattribs={'layer': layer})
        for l in lis:
            ans = self.wall_face(l,Thick,low,high)
            for i in ans:
                pf.append_face(i)

    def split_point(self,lis):
        split_p = []
        for i in lis:
            split_p.append((i[0],i[1]))
            split_p.append((i[2],i[3]))
        return split_p

    def draw_wd(self,lis,layer,Thick,low=0,high=60):
        bearing_wall = self.split_point(self.location['bearing_wall:'])
        not_bearing_wall = self.split_point(self.location['not_bearing_wall:'])
        for l in lis:
            long = abs(l[0]-l[2])+abs(l[1]-l[3])
            rotate, ang = 0, 0
            if abs(l[0]-l[2])<abs(l[1]-l[3]):
                rotate = 0
            ang = math.atan2((l[1]-l[3]),(l[0]-l[2]))/math.pi*180
            #print(ang)            
            if ((l[0],l[1]) in not_bearing_wall or (l[2],l[3]) in not_bearing_wall) and 500<long<1300:
                self.msp.add_blockref('单嵌板木门 12 - 800 x 2100mm-373023-_三维_',insert =(int((l[0]+l[2])/2),int((l[1]+l[3])/2)),dxfattribs={'xscale': long/820,'yscale': 1,'zscale': 1,'rotation':rotate+ang})
                self.draw_wall_3d([l],layer='A-WALL',Thick=Thick[0],low=2000,high=3000)
            #else:
            elif (l[0],l[1]) in bearing_wall or (l[2],l[3]) in bearing_wall:
                self.msp.add_blockref('推拉窗5 - 带贴面 - 900 x 1200mm-330476-_三维_',insert =(int((l[0]+l[2])/2),int((l[1]+l[3])/2)),dxfattribs={'xscale': long/920,'yscale':1,'zscale': 1,'rotation':rotate+ang})
                self.draw_wall_3d([l],layer='A-WALL',Thick=Thick[1],low=0,high=1000)
                self.draw_wall_3d([l],layer='A-WALL',Thick=Thick[1],low=2000,high=3000)
            else:
                self.draw_wall_3d([l],layer='A-WALL',Thick=Thick[0],low=0,high=3000)

    def get_rotation(self,tup):
        long = []
        for i in self.location['teapoy:']:
            long.append(abs((i[0]+i[2])/2-(tup[0]+tup[2])/2)+abs((i[1]+i[3])/2-(tup[1]+tup[3])/2))
        near_p = self.location['teapoy:'][long.index(min(long))]
        h = (near_p[0]+near_p[2])/2-(tup[0]+tup[2])/2
        w = (near_p[1]+near_p[3])/2-(tup[1]+tup[3])/2
        if (h < 0 and abs(w)<abs(h)) or (w > 0 and abs(w)>abs(h)):
            rotation = 180
        else:
            rotation = 0
        return rotation
        
    def draw_furn(self,lis,name,high = 0):
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
                if not 0.5*(sizes[name][0]+sizes[name][1])<(w+d)<2*(sizes[name][0]+sizes[name][1]):
                    continue
            if name == '双人床5 - W1680_D2256-343117-_三维_':
                dxfattrib['xscale'] = 0.8
                dxfattrib['yscale'] = 0.8
                self.msp.add_blockref(name,insert =(int((l[0]+l[2])/2+300),int((l[1]+l[3])/2),high),dxfattribs=dxfattrib)
            elif name == '三人沙发8 - W2010_D890_H850-349890-_三维_':
                dxfattrib['rotation'] += self.get_rotation(l)
                self.msp.add_blockref(name,insert =(int((l[0]+l[2])/2+300),int((l[1]+l[3])/2),high),dxfattribs=dxfattrib)
            else:
                self.msp.add_blockref(name,insert =(int((l[0]+l[2])/2),int((l[1]+l[3])/2),high),dxfattribs=dxfattrib)

    def draw_dxf(self):
        if not os.path.exists('./template/model.dxf'):
            src_doc = ezdxf.readfile('./template/wifi_dxf.dxf')
            doc = ezdxf.new()
            doc, names = self.model_importer(src_doc,doc)
            doc.saveas('./template/model.dxf')
        doc = ezdxf.readfile('./template/model.dxf')
        self.msp = doc.modelspace()
        ans = self.load_txt()
        #print(ans)
        labels = ['bearing_wall:','not_bearing_wall:','window-door:','bed:','teapoy:','sofa:','toilets:','kitchen:','desk:','tv:','locker:','wash:']
        self.draw_wall_3d(ans['bearing_wall:'],layer='A-WALL',Thick=0,low=0,high=3000)
        self.draw_wall_3d(ans['not_bearing_wall:'],layer='A-WALL',Thick=0,low=0,high=3000)
        self.draw_wd(ans['window-door:'],layer='A-WALL',Thick=[0,0],low=0,high=60)
        self.draw_furn(ans['bed:'],'双人床5 - W1680_D2256-343117-_三维_')
        self.draw_furn(ans['teapoy:'],'玻璃茶几 - 矩形2 - W1300_D700_H400-350883-_三维_')
        self.draw_furn(ans['sofa:'],'三人沙发8 - W2010_D890_H850-349890-_三维_')
        self.draw_furn(ans['toilets:'],'连体式座便器 - 污水出口到墙 305-339689-_三维_')
        self.draw_furn(ans['kitchen:'],'小厨房-中 - 1372mm-364451-_三维_')
        self.draw_furn(ans['desk:'],'西餐桌椅组合 - 1200x850x750mm 松木-353545-_三维_')
        self.draw_furn(ans['TV:'],'地柜1 - W1830 _D410_H400mm-355695-_三维_')
        self.draw_furn(ans['TV:'],'电视 - 平板 - 1270mm-354731-_三维_',high=400)
        self.draw_furn(ans['wash:'],'梳妆台柜 - 双门洗涤台 - 1234 x 590 x 800mm-365402-_三维_')
        doc.saveas(self.save_path)

if __name__ == '__main__':
    names = ['130','144']
    time_start = time.time()
    for name in names:
        dxfx = DXF(src_dxf=r'D:\Projects\BK\dxf\house\house\dxf\wifi_dxf.dxf',txt_path=r'C:\Users\zhangyichi\Desktop\location\\' + name + '.txt',save_path=name + '.dxf')
        dxfx.draw_dxf()
        print(name+' done in '+str(time.time() - time_start)+'s')
