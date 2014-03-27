#!/bin/bash

#----------------------------------------------------------------
#Algunas configuraciones
userD=`whoami`
currentDir=`pwd`
cd /home/$userD/
git clone https://github.com/Gustavroot/LEEDcicima.git
#cd LEEDcicima
#git pull origin master
cd $currentDir
#-------------------------------------------------------------------------

#Resolucion recomendada: 1280x710, para Acer Aspire 14 pulgadas
#640x480
resolucion=1280x710

#Specify ffmpeg PATH
ffmpegPATH=/home/$userD/Downloads/src0/ffmpeg-0.11.1/ffmpeg

directVideos=../videos/
transformedPath=../videos/transf/
rm -R $transformedPath
mkdir $transformedPath

#echo "cosa"
stringList=`ls $directVideos`
arrayList=(${stringList//\ / })

#echo ${#arrayList[@]}

counter=0
for i in $(ls $directVideos)
do
    fileToProcess=${arrayList[$counter]}
    #echo $fileToProcess
    if [[ -d $directVideos$fileToProcess ]]; then
        continue
        #echo "Procesando archivo "${arrayList[$counter]}"..."
    else
        echo ""
        echo "Procesando archivo "${arrayList[$counter]}"..."
        $ffmpegPATH -i $directVideos$fileToProcess -s $resolucion -b:v 512k -vcodec mpeg1video -acodec copy "TRANSFORMED"$fileToProcess
        mv ./TRANSFORMED$fileToProcess $transformedPath
        #transformedPath
    fi
    counter=`expr $counter + 1`
done

echo ""
echo "Transformaciones finalizadas..."

#echo ${arrayList[0]}

#----------------------------------------------------------------
#Algunas configuraciones
sudo aptitude install gnuplot
#-------------------------------------------------------------------------
