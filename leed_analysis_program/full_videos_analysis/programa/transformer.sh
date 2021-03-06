#!/bin/bash

#----------------------------------------------------------------
userD=`whoami`
currentDir=`pwd`
cd /home/$userD/
git clone https://github.com/Gustavroot/LEEDcicima.git
cd $currentDir
#-------------------------------------------------------------------------
resolucion_buff=`xdpyinfo | grep dimensions`
resolucion_buff2=($resolucion_buff)
resolucion=${resolucion_buff2[1]}

ffmpegPATH=/usr/local/bin/ffmpeg

directVideos=./full_videos_analysis/videos/
transformedPath=./full_videos_analysis/videos/transf/
if [ -d "$transformedPath" ]; then
    rm -R $transformedPath
fi
mkdir $transformedPath

stringList=`ls $directVideos`
arrayList=(${stringList//\ / })

counter=0
for i in $(ls $directVideos)
do
    fileToProcess=${arrayList[$counter]}
    if [[ -d $directVideos$fileToProcess ]]; then
        continue
    else
        echo ""
        echo "Procesando archivo "${arrayList[$counter]}"..."
        $ffmpegPATH -i $directVideos$fileToProcess -s $resolucion -b:v 512k -vcodec mpeg1video -acodec copy "TRANSFORMED"$fileToProcess
        mv ./TRANSFORMED$fileToProcess $transformedPath
    fi
    counter=`expr $counter + 1`
done

echo ""
echo "Transformaciones finalizadas..."
