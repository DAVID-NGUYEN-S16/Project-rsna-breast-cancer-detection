import cv2
import os
import glob
import multiprocessing as mp

def find_id_max(numLabels, labels, stats, centroids, thresh):
    idmax = 0
    area  = stats[0, cv2.CC_STAT_AREA]/2
    for i in range(1, numLabels): 
        x = stats[i, cv2.CC_STAT_LEFT] 
        y = stats[i, cv2.CC_STAT_TOP] 
        w = stats[i, cv2.CC_STAT_WIDTH] 
        h = stats[i, cv2.CC_STAT_HEIGHT] 
        if x + w == thresh.shape[0] and y + h ==  thresh.shape[1] and x == 0 and y == 0:
            # print(f'{x + w} : {y + h} = {x} : {y}')
            continue
        if area < stats[i, cv2.CC_STAT_AREA]:
            # print(1)
            area = stats[i, cv2.CC_STAT_AREA] 
            idmax = i
    return idmax
f = open("demofile3.txt", "w")
def reprocess(image, select = 1):
    expen = 20
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    if select == 1:
        thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)[1]
    else : thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    numLabels, labels, stats, centroids = cv2.connectedComponentsWithStats(
                    thresh,
                    4,
                    cv2.CV_32S
    )

    idmax = find_id_max(numLabels, labels, stats, centroids, thresh)
    
    ######## CROP
    x = stats[idmax, cv2.CC_STAT_LEFT] 
    y = stats[idmax, cv2.CC_STAT_TOP] 
    w = stats[idmax, cv2.CC_STAT_WIDTH] 
    h = stats[idmax, cv2.CC_STAT_HEIGHT] 
    w_max =  image.shape[1]
    h_max =  image.shape[0] - 1
    ### Find y optimaztion
        # h, w, chance
    y_cur1 = y
    y_cur2 = y + h
    if x > 0:
        ### Find y optimaztion
        
        for i in range(y, 2):
            if gray[i][w_max-1] > 0:
                h+= y - i
                y = i 
                break
        while(h_max > 0  and gray[h_max][w_max-1] == 0):  h_max -= 2
        new_image = image[min(y_cur1,y): max( y_cur2, h_max) , max(0,x-expen) : ]
    else :
        for i in range(y, 2):
            if gray[i][0] > 0:
                h+= y - i
                y = i 
                break
        while(h_max > 0 and gray[h_max][0] == 0):  h_max -= 2
        new_image = image[min(y_cur1, y): max(y_cur2, h_max) , : min(w_max, x + w+ expen)]
    return new_image
def crop_image(path):
    # print(1111)
    image = cv2.imread(path)
    # print(image)
    name_image = os.path.split(path)[1]
    new_image = reprocess(image)
    file_name = f'Image_croped\{name_image}'
    try:
        
        # f.write(str(name_image) + '\n')
        # f.close()
        cv2.imwrite(file_name, new_image)
    except:
        new_image = reprocess(image, select=2)
        try:
            cv2.imwrite(file_name, new_image)
        except:
            f.write(str(name_image) + 'ngu \n')
# 
####-----Ss2-------------
# def find_id_max(numLabels, labels, stats, centroids, thresh):
#     idmax = 0
#     area = 0
#     for i in range(1, numLabels): 
#         x = stats[i, cv2.CC_STAT_LEFT] 
#         y = stats[i, cv2.CC_STAT_TOP] 
#         w = stats[i, cv2.CC_STAT_WIDTH] 
#         h = stats[i, cv2.CC_STAT_HEIGHT] 
#         if x + w == thresh.shape[0] and y + h ==  thresh.shape[1] and x == 0 and y == 0:
#             # print(f'{x + w} : {y + h} = {x} : {y}')
#             continue
#         if area < stats[i, cv2.CC_STAT_AREA]:
#             # print(1)
#             area = stats[i, cv2.CC_STAT_AREA] 
#             idmax = i
#     return idmax
# def crop_image(path):
#     image = cv2.imread(path)
#     name_image = os.path.split(path)[1]
#     expen = 50
#     if image is None:
#         expen = 50
#         image = cv2.imread(f'Image_512x512/{name_image}')
#     # print(path)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     gray = cv2.GaussianBlur(gray, (7, 7), 0)
#     thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)[1]
   
    
    
#     numLabels, labels, stats, centroids = cv2.connectedComponentsWithStats(
#                     thresh,
#                     4,
#                     cv2.CV_32S
#     )

#     idmax = find_id_max(numLabels, labels, stats, centroids, thresh)
    
#     ######## CROP
#     x = stats[idmax, cv2.CC_STAT_LEFT] 
#     y = stats[idmax, cv2.CC_STAT_TOP] 
#     w = stats[idmax, cv2.CC_STAT_WIDTH] 
#     h = stats[idmax, cv2.CC_STAT_HEIGHT] 
#     w_max =  image.shape[1]
#     h_max =  image.shape[0] - 1
#     ### Find y optimaztion
#         # h, w, chance
#     y_cur1 = y
#     y_cur2 = y + h
#     if x > 0:
#         ### Find y optimaztion
        
#         for i in range(y, 2):
#             if gray[i][w_max-1] > 0:
#                 h+= y - i
#                 y = i 
#                 break
#         while(h_max > 0  and gray[h_max][w_max-1] == 0):  h_max -= 2
#         new_image = image[min(y_cur1,y): max( y_cur2, h_max) , max(0,x-expen) : ]
#     else :
#         for i in range(y, 2):
#             if gray[i][0] > 0:
#                 h+= y - i
#                 y = i 
#                 break
#         while(h_max > 0 and gray[h_max][0] == 0):  h_max -= 2
#         new_image = image[min(y_cur1, y): max(y_cur2, h_max) , : min(w_max, x + w+ expen)]
#     file_name = f'Image_croped\{name_image}';
#     # print(file_name)
#     try:
#         cv2.imwrite(file_name, new_image)
    
#     except:
#         f = open("demofile3.txt", "w")
#         f.write(str(name_image))
#         f.close()
#         return 
    # cv2.imwrite(file_name, new_image)
    

####-----Ss1-------------
# import cv2
# import os
# import glob
# def find_id_max(numLabels, labels, stats, centroids, thresh):
#     idmax = 0
#     area = 0
#     for i in range(1, numLabels): 
#         x = stats[i, cv2.CC_STAT_LEFT] 
#         y = stats[i, cv2.CC_STAT_TOP] 
#         w = stats[i, cv2.CC_STAT_WIDTH] 
#         h = stats[i, cv2.CC_STAT_HEIGHT] 
#         if x + w == thresh.shape[0] and y + h ==  thresh.shape[1] and x == 0 and y == 0:
#             # print(f'{x + w} : {y + h} = {x} : {y}')
#             continue
#         if area < stats[i, cv2.CC_STAT_AREA]:
#             # print(1)
#             area = stats[i, cv2.CC_STAT_AREA] 
#             idmax = i
#     return idmax
# def crop_image(path):
#     image = cv2.imread(path)
#     print(path)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     gray = cv2.GaussianBlur(gray, (7, 7), 0)
#     thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)[1]
#     name_image = os.path.split(path)[1]
#     numLabels, labels, stats, centroids = cv2.connectedComponentsWithStats(
#                     thresh,
#                     4,
#                     cv2.CV_32S
#     )

#     idmax = find_id_max(numLabels, labels, stats, centroids, thresh)
    
#     ######## CROP
#     x = stats[idmax, cv2.CC_STAT_LEFT] 
#     y = stats[idmax, cv2.CC_STAT_TOP] 
#     w = stats[idmax, cv2.CC_STAT_WIDTH] 
#     h = stats[idmax, cv2.CC_STAT_HEIGHT] 
#     w_max =  image.shape[1]
#     h_max =  image.shape[0] - 1
#     ### Find y optimaztion
#         # h, w, chance
#     if x > 0:
#         ### Find y optimaztion
#         for i in range(y, 2):
#             if gray[i][w_max-1] > 0:
#                 h+= y - i
#                 y = i 
#                 break
#         while(gray[h_max][w_max-1] == 0):  h_max -= 2
#         new_image = image[y: h_max , max(0,x-150) : ]
#     else :
#         for i in range(y, 2):
#             if gray[i][0] > 0:
#                 h+= y - i
#                 y = i 
#                 break
#         while(gray[h_max][0] == 0):  h_max -= 2
#         new_image = image[y: h_max , : min(w_max, x + w+ 150)]
#     file_name = f'Image_croped\{idmax}_{name_image}';
#     # print(file_name)
#     cv2.imwrite(file_name, new_image)
    