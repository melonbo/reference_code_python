import cv2
import numpy as np
import sys
import os
# import sets
import multiprocessing
 
def shrink(cv_img):
    mask = cv_img>0
    coords = np.argwhere(mask)
    if len(cv_img.shape)==3:
        y0,x0,_ = coords.min(axis = 0)
        y1,x1,_ = coords.max(axis = 0)+1
        new_img = cv_img[y0:y1,x0:x1,:]
    else:
        y0,x0 = coords.min(axis = 0)
        y1,x1 = coords.max(axis = 0)+1
        new_img = cv_img[y0:y1,x0:x1]
    return new_img
 
 
# logo_path = '2logo_demo/'
logo_path = '/media/crx/4f5a4954-cbbd-46a9-9c48-aeb156476154/netease/file/1program/3ad/0banzheng/pachongpic/google/2logo_v6集合/kuang_dianzi/'
 
#logo_name_list = [os.path.join(logo_path, logo_name) for logo_name in os.listdir(logo_path) if os.path.isfile(os.path.join(logo_path, logo_name))]
logo_name_list = []
for root,dirs,files in os.walk(logo_path):
    for f in files:
        path = os.path.join(root,f)
        if os.path.isfile(path):
            logo_name_list.append(path)
'''
logo_list = {}
for logo_name in logo_name_list:
    for logo in LOGO_LIST:
        if logo in logo_name:
            if logo not in logo_list:
                logo_list[logo] = [logo_name]
            else:
                logo_list[logo].append(logo_name)
            break
'''
savedir = logo_path+'output/'
print(savedir)
 
def start(begin,end):
    for i in range(begin,end):
        image_name = logo_name_list[i]
        print(image_name)
        try:
            img = cv2.imread(image_name,-1)
            new_img = shrink(img)
            cv2.imwrite(image_name,new_img)
        except:
            print('error!')
            os.remove(image_name)
            continue
 
multiprocess=2
# if multiprocess:
# 	num_workers = 4
# 	part = int(len(logo_name_list)/num_workers)
# 	id_min = [i*part for i in range(num_workers)]
# 	id_max = [(i+1)*part for i in range(num_workers)]
# 	pool = multiprocessing.Pool(processes=num_workers)
# 	for i in range(num_workers):
# 		pool.apply_async(start,args=(id_min[i], id_max[i]))
# 	pool.close()
# 	pool.join()
# else:
# 	start(0,len(logo_name_list))
 
start(0,len(logo_name_list))
