# Create annotation for FDDB darknet

import os
import cv2
from shutil import copyfile
import math


dataset_path = "dataset/fddb/"

os.makedirs(dataset_path+"FDDB-folds/annotations_darknet")

file_no = 0

train = open(dataset_path+"FDDB-folds/annotations_darknet/train.txt","w")
test = open(dataset_path+"FDDB-folds/annotations_darknet/test.txt","w")

for list1 in range(1,11):
   list2 = str(list1).zfill(2)
   try:
      IN = open(dataset_path+"FDDB-folds/FDDB-fold-"+list2+"-ellipseList.txt")
   except:
      print("wider face dataset not found")
      train.close()
      test.close()
      quit()
   line=IN.readline()
   while line:
      file_no = file_no + 1
      file_path = line.strip()

      temp = cv2.imread(dataset_path+"originalPics/"+file_path+".jpg", cv2.IMREAD_UNCHANGED).shape
      imageh, imagew = temp[0],temp[1]

      if file_no%4 == 0:
         test.write("../"+dataset_path+"FDDB-folds/annotations_darknet/"+str(file_no)+".jpg\n")
      else:
         train.write("../"+dataset_path+"FDDB-folds/annotations_darknet/"+str(file_no)+".jpg\n")

      copyfile("./"+dataset_path+"originalPics/"+file_path+".jpg", "./"+dataset_path+"FDDB-folds/annotations_darknet/"+str(file_no)+".jpg")
      OUT=open(dataset_path+"FDDB-folds/annotations_darknet/"+str(file_no)+".txt","+w")

      line=IN.readline()
      line_n=int(line)

      for i in range(line_n):
         major_axis_radius=0
         minor_axis_radius=0
         angle=0
         center_x=0
         center_y=0
         line=IN.readline()
         major_axis_radius,minor_axis_radius,angle,center_x,center_y,temp = map(float,line.split())

         x=center_x
         y=center_y

         w=abs(math.cos(angle)*major_axis_radius)*2
         h=abs(math.cos(angle)*minor_axis_radius)*2

         # w=minor_axis_radius*2
         # h=major_axis_radius*2

         category=0

         x=1.0*x/imagew
         y=1.0*y/imageh
         w=1.0*w/imagew
         h=1.0*h/imageh

         if w>0 and h>0 and x-w/2>=0 and y-h/2>=0 and x+w/2<=1 and y+h/2<=1:
            OUT.write(str(category) +" "+ str(x) +" "+ str(y) +" "+ str(w) +" "+ str(h))
         else:
            print ("Invalid string" + str(x),str(y),str(w),str(h),str(file_no))

      line=IN.readline()
      OUT.close()
   IN.close()

train.close()
test.close()
