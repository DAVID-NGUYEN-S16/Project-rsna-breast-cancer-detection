import cv2
import imageio
import pandas as pd

meta = pd.read_csv(r'D:\OneDrive - Industrial University of HoChiMinh City\WORKBASE\Project-rsna-breast-cancer-detection\Data_main\CSV_MAIN\meta_data.csv')
def xx(id):
    file_name = f'D:/OneDrive - Industrial University of HoChiMinh City/WORKBASE/Project-rsna-breast-cancer-detection/Data_main/Meta_image/{meta.view[id]}_{meta.laterality[id]}_{meta.image_id[id]}.png'
    img = cv2.imread(file_name)
    # img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    # print(file_name)
    # print(img)
    imageio.imwrite(f"D:/OneDrive - Industrial University of HoChiMinh City/WORKBASE/Project-rsna-breast-cancer-detection/Data_main/Dataset_LAT/{meta.view[id]}_{meta.laterality[id]}_{meta.image_id[id]}.png", img)
def process_move(id):
    xx(id)