#!/usr/bin/python

import subprocess
import os

#Program to cut video transformed, located at videos/transf/
def getLength(filename):
  result = subprocess.Popen(["ffprobe", filename],
    stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
  return [x for x in result.stdout.readlines() if "Duration" in x]

#--main--
print subprocess.Popen(['pwd'])
filename_an=os.listdir("./full_videos_analysis/videos/transf/")
duration_video = getLength("./full_videos_analysis/videos/transf/"+filename_an[0])[0].split(',')[0].lstrip().split(' ')[1].split('.')[0].split(':')

dur_video_total_secs = 60*60*int(duration_video[0])+60*int(duration_video[1])+int(duration_video[2])

counter_dur_sec=0
counter_dur_min=0
counter_dur_hour=0

step_secs = 30

dur_video_total_secs_red = dur_video_total_secs/int(step_secs)
remaining_secs = int((dur_video_total_secs/float(step_secs)-dur_video_total_secs/int(step_secs))*int(step_secs))
global_counter = 0

#Determination of how many ZFILLs - how many digits is gonna have the variable global_counter
zfills = dur_video_total_secs/int(step_secs)
zfills_digits = len(str(zfills))

input_name = './full_videos_analysis/videos/transf/'+filename_an[0]
while 60*60*counter_dur_hour+60*counter_dur_min+counter_dur_sec < dur_video_total_secs_red*step_secs:
    counter_dur_sec_tmp = counter_dur_sec
    counter_dur_min_tmp = counter_dur_min
    counter_dur_hour_tmp = counter_dur_hour
    counter_dur_sec = counter_dur_sec + int(step_secs)
    if counter_dur_sec == 60:
        counter_dur_sec = 0
        counter_dur_min = counter_dur_min + 1
    if counter_dur_min == 60:
        counter_dur_min = 0
        counter_dur_hour = counter_dur_hour + 1
    initial_time_str = str(counter_dur_hour_tmp).zfill(2)+':'+str(counter_dur_min_tmp).zfill(2)+':'+str(counter_dur_sec_tmp).zfill(2)
    final_time_str = str(0).zfill(2)+':'+str(0).zfill(2)+':'+str(step_secs).zfill(2)
    output_name = "OutputPart"+str(global_counter).zfill(zfills_digits)+".wmv"
    params_ffmpeg = ['ffmpeg','-i',input_name,'-vcodec','copy','-acodec','copy','-ss',initial_time_str,'-t',final_time_str,output_name]
    print "\n"
    print "--------NEXT CUT--------"
    print ' '.join(params_ffmpeg)
    subprocess.Popen(params_ffmpeg).wait()
    global_counter = global_counter + 1

if remaining_secs>0:
    initial_time_str = str(counter_dur_hour).zfill(2)+':'+str(counter_dur_min).zfill(2)+':'+str(counter_dur_sec).zfill(2)
    final_time_str = str(0).zfill(2)+':'+str(0).zfill(2)+':'+str(remaining_secs).zfill(2)
    output_name = "OutputPart"+str(global_counter).zfill(zfills_digits)+".wmv"
    subprocess.Popen(['ffmpeg','-i',input_name,'-vcodec','copy','-acodec','copy','-ss',initial_time_str,'-t',final_time_str,output_name]).wait()

#Moving files to videos/transf/
for x in range(0,global_counter+1):
    original_name_mv = 'OutputPart'+str(x).zfill(zfills_digits)+'.wmv'
    final_name_mv = './full_videos_analysis/videos/transf/'
    subprocess.Popen(['mv',original_name_mv,final_name_mv]).wait()
