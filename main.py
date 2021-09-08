import cv2 as cv
import numpy as np
import mediapipe as mp
import time
from hand_detector import HandDetector
from hand_detector import ResultAnalysis
import pyautogui
import threading

        
def main():
    capture =cv.VideoCapture(0)
    
    time_prev=0
    
    dim_x, dim_y=pyautogui.size()
    
    move = False

    while True:
        success, view= capture.read()
        
        
                        
            
        cv.putText(view,"Frame Rate: "+str(1//(time.time()-time_prev)),(20,50),cv.FONT_HERSHEY_TRIPLEX,1,(0,255,0))
        time_prev=time.time()
        # imgRGB = cv.cvtColor(view, cv.COLOR_BGR2RGB)
        # results = hands.process(imgRGB)
        # cv.putText(view,str(1//(time.time()-time_prev)),(20,20),cv.FONT_HERSHEY_TRIPLEX,1,(0,255,0))
        # 
        # if results.multi_hand_landmarks:
        #     h,w,c=view.shape
        #     for hand in results.multi_hand_landmarks:
        #         for id,lm in enumerate(hand.landmark):
        #             cx,cy = int(lm.x*w), int(lm.y*h)
        #             cv.rectangle(view,(cx-10,cy-10),(cx+10,cy+10),(0,255,0),-1)
        #         mpDraw.draw_landmarks(view, hand,mphands.HAND_CONNECTIONS)

        
        cv.imshow("Test", view)    
        
        if cv.waitKey(20) & 0xFF==ord('q'):
            break
    capture.release()

    cv.destroyAllWindows()





if __name__=='__main__':
    main()
