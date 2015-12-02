#!/usr/bin/python

import sys
import os
import subprocess
import shutil

if os.path.exists('./segmented_videos_analysis/frames/'): shutil.rmtree('./segmented_videos_analysis/frames/')
os.mkdir('./segmented_videos_analysis/frames/')

files_list = os.listdir(sys.argv[1])
files_list_names = []
files_names_termination = files_list[0].split('.')[-1]
for x in files_list:
    files_list_names.append('.'.join(x.split('.')[0:len(x.split('.'))-1]))
files_list_names = sorted(files_list_names, key=float)

for y in files_list_names:
    input_file = sys.argv[1]+y+'.'+files_names_termination
    print 'Extracting '+sys.argv[2]+' frame from video: '+input_file
    output_file = './'+y+'.'+'JPG'
    subprocess.Popen(['./segmented_videos_analysis/extract_'+sys.argv[2]+'_frame.py',input_file,output_file]).wait()

for z in files_list_names:
    input_file = './'+z+'.'+'JPG'
    output_file = './segmented_videos_analysis/frames/'+z+'.'+'JPG'
    subprocess.Popen(['mv',input_file,output_file]).wait()
