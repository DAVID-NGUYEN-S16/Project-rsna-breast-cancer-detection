class Evaluate:
    def __init__(self, meta_pro, name):
        self.al_data = meta_pro.reset_index()
        self.name = name
    def quatity_cc_mlo(self):
        print("So luong CC và MLO")
        print(self.al_data.view.value_counts())
    def lelf_right(self):
        print("So luong L và R")
        print(self.al_data.groupby(['view', 'laterality']).size())
    def show_one(self, par):
        print(self.al_data[self.al_data.patient_id == par])
    def quanlity_cancer(self):
        sl = len(self.al_data[self.al_data.cancer == 1])
        print(f"So luong img cancer: {sl}")
        # print(self.al_data[self.al_data.cancer == 1])
    def show(self):
        ls = len(self.al_data)
        par = len(self.al_data.patient_id.unique())
        print(f'Dataset {self.name} \n Số lượng image: {ls} \n Số luong patient: {par}')
        self.quatity_cc_mlo()
        self.lelf_right()
        self.quanlity_cancer()