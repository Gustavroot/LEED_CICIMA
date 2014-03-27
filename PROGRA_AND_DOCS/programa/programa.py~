#!/usr/bin/python

import numpy as np
import cv2
import sys


drawing = False # true if mouse is pressed
#mode = False # if True, draw rectangle. Press 'm' to toggle to curve
ix,iy = -1,-1

#La siguiente lista contrendra un listado de listas,
#cada una de las listas internas es un conjunto de puntos,
#con cada uno de esos conjuntos de puntos se dibujaran poligonos
#en los frames posteriores al dibujado
#Esta primera lista es la mas general... contiene un listado con n
#elementos, 1 por cada video. Cada elemento es un listado de los lazos
#correspondientes al video correspondiente
listadoFilesLazos=[]
generalList=[]
specificList=[]

#El siguiente es el intervalo temporal, en ms, entre frames...
espaciadoTemporal=15

#La siguiente lista contendra las intensidades, que serviran luego para llevar
#a cabo los graficados de intensidad vs tiempo
listaIntensidades=[]

#Est contador se utilizara mas adelante, y se reseteara, para conteo de frames
counterFrames=1

#Cantidad de frames para rewind...
numberFramesRewind=20

#El siguiente contador me permite llevar la cuenta de cuantas veces me devuelvo en un video
#contadorDevolucionFRAMES=0

#img = cv2.imread('/home/gustavo/Desktop/Progra_Verano/GITrepo/ProyectoModulo5/testImgs/Blackeyegalaxy.jpg',0)
#img=None
#print "hola"
#img=np.zeros((512,512,3), np.uint8)


#En caso de presionar la letra 'q', se activa esta funcion,
#la cual detiene el programa para poder dibujar
#Si se vuelve a presionar 'q', se reanuda
def funcionDetencionYReanudacion(counterMAS, filename2, img2):
    global generalList, listaIntensidades, counterFrames
    tmpPRT=0
    while(1):
        cv2.imshow(filename2, img2)
        kp=cv2.waitKey(200) & 0xFF
        #if kp==ord('m'):
        #    mode = not mode
        if kp==ord('q'): #elif
            print "Reanudado..."
            tmpPRT=2
            break
        #El siguiente codigo se ejecuta en caso de devolucion ('r'=rewind)
        if kp==ord('r'):
            tmpPRT=1
            #Tengo que salirme del lazo alguna vez, ya que si no la recursividad no tiene sentido...
            break
        #print "r"
    if tmpPRT==1:
       #Abro nuevamente el video, ya que quiero tomar el frame al que me voy a devolver
        tmpVideoBuff = cv2.VideoCapture(sys.argv[1]+filename2)
        #Tengo que hacer un for para llegar a ese frame...
        for cntrFrmsBuff in range(0,(counterFrames-numberFramesRewind)):
            tmpRetBuff, tmpFrameBuff=tmpVideoBuff.read()
        #Una vez que tengo el frame, extraigo la imagen...
        imgBuff = cv2.cvtColor(tmpFrameBuff, cv2.COLOR_BGR2GRAY)
        #Y en ella debo dibujar los poligonos que tenga hasta el momento...
        cntROTULADO=0
        for x in generalList:
            fontSCR = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(imgBuff,str(cntROTULADO),(generalList[cntROTULADO][0][0],generalList[cntROTULADO][0][1]), fontSCR, 1,(255,255,255),2,2)
            cv2.polylines(imgBuff,[np.array(x, np.int32).reshape((-1,1,2))],True,(255,0,0))
            cntROTULADO+=1
        #Termino de configurar algunos detalles para poder desplegar el frame al que me devolvi...
        cv2.namedWindow(filename2)
        cv2.setMouseCallback(filename2,draw_lines, imgBuff)
        cv2.imshow(filename2, imgBuff)
        #Por ultimo, se eliminan los elementos de listaIntensidades que ya no son necesarios...
        for cntrPOL in range(0,len(listaIntensidades[counter-2])):
            for cntBORR in range(0,numberFramesRewind):
                listaIntensidades[counter-2][cntrPOL].pop()
        #Puesto que me estoy devolviendo numerFramesRewind cantidad de frames:
        counterFrames-=numberFramesRewind
        #contadorDevolucionFRAMES+=1
        #Y debo hacer un llamado, de manera recursiva, a esta funcion de detencion,
        #ya que hay que seguir desplegando la img, y ademas puede que quiera devolverme
        #todavia mas en el video
        filename3=filename2
        funcionDetencionYReanudacion(0, filename3, imgBuff)
    #if tmpPRT==2:
    #    procesado(sys.argv[counter], counterFrames)
    '''
    if cv2.waitKey(200) & 0xFF != ord('q'):
        cv2.imshow(filename2, img2)
        counter+=200
        funcionDetencionYReanudacion(counter, filename2, img2)
    else:
        print "Reanudado..."
    '''

#Esta funcion es la que se llama al dibujar figuras (poligonos)
def draw_lines(event, x, y, flags, param):
    #Recordar que aqui "param" representa a la imagen o frame que se esta procesando
    global generalList, specificList
    global ix,iy,drawing#,mode
    #Click inicial
    if event == cv2.EVENT_LBUTTONDOWN:
        #En este primer punto de contacto, se lleva a cabo un rotulado del poligono
        #a dibujar... se rotula con len(listadoFilesLazos[counter-2])
        fontSCR = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(param,str(len(generalList)),(x,y), fontSCR, 1,(255,255,255),2,2)

        specificList=[]
        bufferArray=[x,y]
        specificList.append(bufferArray)
        drawing = True
        ix,iy = x,y
        #print param[y,x]
    #Arrastrado del mouse
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            bufferArray=[x,y]
            specificList.append(bufferArray)
            cv2.circle(param,(x,y),5,(0,0,255),-1)
            #Intento inicial de dibujo de lineas... fallo
            #cv2.line(param,(ix,iy),(x,y),(255,0,0),5)
            #if mode == True:
            #    cv2.rectangle(param,(ix,iy),(x,y),(0,255,0),-1)
            #else:
            #    cv2.circle(param,(x,y),5,(0,0,255),-1)
    #Cuando se suelta el mouse, se detiene el dibujado, y se completa
    #asi una figura cerrada
    elif event == cv2.EVENT_LBUTTONUP:
        #Cuando se suelta el mouse, quiere decir que se creo un nuevo poligono,
        #por lo que hay que agregar un nuevo elemento a listaIntensidades, y hay
        #que recordar que counter es un contador para los videos
        listaIntensidades[counter-2].append([])
        #Ademas, se debe hacer un llenado de acuerdo al tiempo, con 0s, puesto que
        #antes del dibujado no hay registros, correspondiente al ultimo poligono dibujado
        for cnt in range(0, counterFrames):
            listaIntensidades[counter-2][len(listaIntensidades[counter-2])-1].append(0)

        bufferArray=[x,y]
        specificList.append(bufferArray)
        drawing = False
        cv2.circle(param,(x,y),1,(0,0,255),-1)
        #if mode == True:
        #    cv2.rectangle(param,(ix,iy),(x,y),(0,255,0),-1)
        #else:
        #    cv2.circle(param,(x,y),1,(0,0,255),-1)
        generalList.append(specificList)
        #Dibujado de poligono:
        pts = np.array(specificList, np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(param,[pts],True,(255,0,0))
        #print specificList
        #print generalList
        print "Cantidad de lazos dibujados hasta el momento: 1 global mas %d locales" %(len(generalList)-1)

    #Este if funcionada para el caso de que se de doble click
    #if event == cv2.EVENT_LBUTTONDBLCLK:
    #    #print param
    #    cv2.circle(param,(x,y),100,(255,0,0),-1)

#A esta funcion se le pasara cada uno de los archivos de video, para ser procesados
def procesado(filename):
    global listadoFilesLazos, generalList, counterFrames

    print "\nIniciando procesado del archivo %s..." %filename
    #Las siguientes dos lineas son una extraccion de un frame,
    #y la idea es no cambiar esto, para luego hacer una comparacion del tipo de
    #este frame, con el tipo del frame que si va cambiando, esto para la detencion
    #del while...
    #print sys.argv[1]+filename
    tmpVideo = cv2.VideoCapture(sys.argv[1]+filename)
    if not tmpVideo:
        print "Falla en extraccion de video..."
    tmpRet, tmpFrame=tmpVideo.read()
    #Extraccion del archivo video
    cap = cv2.VideoCapture(sys.argv[1]+filename)
    #print cap.get(3)
    #cap.set(CV_CAP_PROP_FRAME_WIDTH, 1280)
    #cap.set(CV_CAP_PROP_FRAME_HEIGHT, 1024)
    counterFrames=1
    devolucionFRAMES=0
    while True:
        #print counterFrames
        estadoFinal="sin interrumpir"
        #Extraccion del frame
        if devolucionFRAMES==1:
            cap = cv2.VideoCapture(sys.argv[1]+filename)
            for x in range(0,counterFrames):
                ret, frame = cap.read()
            devolucionFRAMES=0
            #contadorDevolucionFRAMES=0
        else:
            ret, frame = cap.read()
        #Setting width and height
        #... pending!
        #Lo que se mencionaba antes... en caso de no tener el tipo adecuado el frame
        #que se extrajo, quiere decir que se llego al final del video
        if type(frame)!=type(tmpFrame):
            break
        #print np.size(frame, 1)
        #print np.size(frame, 0)
        #Otra forma de verificar que se ha llegado al final del video...
        #if not frame:
        #    break
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #img = cv2.cvtColor(frame, 0)
        #Dibujado de poligonos... (si es que los hay)... hay que recordar que generalList
        #es una lista que contiene listas, y cada una de esas listas interas es un conjunto
        #de puntos asociados a un poligono anteriormente dibujado... tambien se hace un
        #rotulado de los poligonos
        cntROTULADO=0
        for x in generalList:
            fontSCR = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img,str(cntROTULADO),(generalList[cntROTULADO][0][0],generalList[cntROTULADO][0][1]), fontSCR, 1,(255,255,255),2,2)
            cv2.polylines(img,[np.array(x, np.int32).reshape((-1,1,2))],True,(255,0,0))
            cntROTULADO+=1
        #print type(img)
        #print filename
        cv2.namedWindow(filename)
        cv2.setMouseCallback(filename,draw_lines, img)
        cv2.imshow(filename, img)

        #---------------------------------------------------------------------------------------------------
        #Este parece ser un buen punto para un procesado...
        #Aqui se toma la lista listadoFilesLazos, que contiene la informacion de los poligonos, y se hace
        #un procesado de esos poligonos... lo que hay que hacer es obtener la intensidad promedio, para la
        #figura formada por cada uno de esos poligonos... esas intensidades se guardan en listaIntensidades
        #Hay que recordar que generalList representa cada uno de los elementos (listado, para cada video,
        #con la info de los poligonos) que luego seran anexados a listadoFilesLazos
        for cnt in range(0, len(generalList)):
            #Procesar al conjunto de puntos en listadoFilesLazos[counter-2][cnt], para obtener la intensidad
            #promedio del poligono que representan dichos puntos
            #Una vez obtenido el valor anterior, se inserta en la listaIntensidades (temporalmente se
            #insertara un 1)
            #Para poder pasar los puntos, necesito generar un numpy array
            #print cv2.contourArea(np.array(generalList[cnt], np.int32).reshape((-1,1,2)))
            #Se genera una imagen negra, del tamanho de la imagen original...
            mask2=np.zeros(img.shape,np.uint8)
            #se dibuja el contorno sobre esa imagen...
            cv2.drawContours(mask2,[np.array(generalList[cnt], np.int32).reshape((-1,1,2))],0,255,-1)
            mean_val = cv2.mean(img,mask = mask2)
            #print mean_val[0]
            #Se crea la variable, como representacion de lo que luego sera una intensidad...
            #intensidadBuffer=1
            #LO QUE ESTA ESCRITO A CONTINUACION ES UNA CABALLADA...!!
            #---------------------------------------------------------------
            #for cnt2 in range(0,len(listaIntensidades[counter-2])):
            #    listaIntensidades[counter-2][cnt2].append(mean_val[0])
            #---------------------------------------------------------------
            #Esto es lo correcto...
            listaIntensidades[counter-2][cnt].append(mean_val[0])
        #---------------------------------------------------------------------------------------------------

        #cv2.namedWindow(filename,img)
        #cv2.setMouseCallback(filename,draw_lines)
        keyFinger=cv2.waitKey(espaciadoTemporal) & 0xFF
        if keyFinger == ord('q'):
            #Cuando se presiona la tecla q, se detiene hasta que se vuelva a presionar dicha letra
            print "Detenido..."
            counterFramesBefore=counterFrames
            funcionDetencionYReanudacion(0, filename, img)
            counterFramesAfter=counterFrames
            #En caso de que el contador de frames haya cambiado, hay q atrasar el video...
            if counterFramesBefore!=counterFramesAfter:
                devolucionFRAMES=1
            #keyFinger = cv2.waitKey(0) & 0xFF
            #if keyFinger == ord('q'):
            #    continue
        elif keyFinger == ord('s'):
            estadoFinal="interrumpido"
            break
        counterFrames+=1

    #Se procedera ahora a generar una imagen 2D con la ubicacion de las regiones dibujadas...
    #ademas de posiciones en un plano cartesiano
    img2D = np.zeros((tmpFrame.shape[0],tmpFrame.shape[1],3), np.uint8)
    cntROTULADO=0
    miarchivoCENTROIDES = open('Centroides_'+filename+'.txt', 'w')
    for x in generalList:
        fontSCR = cv2.FONT_HERSHEY_SIMPLEX
        M = cv2.moments(np.array(x, np.int32).reshape((-1,1,2)))
        centroid_x = int(M['m10']/M['m00'])
        centroid_y = int(M['m01']/M['m00'])
        if x!=generalList[0]:
            cv2.putText(img2D,str(cntROTULADO)+"-("+str(centroid_x)+","+str(centroid_y)+")",(generalList[cntROTULADO][0][0],generalList[cntROTULADO][0][1]), fontSCR, 1,(255,255,255),2,2)
            miarchivoCENTROIDES.write(str(cntROTULADO)+"    "+str(centroid_x)+"    "+str(centroid_y)+"\n")
        cv2.polylines(img2D,[np.array(x, np.int32).reshape((-1,1,2))],True,(255,0,0))
        cntROTULADO+=1
    cv2.line(img2D,(0,tmpFrame.shape[0]/2),(tmpFrame.shape[1],tmpFrame.shape[0]/2),(255,0,0),5)
    cv2.line(img2D,(tmpFrame.shape[1]/2,0),(tmpFrame.shape[1]/2,tmpFrame.shape[0]),(255,0,0),5)
    cv2.imwrite('2D_'+str(counter-2)+'_'+filename+'.png',img2D)
    #Ademas, hay que etiquetar el sistema de coordenadas... aqui esta PENDIENTE encontrar
    #los centros de los poligonos, para rotular esto... ademas, hace falta hacer un rotulado
    #del sistema coordenado
    #FALTA!

    #Detalles finales del procesado de videos...
    tmpVideo.release()
    cap.release()


    #Buscar una forma de liberar estos dos sin que genere error...!
    #cap.release()
    #cv2.destroyAllWindows()
    listadoFilesLazos.append(generalList)
    generalList=[]
    print "Procesamiento del archivo %s se ha completado (%s)." % (unicode(filename), unicode(estadoFinal))
    cv2.destroyWindow(filename)


#Se hace un llamado a procesado, con nombres de archivos de video
#procesado("LEEDgraphite.wmv")


print "\nPROGRAMA PARA EL PROCESADO DE VIDEOS OBTENIDOS A PARTIR DE LEED"
print "(al dibujar las regiones de conteo, recuerde que la primera es la global, y las siguientes son las relacionadas con curvas de intensidad)\n"
counter=0
for elem in sys.argv:
    if counter>=2:
        #Cada entrada principal de listaIntensidades es un video
        listaIntensidades.append([]) #esto se pone antes del llamado a procesado, puesto que si no hay un out of scope
        #print sys.argv[counter]
        #print counter
        procesado(sys.argv[counter])
    counter+=1

#print len(listadoFilesLazos)
#print listaIntensidades
espaciadoTemporalMS=float(espaciadoTemporal)/1000
#Ahora se procede al guardado de los valores de intensidad en archivos
for cntAR in range(len(listaIntensidades)):
    for cntAR2 in range(len(listaIntensidades[cntAR])):
        miarchivo = open('Datos_'+sys.argv[cntAR+2]+'_'+str(cntAR2)+'.dat', 'w')
        for cntAR3 in range(len(listaIntensidades[cntAR][cntAR2])):
            miarchivo.write(str(cntAR3*espaciadoTemporalMS)+"    "+str(listaIntensidades[cntAR][cntAR2][cntAR3])+"\n")
#fin del for...        


#Hay que llevar a cabo un guardado adecuado de la informacion en listaIntensidades... todo
#eso se guardara en archivos .txt


#print sys.argv[1]
#print sys.argv[2]
#print len(sys.argv)


print "\nFin del programa"
