import os, sys, shutil
import numpy as np
import glob
from PIL import Image
from scipy.misc import imread
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cv2
import random
import string
sys.path.append(os.path.join(os.getcwd(),'python/'))

import darknet as dn
import pdb
from datetime import datetime

#Load config files
def detect_image(imagepath, filepath, dest):
  dn.set_gpu(0)
  net = dn.load_net(b"./yolov3.cfg", b"./yolov3.weights", 0)
  meta = dn.load_meta(b"./coco.data")

  #Raw folder path
  #folder_raw = "/home/manish/Downloads/darknet/data/raw"
  #files = os.listdir(folder_raw)

  #Classified folder path
  static = "./static/img"
  count = 0
  file1 = open(os.path.join(static,datetime.now().strftime("%Y%m%d-%H%M%S")+".txt"),"w")

  labels_list = ['person','bicycle','car','motorbike','aeroplane','bus','train','truck','boat','traffic light','fire hydrant','stop sign','parking meter','bench','bird','cat','dog','horse','sheep','cow','elephant','bear','zebra','giraffe','backpack','umbrella','handbag','tie','suitcase','frisbee','skis','snowboard','sports ball','kite','baseball bat','baseball glove','skateboard','surfboard','tennis racket','bottle','wine glass','cup','fork','knife','spoon','bowl','banana','apple','sandwich','orange','broccoli','carrot','hot dog','pizza''donut','cake','chair','sofa','pottedplant','bed','diningtable','toilet','tvmonitor','laptop','mouse','remote','keyboard','cell phone','microwave','oven','toaster','sink','refrigerator','book','clock','vase','scissors','teddy bear','hair drier','toothbrush']
  #labels_list = 'objdata'
  font = cv2.FONT_HERSHEY_SIMPLEX
  chart_colors = [(204,102,51),(18,557,220),(0,153,255),(24,150,16),(175,175,246),(172,62,59),(198,153,0),(172,62,59),(18,557,220),(0,153,255),(204,102,51),(18,557,220),(0,153,255),(24,150,16),(175,175,246),(172,62,59),(198,153,0),(172,62,59),(18,557,220),(0,153,255),(204,102,51),(18,557,220),(0,153,255),(24,150,16),(175,175,246),(172,62,59),(198,153,0),(172,62,59),(18,557,220),(0,153,255),(204,102,51),(18,557,220),(0,153,255),(24,150,16),(175,175,246),(172,62,59),(198,153,0),(172,62,59),(18,557,220),(0,153,255),(204,102,51),(18,557,220),(0,153,255),(24,150,16),(175,175,246),(172,62,59),(198,153,0),(172,62,59),(18,557,220),(0,153,255),(204,102,51),(18,557,220),(0,153,255),(24,150,16),(175,175,246),(172,62,59),(198,153,0),(172,62,59),(18,557,220),(0,153,255),(204,102,51),(18,557,220),(0,153,255),(24,150,16),(175,175,246),(172,62,59),(198,153,0),(172,62,59),(18,557,220),(0,153,255),(204,102,51),(18,557,220),(0,153,255),(24,150,16),(175,175,246),(172,62,59),(198,153,0),(172,62,59),(18,557,220),(0,153,255)]
 
  #Perform detection for every image in the files list
  #for f in files:
<<<<<<< HEAD
  if imagepath.endswith(".jpg") or imagepath.endswith(".jpeg") or imagepath.endswith(".png"):
=======
  if imagepath.endswith(".jpg") or imagepath.endswith(".jpeg") or imagepath.endswith(".png") or imagepath.endswith(".heic") or imagepath.endswith(".tiff") or imagepath.endswith(".HEIC"):
>>>>>>> ae2165a48199206d3660c20523c0e905ef026e9c
          print (imagepath)
          image_cv2 = cv2.imread(os.path.join(imagepath),cv2.IMREAD_COLOR)
          image_path = bytes(os.path.join(imagepath).encode("utf-8"))
          r = dn.detect(net, meta, imagepath)
          print (r)
          cnt = 0
          if r != []:
              while cnt < len(r):
                    name = r[cnt][0]
                    if name in labels_list:
                          i = labels_list.index(name)
                    predict = r[cnt][1]
                    #prob = name+":"+str(predict)*100+"%"
                    x = r[cnt][2][0]
                    y = r[cnt][2][1]
                    w = r[cnt][2][2]
                    z = r[cnt][2][3]
                    #print (x, y, w, z)

                    x_max = int(round((2*x+w)/2))
                    x_min = int(round((2*x-w)/2))
                    y_min = int(round((2*y-z)/2))
                    y_max = int(round((2*y+z)/2))
                    print (x_min, y_min, x_max, y_max)
                    pixel_list = [ x_min, y_min, x_max, y_max]
                    neg_index = [pixel_list.index(val) for val in pixel_list if val < 0]
                    cv2.rectangle(image_cv2,(x_min,y_min),(x_max,y_max),(chart_colors[i]), 2)
                    if neg_index == []:
                            cv2.rectangle(image_cv2,(x_min,y_min-24), (x_min+10*len(name),y_min),chart_colors[i],-1)
                            cv2.putText(image_cv2,name,(x_min,y_min-12), font, 0.5,(0,0,0),1,cv2.LINE_AA)
                    else:
                            if (y_min < 0 and x_min > 0):
                                    cv2.rectangle(image_cv2,(x_min,0), (x_min+10*len(name),24),chart_colors[i],-1)
                                    cv2.putText(image_cv2,name,(x_min,12), font, 0.5,(0,0,0),1,cv2.LINE_AA)
                            elif (x_min < 0 and y_min > 0):
                                    cv2.rectangle(image_cv2,(0,y_min-24), (10*len(name),y_min),chart_colors[i],-1)
                                    cv2.putText(image_cv2,name,(0,y_min-12), font, 0.5,(0,0,0),1,cv2.LINE_AA)
                            elif (x_min < 0 and y_min < 0):
                                    cv2.rectangle(image_cv2,(0,0), (10*len(name),24),chart_colors[i],-1)
                                    cv2.putText(image_cv2,name,(0,12), font, 0.5,(0,0,0),1,cv2.LINE_AA)
                    #cv2.imshow('image',image_cv2)
                    #cropped = image.crop((x_min, y_min+20, x_max, y_max))
                    cnt+=1
             
              count += 1
              #saving_path = folder_classified+ name +"_"+ str(count) + ".jpg"
              #imageFileName = static + ''.join(random.choice(string.ascii_uppercase) for _ in range(5)) + '.jpg'
              file1.write(name+"\n")
              cv2.imwrite(dest,image_cv2)
              cv2.destroyAllWindows()

  file1.close()

  return 