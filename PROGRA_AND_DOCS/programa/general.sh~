#!/bin/bash

transformedPath=../videos/transf/
userD=`whoami`

#Fecha actual, con identificador unico...
numSECS=`date +%s`
now=$(date +"%m_%d_%Y")"_"$numSECS

rm -R RESULTS*
mkdir "RESULTS_$now"
mkdir "RESULTS_$now/TwoDim"
mkdir "RESULTS_$now/Intensidades"
./programa.py $transformedPath `ls $transformedPath`

mv 2D_* "RESULTS_$now/TwoDim"
mv Datos_* "RESULTS_$now/Intensidades"
mv Centroides_* "RESULTS_$now/TwoDim"

#Ahora se procede a generar las graficas con gnuplot...
stringList=`ls "RESULTS_$now/Intensidades"`
arrayList=(${stringList//\ / })
for i in $(ls "RESULTS_$now/Intensidades")
do
    fileToProcess=${arrayList[$counter]}
    #echo $fileToProcess
    gnuplot << EOF
    #Ahora se puede hacer gnuplot scripting aqui...
    set isosamples 40
    unset key
    set title "Intensidad vs tiempo"
    set ztics 1
    plot "RESULTS_$now/Intensidades/$fileToProcess" with lines
    set term pngcairo mono enhanced
    set out 'Grafica_$fileToProcess.png'
    replot

    #set xlabel "Tiempo"
    #set ylabel "Intensidad"
    #plot "RESULTS_$now/Intensidades/$fileToProcess" using 1:2 with lines
    ##Una vez generado el .ps...
    #set term postscript
    #set output "PS_$fileToProcess.ps"
    #replot
    ##set term x11
    ##Se genera el png...
    #set term png
    #set output "Grafica_$fileToProcess.png"
    #replot
    ##set term x11
EOF
    counter=`expr $counter + 1`
done

#rm PS_*
mv Grafica_* "RESULTS_$now/Intensidades"


read -p "¿Desea almacenar la informacion recien procesada (en un repositorio de Github)? (s o n) " answr
echo ""
if [ "$answr" == "s" ]
then
    currentDir=`pwd`
    cd /home/$userD/LEEDcicima/
    git pull origin master
    cp -R $currentDir"/RESULTS_$now" .
    git add -A
    git commit -m "Analisis computacional de LEED: "$now
    echo ""
    echo "Si se le pide un usuario y la correspondiente contraseña a continuacion, es la informacion de su usuario de Github:"
    echo ""
    git push origin master
    echo ""
    echo "En caso de haber fallado el ingreso de contraseña de su usuario de Github, ejecutar el script gitpush.sh, ubicado en el mismo directorio en el que se encuentra este script."
    echo ""
    echo "Identificador unico para este analisis realizado (con este identificador se encuentra cual directorio, en el repositorio de Github, contiene los resultados obtenidos): "$numSECS
    echo ""
fi


#mv 2D_* ../RESULTS/
