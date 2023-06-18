import cv2
import pydicom
import numpy as np
from pydicom.pixel_data_handlers import apply_windowing
import imageio
import multiprocessing as mp
import glob
import os

class Convert_dcm:
    def __init__(self, data, dict_path):
        self.df = data
        self.dict_path = dict_path
    def procees_dcm(self, path):
        
        dicom = pydicom.dcmread(path)
        # try : 
        img = dicom.pixel_array
        # except:
        #     # print(self.get_info())
           
        #     f.write(self.get_info())
        #     return 
            
        img = apply_windowing(img, dicom)
        img = (img - img.min()) / (img.max() - img.min())

        if dicom.PhotometricInterpretation == "MONOCHROME1":  
            img = 1 - img
        image = np.uint8(img * 255)
        return image
    def move(self, img, id_img):
        # path1 = f"D:\OneDrive - Industrial University of HoChiMinh City\WORKBASE\Project-rsna-breast-cancer-detection\RSNA_NOSIZE\{self.df.view[i]}_{self.df.image_id[i]}.png"
        # print(path1)
        # img = cv2.imread(path1)
        views = self.df[self.df.image_id == id_img].view.values[0]
        try:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        except:
            img = img
        # id_img = id_img.replace('_' , '_')
        imageio.imwrite(f'D:\OneDrive - Industrial University of HoChiMinh City\WORKBASE\Project-rsna-breast-cancer-detection\Meta_Image_origin\CMMD\{views}_{id_img}.png', img)
    def process1(self, id_img):
        # self.move(id)
        img = self.procees_dcm(self.dict_path[id_img])
        self.move(img, id_img)
    def my_method(self, ls):
        with mp.Pool(12) as p:
            p.map(self.process1, ls)