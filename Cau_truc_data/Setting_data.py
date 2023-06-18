import numpy as np
import pandas as pd
import multiprocessing as mp
class Setting_data:
    def __init__(self, data):
        
        self.data= data[['patient_id', 'image_id', 'view', 'laterality','status']]
        
        self.id = 0
        self.par = 0
        self.group = None
        
        
        self.meta_pro = []
    def set_par(self, par):
        self.par = par
    ## Zip columns img and cancer
    def zip_idimg_cancer(self):
        # Tạo id_img_zip để tận dụng cancer để sort xử lý ưu tiênc
        '''
        Chú ý dữ liệu phải được resetindex trước kh xử lý 
        '''
        self.data['id_img_zip'] = None
        for i in range(len(self.data)):
            # print(f'{self.data.cancer[i]}_{self.data.image_id[i]}')
            self.data.id_img_zip[i] = f'{self.data.status[i]}_{self.data.image_id[i]}'
        # ## Nhóm dữ liệu lại để xử lý
        self.group = self.data.groupby(['patient_id', 'view', 'laterality', 'id_img_zip']).size()
        self.data = self.data[(self.data.view == 'CC') |(self.data.view == 'MLO')]
        
    
    # Hàm filter_for2x là hàm dùng để cân bằng dữ liệu
    def filter_for_2x(self, par, lat):
        
        A = list(self.group[par]['CC'][lat].index)
        B = list(self.group[par]['MLO'][lat].index)
        
        A = sorted(A, key=lambda x: x[0],  reverse=True)# ls[0][0]
        B = sorted(B, key=lambda x: x[0],  reverse=True)# ls[0][0]
        i = 0
        j = 0
        # print(A)
        # print(B)
        while i < len(A) and j < len(B):
            a = A[i]
            b = B[i]
            # print(f"Lay a: {a.split('_')} \n lay b:{a.split('_')}")
            cancer_a, a = a.split('_')
            cancer_b, b = b.split('_')
            # print(a, b)
            ## update data
            # return
            
            self.meta_pro.append(a)
            # return
            self.meta_pro.append(b)
            
            self.id+=2
            i+=1
            j+=1
  
    def check_cancer(self, par, views, lat):
        try: 
            return len(self.group[par][views][lat].index) >0
        except:
            return False
    def filter_main(self, par, lat):
        # Kiểm tra nếu CC + lat và MLO + lat mà đều chứa hình ảnh true
        if self.check_cancer(par, 'CC', lat) and self.check_cancer(par, 'MLO', lat):
           self.filter_for_2x(par, lat=lat)

            
    # def save_file(self, path):
    #     self.meta_pro.to_csv(path)
    def procee_par(self, par):
        ## Process img R
    
        self.filter_main(par, lat='R')

        ## Process img L
        self.filter_main(par, lat='L')
    def process_multi(self, par):
        # print(par)
        self.procee_par(par)
    def multi_process(self, list_par):
        self.zip_idimg_cancer()
        for i in list_par:
            self.procee_par(i)

    