class Evaluate:
    def __init__(self, meta_pro, name):
        self.al_data = meta_pro.reset_index()
        self.name = name
    def quatity_cc_mlo(self):
        return f"\nSo luong CC và MLO\n{self.al_data.view.value_counts()}\n"
        # print(self.al_data.view.value_counts())
    def lelf_right(self):
        return f"\nSo luong L và R\n{self.al_data.groupby(['view', 'laterality']).size()}\n"
        # print(self.al_data.groupby(['view', 'laterality']).size())
    def show_one(self, par):
        return self.al_data[self.al_data.patient_id == par]
    def quanlity_cancer(self):
        sl = len(self.al_data[self.al_data.cancer == 1])
        slno = len(self.al_data[self.al_data.cancer == 0])
        return f"So luong img cancer: {sl} \n So luong img no cancer: {slno}"
        # print(self.al_data[self.al_data.cancer == 1])
    def show(self, path):
        ls = len(self.al_data)
        par = len(self.al_data.patient_id.unique())
        # print( 
        # self.quatity_cc_mlo()
        # self.lelf_right()
        # self.quanlity_cancer()
        f = open(path, 'a', encoding='utf-8')
        f.write(f'Dataset {self.name} \n Số lượng image: {ls} \n Số luong patient: {par} {self.quatity_cc_mlo()} {self.lelf_right()} {self.quanlity_cancer()}\n\n +++++++++++++++\n\n')
        f.close()