import cv2
import imageio
import pandas as pd
import os
import multiprocessing as mp
# from drop_foryou import *
class move_image:
    def __init__(self, data, path=None):
        self.meta = data
        self.path_global = path
        
    def xx(self, id):
        par = self.meta.patient_id[id]
        lat = self.meta.laterality[id]
        view = self.meta.view[id]
        file_name = f"{self.path_global}/{self.meta.view[id]}_{self.meta.image_id[id]}.png"
        img = cv2.imread(file_name)
        
        if os.path.exists(f"E:/WORKBASE/Project-rsna-breast-cancer-detection/META_DATA/Data_image/{par}/") == False:
            os.mkdir(f"E:/WORKBASE/Project-rsna-breast-cancer-detection/META_DATA/Data_image/{par}/")
        if os.path.exists(f"E:/WORKBASE/Project-rsna-breast-cancer-detection/META_DATA/Data_image/{par}/{view}/") == False:
            os.mkdir(f"E:/WORKBASE/Project-rsna-breast-cancer-detection/META_DATA/Data_image/{par}/{view}/")
        if os.path.exists(f"E:/WORKBASE/Project-rsna-breast-cancer-detection/META_DATA/Data_image/{par}/{view}/{lat}/") == False:
            os.mkdir(f"E:/WORKBASE/Project-rsna-breast-cancer-detection/META_DATA/Data_image/{par}/{view}/{lat}/")
        # if os.path.exists(f"E:/WORKBASE/Project-rsna-breast-cancer-detection/META_DATA/Data_image/{par}/{lat}/{view}/") == False:
        #     os.mkdir(f"E:/WORKBASE/Project-rsna-breast-cancer-detection/META_DATA/Data_image/{par}/{lat}/{view}/")
        # # try:
        img = cv2.resize(img, (512, 512))
        # try:
        #     img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        # except:
        #     img = img
        # print(1)
        imageio.imwrite(f'E:/WORKBASE/Project-rsna-breast-cancer-detection/META_DATA/Data_image/{par}/{view}/{lat}/{view}_{lat}_{self.meta.image_id[id]}.png', img)

    def process_move(self, id):
        self.xx(id)
    def my_method(self, ls):
        with mp.Pool(12) as p:
            p.map(self.process_move, ls)
    