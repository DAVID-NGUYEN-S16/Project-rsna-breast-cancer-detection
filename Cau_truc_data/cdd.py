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
        # name = self.meta.image_id[i].replace('-', '_')
        pat = self.meta.fullPath[i]
        path = f"E:\WORKBASE\Project-rsna-breast-cancer-detection\MINI-DDSM-Complete-PNG-16\{pat}"
        img = cv2.imread(path)
        imageio.imwrite( f'E:\WORKBASE\Project-rsna-breast-cancer-detection\DATA_STANDARD\DDSM\{view}_{idimg}_{par}.png', img)
    def my_method(self, ls):
        with mp.Pool(12) as p:
            p.map(self.process, ls)