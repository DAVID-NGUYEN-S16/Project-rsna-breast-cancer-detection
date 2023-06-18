import cv2
import pydicom
import numpy as np
from pydicom.pixel_data_handlers import apply_windowing
import imageio
import multiprocessing as mp
import glob
import os
import matplotlib.pyplot as plt
from scipy import stats as sst
def crop_by_row(img, res):
    img_ori = res
    nb_row  = img.shape[0]
    ls = []
    # I will caculation quantity pixel 255 in a row (horizontal)
    for i in range(nb_row):
        x = np.sum(img[i, :])
        ls.append(x)
    
    vl = np.min(ls)
    y1 = nb_row
    y2 = 0
    # I will browse from middle to top position
    for i in range(int(nb_row/2), nb_row):
        if ls[i] <= vl:
            y1 = i
            break
    # I will browse from middle down last position
    for i in reversed(range(int(nb_row/2))):
        if ls[i] <= vl:
            y2 = i
            break
    return img_ori[y2: y1, :]
def crop_by_col(img, res):
    
    img_ori = res
    vl = np.sum(img[:, 0])
    nb_col  = img.shape[1]
    ls = []
    # I will caculation quantity pixel 255 in a col (vertical)
    for i in range(nb_col):
        x = np.sum(img[:, i])
        # find minimize values in total pixel x
        vl = min(vl, x)
        ls.append(x)
    
    if vl > img.shape[0]/3: 
        # Case breat very big, fill image 
        return img_ori

    ## Since there will be similar values, we will add an auxiliary amount to vl
    vl += 10
    # I will define breast at position left or right
    if (np.sum(img[:, 0: int(nb_col/2) ]) > np.sum(img[:, int(nb_col/2)+1 :  ])):
        L = 0
        for i in range(int(nb_col/4), nb_col):
            if ls[i] <= vl:

                img_ori = img_ori[:, : i + 50]
                return img_ori
    else :
        L = 1
        lens =  list(range(nb_col))[int(nb_col/4): ]
        for i in reversed(lens):
            if ls[i] <= vl:

                img_ori = img_ori[:, i-50: ]
                return img_ori
                
    return img_ori       
## show hist 
def process_crop(img):
 
    if len(img.shape)==3: 
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else : 
        gray = img
            
    # Blurring the image.
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    
    # Calculating the mean of the image, but it is ignoring the top and bottom 10% of the values.
    level = sst.trim_mean(gray.flatten(), 0.1) 
    
    # Thresholding the image.
    image_gray = cv2.threshold(gray, level, 255, cv2.THRESH_BINARY)[1]
    # Processed image white 
    imgcp = image_gray/255
    h, w = image_gray.shape
    if((h*w)-10 <= np.sum(imgcp)):

        image_gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    if((h*w)/2 >= np.sum(imgcp)):
        img = crop_by_col(imgcp, img)
#         print(img)
        img = crop_by_row(imgcp, img)
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
       
        name = self.df_main.image_id[id].replace('&', '_')
        path = f'D:/OneDrive - Industrial University of HoChiMinh City/WORKBASE/Project-rsna-breast-cancer-detection/DDSM/DICOM/{self.df_main.patient_id[id]}_{id}/{id}.dcm'
        if os.path.exists(path) == False:
            path = f'D:/OneDrive - Industrial University of HoChiMinh City/WORKBASE/Project-rsna-breast-cancer-detection/DDSM/DICOM/{self.df_main.patient_id[id]}_{id}/patient_id_{id}.dcm'
        self.path = path

        self.id = id
        
        return path
    def procees_dcm(self):

        dicom = pydicom.dcmread(self.path)

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

        file_name = f'D:/OneDrive - Industrial University of HoChiMinh City/WORKBASE/Project-rsna-breast-cancer-detection/Phan_tich/Origin/{self.df_main.image_id[id]}.png'
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
        new_image = self.procees_dcm()
        new_image = process_crop(new_image)
        self.save_image(new_image)
        return new_image
    
    def show(self, cl = 'gray'):
        fig, axs = plt.subplots(1, 2)
        origin_img = self.procees_dcm()
        # start = time.time()
        croped_img = self.crop_image(self.path)
        # end = time.time()
        file_name = self.path.split('/')
        id_img = int(file_name[-1].split('.')[0])
        target = {0: 'no-cancer', 1: 'cancer'}
        info = self.get_info()
        fig.suptitle(f'Id_img: {info[0]} \n Id_par: Id_par: {info[1]} \n State: {target[info[3]]} \n Views: {info[2]} \n Time = {end - start} \n\n')
        axs[0].imshow(origin_img, cmap='bone')
        axs[0].set_title('Origin')
        axs[1].imshow(croped_img, cmap='bone')
        axs[1].set_title('Croped image')
    def process1(self, i):
        self.set_path(i)
        # img = resize_img()
        self.crop_image_for_you()
        # self.crop_image()
    def my_method(self, ls):
        with mp.Pool(12) as p:
            p.map(self.process1, ls)
    
            
        
