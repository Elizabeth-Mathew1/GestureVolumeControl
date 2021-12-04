import cv2.cv2 as cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
import osascript
####################################################################
wCam=1180
hCam=720
####################################################################
volume1=0
volumeb=400
volumep=0
cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime=0
detector=htm.handDetector(detectionCon=0.7)

result = osascript.osascript('get volume settings')
print(result)
print(type(result))
volInfo = result[1].split(',')
outputVol = volInfo[0].replace('output volume:', '')
print(outputVol)

target_volume = 100

#volume.SetMasterVolumeLevel(-20.0, None)


while True:
    success,img=cap.read()
    img=detector.findHands(img)
    lmList=detector.findPosition(img,draw=False)
    if len(lmList)!=0:
        #print(lmList[4],lmList[8])
        x1,y1=lmList[4][1],lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2
        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length=math.hypot(x2-x1,y2-y1)
        #print(length)

        volume1=np.interp(length,[50,300],[0,100])
        volumeb = np.interp(length, [50,300], [400, 150])
        volumep = np.interp(length, [50, 300], [0, 100])
        print(volume1)
        vol = "set volume output volume " + str(volume1)
        osascript.osascript(vol)
        if(length<50):
            cv2.circle(img, (cx, cy), 15, (0, 0, 255), cv2.FILLED)
    cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
    cv2.rectangle(img, (50, int(volumeb)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volumep)}%', (50, 500), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 4)
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime


    cv2.putText(img,f'FPS:{int(fps)}',(60,90),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),4)
    cv2.imshow("Img",img)
    cv2.waitKey(1)


