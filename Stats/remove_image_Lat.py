import cv2
import imageio
import pandas as pd
import os
meta = pd.read_csv(r'D:\OneDrive - Industrial University of HoChiMinh City\WORKBASE\Project-rsna-breast-cancer-detection\Data_main\CSV_MAIN\meta_data.csv')
def xx(id):
    file_name = f'D:/OneDrive - Industrial University of HoChiMinh City/WORKBASE/Project-rsna-breast-cancer-detection/Meta_image/{meta.view[id]}_{meta.laterality[id]}_{meta.image_id[id]}.png'
    img = cv2.imread(file_name)
    print(img)
    # img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    # print(file_name)
    # print(img)
    par = meta.patient_id[id]
    lat = meta.laterality[id]
    view = meta.view[id]
    if os.path.exists(f"D:/OneDrive - Industrial University of HoChiMinh City/WORKBASE/Project-rsna-breast-cancer-detection/Data_main/Dataset_LAT/{par}/") == False:
        os.mkdir(f"D:/OneDrive - Industrial University of HoChiMinh City/WORKBASE/Project-rsna-breast-cancer-detection/Data_main/Dataset_LAT/{par}/")
    if os.path.exists(f"D:/OneDrive - Industrial University of HoChiMinh City/WORKBASE/Project-rsna-breast-cancer-detection/Data_main/Dataset_LAT/{par}/{lat}/") == False:
        os.mkdir(f"D:/OneDrive - Industrial University of HoChiMinh City/WORKBASE/Project-rsna-breast-cancer-detection/Data_main/Dataset_LAT/{par}/{lat}/")
    if os.path.exists(f"D:/OneDrive - Industrial University of HoChiMinh City/WORKBASE/Project-rsna-breast-cancer-detection/Data_main/Dataset_LAT/{par}/{lat}/{view}/") == False:
        os.mkdir(f"D:/OneDrive - Industrial University of HoChiMinh City/WORKBASE/Project-rsna-breast-cancer-detection/Data_main/Dataset_LAT/{par}/{lat}/{view}/")
    # try:
    imageio.imwrite(f"D:/OneDrive - Industrial University of HoChiMinh City/WORKBASE/Project-rsna-breast-cancer-detection/Data_main/Dataset_LAT/{par}/{lat}/{view}/{meta.view[id]}_{meta.laterality[id]}_{meta.image_id[id]}.png", img)

def process_move(id):
    xx(id)