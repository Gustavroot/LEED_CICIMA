#!/usr/bin/env python

import sys
import os
import shutil

#Usage: ./replicate.py original_dir/ final_dir/

if os.path.exists('./segmented_videos_analysis/frames_replicate/'): shutil.rmtree('./segmented_videos_analysis/frames_replicate/')
os.mkdir('./segmented_videos_analysis/frames_replicate/')

#Initial directory: print sys.argv[1]
#Final directory: print sys.argv[2]
#--------------MAIN PROGRAM
files_list = os.listdir("./segmented_videos_analysis/frames/")
files_list_names = []
files_names_termination = files_list[0].split('.')[-1]
for x in files_list:
    files_list_names.append('.'.join(x.split('.')[0:len(x.split('.'))-1]))
files_list_names = sorted(files_list_names, key=float)

frames_per_img = 1
total_final_imgs = len(files_list_names)*frames_per_img
zfill_size = len(str(total_final_imgs))

general_counter = 1
image_name_buff = "buff"
for image in files_list_names:
    for x in range(0,frames_per_img):
        shutil.copyfile("./segmented_videos_analysis/frames/"+image+"."+files_names_termination, "./segmented_videos_analysis/frames_replicate/"+'img_'+str(general_counter).zfill(5)+'.JPG')
        general_counter += 1
    if general_counter>len(files_list_names):
        image_name_buff = image
#Copying last file twice, as ffmpeg is avoiding its addition into the video
shutil.copyfile("./segmented_videos_analysis/frames/"+image_name_buff+"."+files_names_termination, "./segmented_videos_analysis/frames_replicate/"+'img_'+str(general_counter).zfill(5)+'.JPG')
