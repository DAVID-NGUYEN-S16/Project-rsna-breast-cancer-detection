import numpy as np
import pandas as pd
import multiprocessing as mp
class Setting_data:
    def __init__(self, data):
        
        self.data= data[['patient_id', 'image_id', 'view', 'laterality', 'age', 'cancer']]
        
        self.id = 0
        self.par = 0
        self.group = None
        
        
        self.meta_pro = pd.DataFrame(columns=['patient_id', 'image_id', 'view', 'laterality', 'age', 'cancer'])
    def set_par(self, par):
        self.par = par
    ## Zip columns img and cancer
    def zip_idimg_cancer(self):
        # Tạo id_img_zip để tận dụng cancer để sort xử lý ưu tiênc
        self.data['id_img_zip'] = None
        for i in range(len(self.data)):
            self.data['id_img_zip'][i] = f'{self.data.cancer[i]}_{self.data.image_id[i]}'
        ## Nhóm dữ liệu lại để xử lý
        self.group = self.data.groupby(['patient_id', 'view', 'laterality', 'id_img_zip', 'age']).size()
        self.data = self.data[(self.data.view == 'CC') |(self.data.view == 'MLO')]
        
    # Hàm filter_for1x là hàm dùng để kiểm tra các trường hợp lẽ của view và lat
    def filter_for1x(self,par, views, lat, i, A):
        # A = list(self.group[par][views][lat].index)
        dic = {'CC': 'MLO', 'MLO': 'CC'}
        while i < len(A):   
            # Kiểm tra nó có phải là 1 hay không vì chỉ có th 1 mới thêm ảnh
            if A[i][0].split('_')[0] == '1':
                a, age_a = A[i]
                cancer_a, a = a.split('_')
            
                ## update data origin

                self.meta_pro.loc[self.id] = [par, a, views, lat, age_a, int(cancer_a)]
                ## update data new fake
                self.meta_pro.loc[self.id+1] = [par, a, dic[views], lat, age_a, 0]
                self.id+=2
            i+=1
    # Hàm filter_for2x là hàm dùng để cân bằng dữ liệu
    def filter_for_2x(self, par, lat):
        A = list(self.group[par]['CC'][lat].index)
        B = list(self.group[par]['MLO'][lat].index)
        A = sorted(A, key=lambda x: x[0],  reverse=True)# ls[0][0]
        B = sorted(B, key=lambda x: x[0],  reverse=True)# ls[0][0]
        i = 0
        j = 0
        print(A)
        print(B)
        while i < len(A) and j < len(B):
            a, age_a = A[i]
            b, age_b = B[i]
            cancer_a, a = a.split('_')
            cancer_b, b = b.split('_')
            print(a, b)
            ## update data
            self.meta_pro.loc[self.id] = [par, a, 'CC', lat, age_a, int(cancer_a)]
            
            self.meta_pro.loc[self.id+1] = [par, b, 'MLO', lat, age_b, int(cancer_b)]
            self.id+=2
            i+=1
            j+=1
            ## Kiem tra luong thua
        # print(i, j)
        self.filter_for1x(par, 'CC', lat, i, A)
        self.filter_for1x(par, 'MLO', lat, j, B)
    def check_cancer(self, par, views, lat):
        try: 
            return len(self.group[par][views][lat].index) >0
        except:
            return False
    def filter_main(self, par, lat):
        # Kiểm tra nếu CC + lat và MLO + lat mà đều chứa hình ảnh true
        if self.check_cancer(par, 'CC', lat) and self.check_cancer(par, 'MLO', lat):
           self.filter_for_2x(par, lat=lat)
        elif  self.check_cancer(par, 'CC', lat) :
            ## Xử lý trường hợp dư ảnh
            # Xuất hiện 2 trường hợp là có cancer và ko có cancer
            A = list(self.group[par]['CC'][lat].index)
            self.filter_for1x(par, 'CC', lat=lat, i=0, A=A)
            
        elif  self.check_cancer(par, 'MLO', lat) :
            B = list(self.group[par]['MLO'][lat].index)
            self.filter_for1x(par, 'MLO', lat=lat, i=0, A=B)
            
    def save_file(self, path):
        self.meta_pro.to_csv(path)
    def procee_par(self, par):
        ## Process img R
    
        self.filter_main(par, lat='R')

        ## Process img L
        self.filter_main(par, lat='L')
    def process_multi(self, par):
        print(par)
        self.procee_par(par)
    def multi_process(self, list_par):
        self.zip_idimg_cancer()
        for i in list_par:
            self.procee_par(i)
        # with mp.Pool(12) as p:
        #     p.map(self.process_multi, list_par) 
    