import os
import numpy as np
import torch
import torchvision
import cv2
import warnings
warnings.filterwarnings("ignore")

def test_pic(img,use_device='cpu'):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = torchvision.transforms.ToTensor()(img)
    # 加载训练好的模型
    model = torch.load(r'.\others\model.pt')
    # 关闭训练模式
    model.eval()

    model.to(use_device)

    with torch.no_grad():
        prediction = model([img.to(use_device)])
        del img
        rec = prediction[0]['boxes'].numpy().tolist()
        scores = prediction[0]['scores'].numpy().tolist()
        labels = prediction[0]['labels'].numpy().tolist()
        lab = ['bed','desk','sofa','kitchen','TV','toilets','wash','teapoy','write','locker','door','window']
        ans = {}
        for i in range(len(rec)):
            if scores[i] >= 0.45:
                ans[str(lab[labels[i]-1])] = ans.get(str(lab[labels[i]-1]),[])+[list(map(int,rec[i]))]
    '''
    fur = []
    for name,val in ans.items():
        if name != 'window' and name != 'door':
            fur.extend(val)
    '''
    if 'window' in ans.keys():
        del ans['window']
    if 'door' in ans.keys():
        del ans['door']
    #print(fur)
    return ans

if __name__ == '__main__':
    img = cv2.imread('./picture/144.jpg')
    print(img.shape)
    a = test_pic(img,use_device='cpu')
    print(a)