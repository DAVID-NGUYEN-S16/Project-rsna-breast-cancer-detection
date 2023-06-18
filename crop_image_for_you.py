import cv2
import pydicom
import numpy as np
from pydicom.pixel_data_handlers import apply_windowing
import imageio
import multiprocessing as mp
import glob
import os

from scipy import stats as sst
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
f = open("demofile3.txt", "w")

class Process_Data():
    def __init__(self, df_main, head = 'train_images' ):
        self.df_main = df_main
        self.path = None
        self.head = head
        self.id = None
        
    def set_path(self, id):
        # path = f'DDSM/DICOM/DICOM/{self.df_main.patient_id[id]}_{id}/{self.df_main.image_id[id]}.dcm'
        # path = glob.glob(f'VinDr-Mammo_Origin_image/CC_L/{self.df_main.Series_Instance_UID[id]}.png')[0]
        # name_path = os.path.basename(path)
        # View_Position = self.df_main.View_Position[id]
        # Image_Laterality = self.df_main.LeftRight[id]
        # path = self.df_main['File Location'][id]
        # path = meta_china['File Location'][i].replace('\\', '/').replace('.', '', 1)
        # idimg = 'SOP_Instance_UID.1'
        # path = f'D:/OneDrive - Industrial University of HoChiMinh City/WORKBASE/Project-rsna-breast-cancer-detection/VinDr-Mammo_Origin_image/VinDr-Mammo_Origin_image/{self.df_main.view[id]}_{self.df_main.laterality[id]}/{self.df_main.image_id[id]}.png'

        # path = self.df_main.path_img[id]
        name = self.df_main.image_id[id].replace('&', '_')
        path = f'D:/OneDrive - Industrial University of HoChiMinh City/WORKBASE/Project-rsna-breast-cancer-detection/DDSM/DICOM/{self.df_main.patient_id[id]}_{id}/{id}.dcm'
        if os.path.exists(path) == False:
            path = f'D:/OneDrive - Industrial University of HoChiMinh City/WORKBASE/Project-rsna-breast-cancer-detection/DDSM/DICOM/{self.df_main.patient_id[id]}_{id}/patient_id_{id}.dcm'
        self.path = path
        # print(path)
        self.id = id
        
        return path
        
    def find_id_max(self, numLabels, labels, stats, centroids, thresh):
        idmax = 0
        total = np.sum(thresh)
        sum_pixel = total/4

        density_ar = total/(thresh.shape[0]*thresh.shape[1]);
        for i in range(0, numLabels): 
            x = stats[i, cv2.CC_STAT_LEFT] 
            y = stats[i, cv2.CC_STAT_TOP] 
            w = stats[i, cv2.CC_STAT_WIDTH] 
            h = stats[i, cv2.CC_STAT_HEIGHT] 

            sums = np.sum(thresh[y:y+h, x : x+ w])
            density_e = sums/ ((y+h)* (x+w))
            if sum_pixel <= sums and density_e >= density_ar :
                idmax = i
                density_ar  = density_e
        return idmax
        
    def ConnectedComponents(self, image, size = (1024, 1024, 3) ):
        expen = 5
        if len(image.shape)==3: gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else : gray = image
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        level = sst.trim_mean(gray.flatten(), 0.1) 
        thresh = cv2.threshold(gray, level, 255, cv2.THRESH_BINARY)[1]

        numLabels, labels, stats, centroids = cv2.connectedComponentsWithStats(
                        thresh,
                        4,
                        cv2.CV_32S
        )
        idmax = self.find_id_max(numLabels, labels, stats, centroids, thresh)
        x = stats[idmax, cv2.CC_STAT_LEFT] 
        y = stats[idmax, cv2.CC_STAT_TOP] 
        w = stats[idmax, cv2.CC_STAT_WIDTH] 
        h = stats[idmax, cv2.CC_STAT_HEIGHT] 

        w_max =  image.shape[1]
        h_max =  image.shape[0] - 1

        thresh = thresh/255
        if (np.sum(thresh[:, 0: int(w_max/2) ]) < np.sum(thresh[:, int(w_max/2)+1 :  ])):

            new_image = image[y: y+h , max(0,x-expen) : ]
        else :
            new_image = image[y: y+h , : min(w_max, x + w+ expen)]
        new_image = cv2.resize(new_image, (512, 1024))
        return new_image
    
    def procees_dcm(self):

        dicom = pydicom.dcmread(self.path)
        # try : 
        img = dicom.pixel_array
            
        img = apply_windowing(img, dicom)
        img = (img - img.min()) / (img.max() - img.min())

        if dicom.PhotometricInterpretation == "MONOCHROME1":  
            img = 1 - img
        image = np.uint8(img * 255)
        return image
    def get_info(self):
        
        id =self.id
        id_img = self.df_main.image_id[id]
        
        id_par = self.df_main.patient_id[id]
        view_position = self.df_main.view[id]
        cancer = 1
        return [id_img, id_par, view_position, view_position]
    def save_image(self, img):
        id = self.id

        file_name = f'D:/OneDrive - Industrial University of HoChiMinh City/WORKBASE/Project-rsna-breast-cancer-detection/Phan_tich/connected_compont/{self.df_main.image_id[id]}.png'
        f.write(file_name)
        imageio.imwrite(file_name, img)
    def resize_img(self, img):
        img = cv2.resize(img, (512, 1024))
        try:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        except:
            img = img
        return img
    def crop_image(self, size=(1024, 1024, 3)):
        new_image = self.procees_dcm()
        new_image = self.ConnectedComponents(new_image)
        self.save_image(new_image)
        return new_image
    def crop_image_for_you(self, size=(1024, 1024, 3)):
        # Reading the dicom file and converting it to a numpy array.
        new_image = self.procees_dcm()
        new_image = self.ConnectedComponents(new_image)
        # new_image = cv2.imread(self.path)
        # print(new_image)
        # print(self.path)
        # new_image = process_crop(new_image)
        # new_image = self.resize_img(new_image)
        self.save_image(new_image)
        return new_image
    def loc_cancer(self, name):
        data = self.df_main
        df = data[data['cancer'] == 1].patient_id
        df = df.unique()
        data = data[data['patient_id'].isin(df)]
        data = data.reset_index()
        data.to_csv(f'{name}.csv')
    def process1(self, i):
        self.set_path(i)
        # img = resize_img()
        self.crop_image_for_you()
        # self.crop_image()
    def my_method(self, ls):
        with mp.Pool(12) as p:
            p.map(self.process1, ls)
    
            
        
