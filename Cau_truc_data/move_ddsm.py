import cv2
import imageio
import pandas as pd
import os
import multiprocessing as mp
meta = pd.read_csv('ddsm.csv')
def xx(id):
        file_name = f'D:\OneDrive - Industrial University of HoChiMinh City\WORKBASE\Project-rsna-breast-cancer-detection\MINI-DDSM-Complete-PNG-16\{meta.fullPath[id]}'
        img = cv2.imread(file_name)

        par = meta.patient_id[id]
        lat = meta.laterality[id]
        view = meta.view[id]
        
        imageio.imwrite(f"D:/OneDrive - Industrial University of HoChiMinh City/WORKBASE/Project-rsna-breast-cancer-detection/DATA_STANDARD/DDSM/{meta.view[id]}_{meta.laterality[id]}_{meta.image_id[id]}.png", img)
def process_move( id):
        xx(id)
def my_method( ls):
    with mp.Pool(12) as p:
        p.map(process_move, ls)
    