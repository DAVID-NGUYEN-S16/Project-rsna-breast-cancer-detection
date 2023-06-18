import cv2
import pydicom
import numpy as np
from pydicom.pixel_data_handlers import apply_windowing
import imageio
import multiprocessing as mp
import glob
import os

from scipy import stats as sst
def cat_tia_row(img, res):
    ## find sum pixel min col
    img_ori = res
#     img = img/255
    nb_row  = img.shape[0]
    ls = []
    for i in range(nb_row):
        x = np.sum(img[i, :])
        ls.append(x)
    ## xet left right
    vl = 5
    y1 = nb_row
    y2 = 0
    for i in range(int(nb_row/2), nb_row):
        if ls[i] <= vl:
            y1 = i
            break
    for i in reversed(range(int(nb_row/2))):
        if ls[i] <= vl:
            y2 = i
            break
    return img_ori[y2: y1, :]
def cat_tia_col(img, res):
    ## find sum pixel min col
    img_ori = res
#     img = img/255
    vl = np.sum(img[:, 0])
    nb_col  = img.shape[1]
    ls = []
    for i in range(nb_col):
        x = np.sum(img[:, i])
        vl = min(vl, x)
        ls.append(x)
#     print(ls)
    if vl > img.shape[0]/3: 
#         print("No crop col")
        return img_ori
    ## xet left right

    ## vì sẽ có các giá trị tương tự nhau nên ta sẽ cộn một lượng phụ trợ vào vl
    vl += 10
    if (np.sum(img[:, 0: int(nb_col/2) ]) > np.sum(img[:, int(nb_col/2)+1 :  ])):
        L = 0
        for i in range(int(nb_col/4), nb_col):
            if ls[i] <= vl:
#                 print(f'Col = {i}, vl = {ls[i]}')
                img_ori = img_ori[:, : i]
                return img_ori
    else :
        L = 1
        lens =  list(range(nb_col))[int(nb_col/4): ]
        for i in reversed(lens):
            if ls[i] <= vl:
#                 print(f'Col = {i}, vl = {ls[i]}')
                img_ori = img_ori[:, i: ]
                return img_ori
                
    return img_ori       
## show hist 
def process_crop(img):
    # if len(img.shape) == 3: gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # else: gray = img
    # gray =  cv2.GaussianBlur(gray, (7, 7), 0)
    # # img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # image_gray = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)[1]
    
    ####
#     print(img.shape)
    if len(img.shape)==3: 
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else : gray = img
            
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    level = sst.trim_mean(gray.flatten(), 0.1) 
    image_gray = cv2.threshold(gray, level, 255, cv2.THRESH_BINARY)[1]
    
    imgcp = image_gray/255
    h, w = image_gray.shape
    if((h*w)-10 <= np.sum(imgcp)):

        image_gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    if((h*w)/2 >= np.sum(imgcp)):
        img = cat_tia_col(imgcp, img)
#         print(img)
        img = cat_tia_row(imgcp, img)
    img = cv2.resize(img, (512, 1024))
    try:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    except:
        img = img
    return img