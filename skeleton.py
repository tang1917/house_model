import cv2,time
import numpy as np


def cvShow(img):
    cv2.namedWindow('img',0)
    cv2.imshow('img',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def Three_element_add(array):
    array0 = array[:]
    array1 = np.append(array[1:],np.array([0]))
    array2 = np.append(array[2:],np.array([0, 0]))
    arr_sum = array0 + array1 + array2
    return arr_sum[:-2]


def VThin(image, array):
    NEXT = 1
    height, width = image.shape[:2]
    for i in range(1,height):
        M_all = Three_element_add(image[i])
        for j in range(1,width):
            if NEXT == 0:                   #如果某个点被删除了，则跳过它的有邻居
                NEXT = 1
            else:
                M = M_all[j-1] if j<width-1 else 1
                if image[i, j] == 0 and M != 0:
                    a = np.zeros(9)
                    if height-1 > i and width-1 > j:
                        kernel = image[i - 1:i + 2, j - 1:j + 2]
                        a = np.where(kernel == 255, 1, 0)
                        a = a.reshape(1, -1)[0]
                    NUM = np.array([1,2,4,8,0,16,32,64,128])
                    sumArr = np.sum(a*NUM)
                    sumArr = int(sumArr)
                    image[i][j] = array[sumArr] * 255
                    if array[sumArr] == 1:
                        NEXT = 0
    return image


def HThin(image, array):
    height, width = image.shape[:2]
    NEXT = 1
    for j in range(1,width):
        M_all = Three_element_add(image[:,j])
        for i in range(1,height):
            if NEXT == 0:
                NEXT = 1
            else:
                M = M_all[i-1] if i < height - 1 else 1
                if image[i, j] == 0 and M != 0:
                    a = np.zeros(9)
                    if height - 1 > i and width - 1 > j:
                        kernel = image[i - 1:i + 2, j - 1:j + 2]
                        a = np.where(kernel == 255, 1, 0)
                        a = a.reshape(1, -1)[0]
                    NUM = np.array([1, 2, 4, 8, 0, 16, 32, 64, 128])
                    sumArr = np.sum(a * NUM)
                    sumArr = int(sumArr)
                    image[i, j] = array[sumArr] * 255
                    if array[sumArr] == 1:
                        NEXT = 0
    return image


def Xihua(binary, num=10):
    image = binary.copy()
    #image = cv2.copyMakeBorder(binary_image, 1, 0, 1, 0, cv2.BORDER_CONSTANT, value=0)
    array = [0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1,\
         1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1,\
         0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1,\
         1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1,\
         1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\
         1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1,\
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\
         0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1,\
         1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1,\
         0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1,\
         1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,\
         1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\
         1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,\
         1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0,\
         1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0]

    for i in range(num):
        image = VThin(image, array)
        image = HThin(image, array)
    return image


