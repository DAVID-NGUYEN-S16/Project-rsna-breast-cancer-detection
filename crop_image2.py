import cv2
import os
import glob
import multiprocessing as mp
import numpy as np

def find_id_max(numLabels, labels, stats, centroids, thresh):
    idmax = 0
    sum_pixel = np.sum(thresh)/3
    for i in range(1, numLabels): 
        x = stats[i, cv2.CC_STAT_LEFT] 
        y = stats[i, cv2.CC_STAT_TOP] 
        w = stats[i, cv2.CC_STAT_WIDTH] 
        h = stats[i, cv2.CC_STAT_HEIGHT] 
        if x + w == thresh.shape[0] and y + h ==  thresh.shape[1] and x == 0 and y == 0:
            continue
        if sum_pixel < np.sum(thresh[y:y+h, x : x+ w]):
            idmax = i
            sum_pixel= np.sum(thresh[y:y+h, x : x+ w])
    return idmax
def reprocess(image, select = 1):
    expen = 20
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    if select == 1:
        thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)[1]
    else : 
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    numLabels, labels, stats, centroids = cv2.connectedComponentsWithStats(
                    thresh,
                    4,
                    cv2.CV_32S
    )

    idmax = find_id_max(numLabels, labels, stats, centroids, thresh)
    print(idmax)
    ######## CROP
    x = stats[idmax, cv2.CC_STAT_LEFT] 
    y = stats[idmax, cv2.CC_STAT_TOP] 
    w = stats[idmax, cv2.CC_STAT_WIDTH] 
    h = stats[idmax, cv2.CC_STAT_HEIGHT] 
    w_max =  image.shape[1]
    h_max =  image.shape[0] - 1
    if x > 0:
       
        new_image = image[y: y+h , max(0,x-expen) : ]
    else :
        new_image = image[y: y+h , : min(w_max, x + w+ expen)]
    return new_image
f = open("demofile3.txt", "w")

def crop_image(path):
   
    image = cv2.imread(path)
    name_image = os.path.split(path)[1]
    new_image = reprocess(image)
    file_name = f'Image_croped\{name_image}';
    try:
        cv2.imwrite(file_name, new_image)
    except:
        new_image = reprocess(image, select=2)
        # print(name_image)
        # cv2.imwrite(file_name, new_image)
        try:
            cv2.imwrite(file_name, new_image)
        except:
            f.write(str(name_image) + 'ngu \n')
