#!/usr/bin/python

import numpy as np
import cv2
import sys
import os.path
import subprocess

listadoGeneralCONTORNOS=[]
#Contours extraction - if any previous
if os.path.isfile("contornos.txt"):
    miarchivoContornos=open("contornos.txt", 'r')
    for linea in miarchivoContornos:
        for lineaContorno in linea.split(':'):
            listadoGeneralCONTORNOS.append([])
            for puntoContorno in lineaContorno.split(';'):
                listadoGeneralCONTORNOS[len(listadoGeneralCONTORNOS)-1].append([int(puntoContorno.split(',')[0]),int(puntoContorno.split(',')[1])])
    miarchivoContornos.close()

drawing = False #true if mouse is pressed
ix,iy = -1,-1

#Lists for polygons
#There is a one to one correspondence between the list listadoFilesLazos and the videos
listadoFilesLazos=[]
generalList=[]
specificList=[]

#Preparing contours for use
generalList=listadoGeneralCONTORNOS

#Time interval between frames
espaciadoTemporal=15

#List for intensities storage
listaIntensidades=[]

#General frames counter
counterFrames=1

#In case of rewind
numberFramesRewind=700
ciclosSaltados=0

FPSextract=10

#This function allows stop and resume, with the q button
def funcionDetencionYReanudacion(counterMAS, filename2, img2, ciclosSaltadosX):
    global generalList, listaIntensidades, counterFrames
    tmpPRT=0
    while(1):
        cv2.imshow(filename2, img2)
        kp=cv2.waitKey(200) & 0xFF
        if kp==ord('q'): #elif
            print "Reanudado..."
            tmpPRT=2
            break
        #'r'=rewind
        if kp==ord('r'):
            tmpPRT=1
            #Necessary break. If not, recursivity makes no sense here
            break
    if tmpPRT==1:
        #Open frame again, to resume
        tmpVideoBuff = cv2.VideoCapture(sys.argv[1]+filename2)
        #Necessary for to get to that frame
        for cntrFrmsBuff in range(0,(counterFrames-numberFramesRewind*ciclosSaltadosX)):
            tmpRetBuff, tmpFrameBuff=tmpVideoBuff.read()
        #Image extraction from that frame
        imgBuff = cv2.cvtColor(tmpFrameBuff, cv2.COLOR_BGR2GRAY)
        #Polygons drawing in that frame/image
        cntROTULADO=0
        for x in generalList:
            fontSCR = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(imgBuff,str(cntROTULADO),(generalList[cntROTULADO][0][0],generalList[cntROTULADO][0][1]), fontSCR, 1,(255,255,255),2,2)
            cv2.polylines(imgBuff,[np.array(x, np.int32).reshape((-1,1,2))],True,(255,0,0))
            cntROTULADO+=1
        #Image config for display
        cv2.namedWindow(filename2)
        cv2.setMouseCallback(filename2,draw_lines, imgBuff)
        cv2.imshow(filename2, imgBuff)
        #Deleting of unnecessary intensities info
        for cntrPOL in range(0,len(listaIntensidades[counter-2])):
            for cntBORR in range(0,numberFramesRewind):
                listaIntensidades[counter-2][cntrPOL].pop()
        #Rewind
        counterFrames-=numberFramesRewind*ciclosSaltadosX
        #Recursively resuming video display, in case of needing to stop again
        filename3=filename2
        funcionDetencionYReanudacion(0, filename3, imgBuff, ciclosSaltadosX)

#Function to draw (event oriented with OpenCV)
def draw_lines(event, x, y, flags, param):
    #"param" represents the frame in process
    global generalList, specificList
    global ix,iy,drawing
    global ciclosSaltados
    #Initial click/tap
    if event == cv2.EVENT_LBUTTONDOWN:
        #In first touch, polygon is labeled on image
        fontSCR = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(param,str(len(generalList)),(x,y), fontSCR, 1,(255,255,255),2,2)
        specificList=[]
        bufferArray=[x,y]
        specificList.append(bufferArray)
        drawing = True
        ix,iy = x,y
    #Dragging touching point
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            bufferArray=[x,y]
            specificList.append(bufferArray)
            cv2.circle(param,(x,y),2,(0,0,255),-1)
    #On mouse release, polygon is drawn
    elif event == cv2.EVENT_LBUTTONUP:
        #On mouse release, info is added to listaIntensidades
        listaIntensidades[counter-2].append([])
        #Before drawing, no info is attached to polygon, so 0s are associated to it
        for cnt in range(0, int(float(counterFrames)/float(ciclosSaltados))):
            listaIntensidades[counter-2][len(listaIntensidades[counter-2])-1].append(0)

        bufferArray=[x,y]
        specificList.append(bufferArray)
        drawing = False
        cv2.circle(param,(x,y),1,(0,0,255),-1)
        generalList.append(specificList)
        #Drawing polygon
        pts = np.array(specificList, np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(param,[pts],True,(255,0,0))
        print "Cantidad de lazos dibujados hasta el momento: 1 global mas %d locales" %(len(generalList)-1)

#When a video is to be analyzed, is passed to the following function
def procesado(filename):
    global listadoFilesLazos, generalList, counterFrames, ciclosSaltados

    #There is a one to one correspondence between listaIntensidades and contours
    for cnt in range(0, len(generalList)):
        listaIntensidades[counter-2].append([])

    print "\nIniciando procesado del archivo %s..." %filename
    #1 frame extraction for later comparison with frames and check failures
    tmpVideo = cv2.VideoCapture(sys.argv[1]+filename)
    str_command = "mediainfo "+sys.argv[1]+filename
    process = subprocess.Popen(str_command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0].split('\n')
    fps_video = 'a'
    for line_from_str in output:
        if line_from_str.startswith('Frame rate'):
            fps_video = line_from_str
            break
    fps_video = fps_video.split()[3]
    fps_video = float(fps_video)
    if not tmpVideo:
        print "Falla en extraccion de video..."
    print "FPS del video "+filename+": "+str(fps_video)
    tmpRet, tmpFrame=tmpVideo.read()
    #Extraction of video file
    cap = cv2.VideoCapture(sys.argv[1]+filename)
    counterFrames=1
    devolucionFRAMES=0
    fontSCR = cv2.FONT_HERSHEY_SIMPLEX
    #Frames per second to extract
    ciclosSaltados=int(fps_video/FPSextract)
    while True:
        estadoFinal="sin interrumpir"
        #Frame extraction
        if devolucionFRAMES==1:
            #Memory release before extracting video again
            cap.release()
            cap = cv2.VideoCapture(sys.argv[1]+filename)
            for x in range(0,counterFrames):
                ret, frame = cap.read()
            devolucionFRAMES=0
        else:
            ret, frame = cap.read()
        #In case of reaching video finale
        if type(frame)!=type(tmpFrame):
            break
        #To control when a frame is extracted
        if counterFrames%ciclosSaltados==0:
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            #Memory release
            del frame
            #Drawing polygons
            cntROTULADO=0
            for x in generalList:
                cv2.putText(img,str(cntROTULADO),(generalList[cntROTULADO][0][0],generalList[cntROTULADO][0][1]), fontSCR, 1,(255,255,255),2,2)
                cv2.polylines(img,[np.array(x, np.int32).reshape((-1,1,2))],True,(255,0,0))
                cntROTULADO+=1
            cv2.putText(img,str("{0:.2f}".format(counterFrames/fps_video)),(0,60), fontSCR, 1,(255,255,255),2,2)
            #Window creation
            cv2.namedWindow(filename)
            cv2.setMouseCallback(filename,draw_lines, img)
            cv2.imshow(filename, img)

            #----------DEBUG
            #Processing
            for cnt in range(0, len(generalList)):
                mask2=np.zeros(img.shape,np.uint8)
                cv2.drawContours(mask2,[np.array(generalList[cnt], np.int32).reshape((-1,1,2))],0,255,-1)
                mean_val = cv2.mean(img,mask = mask2)
                del mask2
                listaIntensidades[counter-2][cnt].append(mean_val[0])
            #----------DEBUG

            keyFinger=cv2.waitKey(espaciadoTemporal) & 0xFF
            if keyFinger == ord('q'):
                #Stop when q is pressed
                print "Detenido..."
                counterFramesBefore=counterFrames
                funcionDetencionYReanudacion(0, filename, img, ciclosSaltados)
                counterFramesAfter=counterFrames
                #If frames counter has decreased, rewind
                if counterFramesBefore!=counterFramesAfter:
                    devolucionFRAMES=1
            elif keyFinger == ord('s'):
                estadoFinal="interrumpido"
                break
        else: #If frame not extracted, some data is deleted
            del ret
            del frame
        counterFrames+=1

    #2D image creation, with posicion of points with respect to target center
    img2D = np.zeros((tmpFrame.shape[0],tmpFrame.shape[1],3), np.uint8)
    cntROTULADO=0
    miarchivoCENTROIDES = open('Centroides_'+filename+'.txt', 'w')
    for x in generalList:
        fontSCR = cv2.FONT_HERSHEY_SIMPLEX
        M = cv2.moments(np.array(x, np.int32).reshape((-1,1,2)))
        centroid_x = int(M['m10']/M['m00'])
        centroid_y = int(M['m01']/M['m00'])
        #Labeling
        cv2.putText(img2D,str(cntROTULADO),(generalList[cntROTULADO][0][0],generalList[cntROTULADO][0][1]), fontSCR, 1,(255,255,255),2,2)
        miarchivoCENTROIDES.write(str(cntROTULADO)+"    "+str(centroid_x)+"    "+str(centroid_y)+"\n")
        #Drawing
        cv2.polylines(img2D,[np.array(x, np.int32).reshape((-1,1,2))],True,(255,0,0))
        cntROTULADO+=1
    cv2.line(img2D,(0,tmpFrame.shape[0]/2),(tmpFrame.shape[1],tmpFrame.shape[0]/2),(255,0,0),5)
    cv2.line(img2D,(tmpFrame.shape[1]/2,0),(tmpFrame.shape[1]/2,tmpFrame.shape[0]),(255,0,0),5)
    cv2.imwrite('2D_'+str(counter-2)+'_'+filename+'.png',img2D)

    #OpenCV eleases
    tmpVideo.release()
    cap.release()

    listadoFilesLazos.append(generalList)
    generalList=[]
    print "Procesamiento del archivo %s se ha completado (%s)." % (unicode(filename), unicode(estadoFinal))
    cv2.destroyWindow(filename)
    #Contours storage
    MiArchivoContornos=open("contornos.txt",'w')
    stringContornosOutput=""
    for x in range(0,len(listadoFilesLazos[0])):
        for y in listadoFilesLazos[0][x]:
            stringContornosOutput+=str(y[0])+","
            stringContornosOutput+=str(y[1])+";"
        stringContornosOutput=stringContornosOutput[:-1]
        stringContornosOutput+=":"
    stringContornosOutput=stringContornosOutput[:-1]
    MiArchivoContornos.write(stringContornosOutput)
    MiArchivoContornos.close()

print "\nPROGRAMA PARA EL PROCESADO DE VIDEOS OBTENIDOS A PARTIR DE LEED"
print "(al dibujar las regiones de conteo, recuerde que la primera es la global, y las siguientes son las relacionadas con curvas de intensidad)\n"
counter=0
for elem in sys.argv:
    if counter>=2:
        #One to one correspondence from videos to listaIntensidades
        listaIntensidades.append([])
        procesado(sys.argv[counter])
    counter+=1

print "\nFin del programa"
