
def save(cancer_train, nocancer_train, cancer_val, nocancer_val, cancer_test, nocancer_test, name = "Rong",  name_folder = "Rong", view = None):
    path = f'E:\WORKBASE\Project-rsna-breast-cancer-detection\Data_main\CSV_MAIN\{name_folder}\{name}'
    os.makedirs(path)
    # print(len(cancer_train), len(nocancer_train))
    # print(nocancer_train)
    cancer_train =  cancer_train[["patient_id",	"image_id"	,"view",	"laterality"	,	"cancer"]]
    nocancer_train =  nocancer_train[["patient_id",	"image_id"	,"view",	"laterality"	,	"cancer"]]
    cancer_val =  cancer_val[["patient_id",	"image_id"	,"view",	"laterality"	,	"cancer"]]
    nocancer_val =  nocancer_val[["patient_id",	"image_id"	,"view",	"laterality"	,	"cancer"]]
    cancer_test =  cancer_test[["patient_id",	"image_id"	,"view",	"laterality"	,	"cancer"]]
    nocancer_test =  nocancer_test[["patient_id",	"image_id"	,"view",	"laterality"	,	"cancer"]]
    
    train = pd.concat([cancer_train, nocancer_train]).reset_index().drop('index', axis=1)
    val = pd.concat([cancer_val, nocancer_val]).reset_index().drop('index', axis=1)
    test = pd.concat([cancer_test, nocancer_test]).reset_index().drop('index', axis=1)
    # test = pd.read_csv(r'D:/OneDrive - Industrial University of HoChiMinh City/WORKBASE/Project-rsna-breast-cancer-detection\DATA_STANDARD\DDSM.csv', index_col='Unnamed: 0')
    ev = Evaluate(train, "Train")
    ev1 = Evaluate(val, "Val")
    ev2 = Evaluate(test, "Test")
    ev.show(f'{path}/description.txt')
    ev1.show(f'{path}/description.txt')
    ev2.show(f'{path}/description.txt')
    train.to_csv(f'{path}/train.csv')
    val.to_csv(f'{path}/val.csv')
    test.to_csv(f'{path}/test.csv')