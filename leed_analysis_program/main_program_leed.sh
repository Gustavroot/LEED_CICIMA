#!/bin/sh

echo "LEED analysis program:\n"

rm -R ./full_videos_analysis/videos/transf/
rm ./full_videos_analysis/videos/*

echo "--choose program mode--"
echo "'full' or 'segmented':"
#FULL is for complete videos
#SEGMENTED is for multiple videos with redundant info (1 frame per video is useful)
read analysis_mode


#Failure buffer variable
failure_buffer='success'

if [ "$analysis_mode" = "full" ]; then
    echo "----"
    #zenity allows to choose file from file browser box
    selected_file=$(zenity --file-selection)
    cp $selected_file ./full_videos_analysis/videos/ || { failure_buffer='fail' ; }
    if [ "$failure_buffer" = "success" ];then
        ./full_videos_analysis/programa/transformer.sh || { failure_buffer='fail' ; }
    fi
    if [ "$failure_buffer" = "success" ];then
        #Cut video in parts of 30 seconds
        ./full_videos_analysis/programa/VideosCutter.py || { failure_buffer='fail' ; }
    fi
    if [ "$failure_buffer" = "success" ];then
        cd ./full_videos_analysis/programa/
        ./general.sh || { failure_buffer='fail' ; }
        mv ./RESULTS* ../../
    fi
fi
if [ "$analysis_mode" = "segmented" ]; then
    echo "----"
    echo "'average' or 'middle'"
    read smoothness
    selected_dir=$(zenity --file-selection --directory)
    if [ "$failure_buffer" = "success" ];then
        ./segmented_videos_analysis/extract_middle_frames.py $selected_dir"/" $smoothness || { failure_buffer='fail' ; }
    fi
    if [ "$failure_buffer" = "success" ];then
        ./segmented_videos_analysis/replicate.py || { failure_buffer='fail' ; }
    fi
    if [ "$failure_buffer" = "success" ];then
        cd ./segmented_videos_analysis/
        ./merge_middles.sh || { failure_buffer='fail' ; }
    fi
    if [ "$failure_buffer" = "success" ];then
        mv "output.wmv" ../full_videos_analysis/videos/ || { failure_buffer='fail' ; }
        cd ../ || { failure_buffer='fail' ; }
    fi
    if [ "$failure_buffer" = "success" ];then
        ./full_videos_analysis/programa/transformer.sh || { failure_buffer='fail' ; }
    fi
    if [ "$failure_buffer" = "success" ];then
       #Cut video in parts of 30 seconds
        ./full_videos_analysis/programa/VideosCutter.py || { failure_buffer='fail' ; }
    fi
    if [ "$failure_buffer" = "success" ];then
        cd ./full_videos_analysis/programa/
        ./general.sh || { failure_buffer='fail' ; }
        mv ./RESULTS* ../../
        cd ../../
    fi
fi
#-----
$SHELL
