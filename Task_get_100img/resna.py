def process():
    path1 = f"D:\OneDrive - Industrial University of HoChiMinh City\WORKBASE\Project-rsna-breast-cancer-detection\RSNA_NOSIZE\{meta_pro.view[i]}_{meta_pro.image_id[i]}.png"
    # print(path1)
    img = cv2.imread(path1)
    try:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    except:
        img = img
    # id_img = id_img.replace('_' , '_')
    imageio.imwrite(f'D:\OneDrive - Industrial University of HoChiMinh City\WORKBASE\Project-rsna-breast-cancer-detection\Meta_Image_origin\RSNA\{meta_pro.view[i]}_{meta_pro.image_id[i]}.png', img)