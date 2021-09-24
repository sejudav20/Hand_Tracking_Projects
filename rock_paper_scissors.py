import cv2 as cv
import numpy as np
import mediapipe as mp
import time
from hand_detector import HandDetector
from hand_detector import ResultAnalysis
import random
class _Node:
    
    def __init__(self,name):
        self.name = name
        self.next = None
    

class _order:
    root = _Node("Rock")
    root.next=_Node("Scissors")
    root.next.next=_Node("Paper")
    root.next.next=root
    def __init__(self):
        pass
    def check(self,computer_decision,player_decision):
        if computer_decision==player_decision:
            return "Draw"
        node=self.root
        while(node.name != computer_decision):
            node = node.next
        node_next=node.next
        if  node_next.name == player_decision:
            return "Computer Won"
        else:
            return "You Won"


def main():
    capture =cv.VideoCapture(0)
    
    time_prev=0
    time_start=time.time()
    
    frame_count = 0
    examined={"Rock":0,"Paper":0,"Scissors":0}
    on_examine=False
    player_decision=""
    computer_decision=""
    outcome=""
    while True:
        success, view= capture.read()
        frame_count+=1
        overlay = np.zeros(view.shape[:3],dtype='uint8')
        hd = HandDetector(view = view,max_hands=1)
        lms = hd.get_results(ratio=True)
        r_analysis = ResultAnalysis(lms)
        time_curr=int(time.time()-time_start)
        if time_curr>4:
            on_examine=True
            
        rps=""
        if on_examine:
            rps = "Examining"
            
            if r_analysis.is_ready():
                finger_num=r_analysis.get_position()
                
                
                if finger_num>2:
                    examined["Paper"]+=1
                elif finger_num==2 or finger_num==1:
                    examined["Scissors"]+=1
                else:
                    examined["Rock"]+=1    
            frame_count+=1
            if frame_count>7:
                rps="Rock"
                for key,value in examined.items():
                     if examined[rps]<value:
                         rps=key
                on_examine=False
                computer_decision=random.choice(list(examined.keys()))
                
                player_decision=rps
                frame_count=0
                examined={"Rock":0,"Paper":0,"Scissors":0}
                time_start=time.time()
                
                outcome=_order().check(computer_decision,player_decision)
        cv.putText(view,rps,(view.shape[1]//2-view.shape[1]//4,view.shape[0]//2),cv.FONT_HERSHEY_TRIPLEX,5,(0,255,0))    
        cv.putText(view,"Frame Rate: "+str(1//(time.time()-time_prev)),(view.shape[1]-50,view.shape[0]-50),cv.FONT_HERSHEY_TRIPLEX,0.5,(0,255,0))
        msg="Start"
        if int(time_curr)==1:
            msg="Rock"
        elif int(time_curr)==2:
            msg="Paper"
        elif int(time_curr)==3:
            msg="Scissors"
        elif int(time_curr)>=4:
            msg="Shoot!"
        cv.putText(view,"Time: "+str(msg),(20,50),cv.FONT_HERSHEY_TRIPLEX,0.8,(0,255,0))
        cv.putText(view,"Your Decision: "+ player_decision,(20,80),cv.FONT_HERSHEY_TRIPLEX,0.8,(0,255,0))

        cv.putText(view,"Computer Decision: "+ computer_decision,(20,110),cv.FONT_HERSHEY_TRIPLEX,0.8,(0,255,0))
        cv.putText(view,"Outcome: "+outcome,(20,140),cv.FONT_HERSHEY_TRIPLEX,0.8,(0,255,0))
        cv.putText(view,"Follow prompt under time when game is running",(20,view.shape[0]-50),cv.FONT_HERSHEY_TRIPLEX,0.5,(0,255,0))
        cv.putText(view,"press n to restart or press q to quit",(20,view.shape[0]-20),cv.FONT_HERSHEY_TRIPLEX,0.5,(0,255,0))
        time_prev=time.time()
        masked = cv.add(view,overlay)
        
        cv.imshow("Test", masked)    
        if cv.waitKey(20) & 0xFF==ord('n'):
            time_start=time.time()
            outcome = ""
            player_decision = ""
            computer_decision = ""
        if cv.waitKey(20) & 0xFF==ord('q'):
            break
    capture.release()

    cv.destroyAllWindows()


if __name__ == "__main__":
    main()