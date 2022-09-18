import cv2
import time
import numpy as np
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from hand_tracking import  handDetecter


#? Necesario para poder cambiar el volumen
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volume_range = volume.GetVolumeRange()



def main():
    video_cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    p_time = 0
    c_time = 0
    detector = handDetecter(detection_con=0.8)

    while video_cap.isOpened():
        succes, img = video_cap.read()
        detector.find_hand(img)
        c_time = time.time()
        fps = 1//(c_time - p_time)
        p_time = c_time
        list_positions = detector.positions(img, draw=False)
        volumen = 0
        if (len(list_positions) != 0):
            #? Accedemos a los dedos 'Indice' y 'Pulgar'
            x1, y1 = list_positions[4][1], list_positions[4][2]
            x2, y2 = list_positions[8][1], list_positions[8][2]

            #* Conseguir coordenadas para dibujar el círculo del medio.
            cx, cy = (x1+x2) // 2, (y1+y2) // 2


            #? Graficar círculos en los dedos seleccionados
            cv2.circle(img, (x1,y1), 15, (0, 250, 0), cv2.FILLED)
            cv2.circle(img, (x2,y2), 15, (0, 250, 0), cv2.FILLED)


            #? Graficar línea que unen los dedos
            cv2.line(img, (x1,y1), (x2,y2), (0,0,150), 2)


            #? Graficar círculo en la mitad de la línea
            cv2.circle(img, (cx,cy), 15, (100, 5, 0), cv2.FILLED)

            #! Procesos para cambiar el volumen del sistema
            volumen = hypot(x2-x1, y2-y1)
            if (volumen < 70):
                cv2.circle(img, (cx,cy), 15, (250,100,100), cv2.FILLED)

            min_vol = volume_range[0]
            max_vol = volume_range[1]   

            vol = np.interp(volumen, [50,300], [min_vol, max_vol])
            volume.SetMasterVolumeLevel(vol, None)

            
        #? Mostrar los FPS
        cv2.putText(img, "FPS: " + str(fps), (7,25), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,255),2)

        #? Entero de 0 - 100
        volvPer = np.interp(volumen, [50,300], [0,100])

        #? Colocar volumen en pantalla
        cv2.putText(img, "Vol: " + str(int(volvPer)) + "%", (3,190), cv2.FONT_HERSHEY_PLAIN, 1, (0,150,0),2)
        
        #? Entero de 0 - 100 transformado para graficarlo
        volvB = np.interp(volumen, [50,300], [450, 200])

        #? Rectangulo externo
        cv2.rectangle(img, (10,200), (50,450), (0, 150, 0), 2)

        #? Rectangulo interno que cambiará dinámicamente según el volumen
        cv2.rectangle(img, (10,int(volvB)), (50,450), (0, 150, 0), cv2.FILLED)
   

        if (cv2.waitKey(10) == ord ('q')):
            break

        cv2.imshow("Controlar Volumen", img)

    video_cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()