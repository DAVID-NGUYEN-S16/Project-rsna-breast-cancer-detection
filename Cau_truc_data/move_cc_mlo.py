import cv2
import pydicom
import numpy as np
from pydicom.pixel_data_handlers import apply_windowing
import imageio
import multiprocessing as mp
import glob
import os
class move:
    def __init__(self, meta):
        self.meta = meta
    def process(self, i):
        par = self.meta.patient_id[i]
        view = self.meta.view[i]
        lat = self.meta.laterality[i]
        idimg = self.meta.image_id[i]
        path = f"D:\OneDrive - Industrial University of HoChiMinh City\WORKBASE\Project-rsna-breast-cancer-detection\Data_main\Dataset_VIEW\{par}\{view}\{lat}\{view}_{lat}_{idimg}.png"
        img = cv2.imread(path)
        imageio.imwrite(f'D:\OneDrive - Industrial University of HoChiMinh City\WORKBASE\Project-rsna-breast-cancer-detection\Data_main1\{view}\{view}_{lat}_{idimg}.png', img)
    def my_method(self, ls):
        with mp.Pool(12) as p:
            p.map(self.process, ls)
            