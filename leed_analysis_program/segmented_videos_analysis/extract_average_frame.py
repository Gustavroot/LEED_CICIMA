#!/usr/bin/env python

#Libraries
import numpy
import cv2
import sys
import os
import shutil
import PIL
from PIL import Image

#First: extraction of all frames.. and saving them on buff dir
if os.path.exists('./buff_imgs/'): shutil.rmtree('./buff_imgs/')
os.mkdir('./buff_imgs/')

video_buff = cv2.VideoCapture(sys.argv[1])
counter_imgs = 0
while(video_buff.isOpened()):
    ret, frame = video_buff.read()
    cv2.imwrite('./buff_imgs/'+str(counter_imgs)+'.JPG', frame)
    check_size = os.stat('./buff_imgs/'+str(counter_imgs)+'.JPG').st_size
    if int(check_size)==0:
        os.remove('./buff_imgs/'+str(counter_imgs)+'.JPG')
        break
    counter_imgs = counter_imgs + 1
video_buff.release()

#Second: averaging all saved frames
#Access all JPG files in directory
allfiles=os.listdir('./buff_imgs/')
imlist=[filename for filename in allfiles if filename[-4:] in [".jpg",".JPG"]]
#Assuming all images are the same size, get dimensions of first image
w,h=Image.open('./buff_imgs/'+imlist[0]).size
N=len(imlist)
#Create a numpy array of floats to store the average (assume RGB images)
arr=numpy.zeros((h,w,3),numpy.float)
#Build up average pixel intensities, casting each image as an array of floats
for im in imlist:
    imarr=numpy.array(Image.open('./buff_imgs/'+im),dtype=numpy.float)
    arr=arr+imarr/N
#Round values in array and cast as 8-bit integer
arr=numpy.array(numpy.round(arr),dtype=numpy.uint8)
#Generate and save final image
out=Image.fromarray(arr,mode="RGB")
out.save(sys.argv[2])

#Removing used buff dir for imgs
shutil.rmtree('./buff_imgs/')
