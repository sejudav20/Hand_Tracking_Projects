import cv2 as cv
import numpy as np
import mediapipe as mp
import time
from hand_detector import HandDetector
from hand_detector import ResultAnalysis
import pyautogui

class MouseController:
    mphands = mp.solutions.hands
    hands = mphands.Hands()
    mpDraw= mp.solutions.drawing_utils
    _move = False
    ACTION_LEFT_CLICK = "click"
    ACTION_RIGHT_CLICK = "r_click"
    ACTION_DRAG = "drag"
    ACTION_MOVE = "move"
    _dim_x, _dim_y=pyautogui.size()
    def is_in_box(self,pos,rect_pt_1, rect_pt_2,shape):
        id,x,y,z = pos
        pt_1_ratio= (rect_pt_1[0]/shape[1], rect_pt_1[1]/shape[0])
        pt_2_ratio= (rect_pt_2[0]/shape[1], rect_pt_2[1]/shape[0])
        
        if (pt_1_ratio[0]<x<pt_2_ratio[0]) and (pt_1_ratio[1]<y<pt_2_ratio[1]):
            width = pt_2_ratio[0]-pt_1_ratio[0]
            height = pt_2_ratio[1]-pt_1_ratio[1]
            distance_x = x-pt_1_ratio[0]
            distance_y = y-pt_1_ratio[1]
            return (True,(distance_x/width,distance_y/height))
        else:
            
            return (False,(0,0))

    def __init__(self,view,scale = 0.80,first_position = ACTION_MOVE,second_position = ACTION_LEFT_CLICK,third_position = ACTION_DRAG,fourth_position = ACTION_RIGHT_CLICK,mouse_pause=0.1,detection_conf=0.5,track_conf=0.55,track_pos=8):
        self._view = view
        pyautogui.PAUSE = mouse_pause
        hd = HandDetector(view=self._view,max_hands=1,detection_conf=detection_conf,track_conf=track_conf)
        hd.display_hand(highlight_pos=track_pos, connect_lines=False)
        

        rect_pt_1= (int(view.shape[1]*(1-scale)),int(view.shape[0]*(1-scale)))
        rect_pt_2= (int(view.shape[1]*(scale)),int(view.shape[0]*(scale)))
        cv.rectangle(self._view, rect_pt_1 ,rect_pt_2,(0,255,0),10)
        lms = hd.get_results(ratio=True)
        r_analysis = ResultAnalysis(lms)
        if(r_analysis.is_ready()):
            cv.putText(self._view, "Position:"+ str(r_analysis.get_position()), (20,20),cv.FONT_HERSHEY_TRIPLEX,1,(0,255,0))
            
            id,x,y,z = lms[track_pos]
            is_in =self.is_in_box(lms[track_pos],rect_pt_1,rect_pt_2, view.shape)
            #cv.putText(view, "Is in box:"+ str(is_in), (20,20),cv.FONT_HERSHEY_TRIPLEX,1,(0,255,0))
            if r_analysis.get_position() == 1:
                self.get_action(first_position)
                

            if r_analysis.get_position()==2:
                self.get_action(second_position)
            if r_analysis.get_position() == 3:
                self.get_action(third_position)
            if r_analysis.get_position() == 4:
                self.get_action(fourth_position)
            if self._move:
                move =is_in[0]   
            if(self._move):
                pyautogui.moveTo((1-(is_in[1][0]))*self._dim_x,(is_in[1][1])*self._dim_y,0.001)
        
        
    def get_view(self):
        return self._view
    def get_action(self, action):
        if action == self.ACTION_RIGHT_CLICK:
            self._right_click()
        elif action == self.ACTION_LEFT_CLICK:
            self._left_click()
        elif action == self.ACTION_DRAG:
            self._drag_pointer()
        elif action == self.ACTION_MOVE:
            self._move_pointer()
        else:
            self._move=False
            pass

    def _move_pointer(self):
        pyautogui.mouseUp()
        self._move=True

    def _drag_pointer(self):
        pyautogui.mouseDown()
        self._move=True
    def _left_click(self):
        pyautogui.mouseDown()
        self._move=False
    def _right_click(self):
        pyautogui.rightClick()
        self._move=False

def main():
    capture =cv.VideoCapture(0)
    
    time_prev=0
    
    dim_x, dim_y=pyautogui.size()
    
    move = False
    capture.set(cv.CAP_PROP_FRAME_HEIGHT,dim_y)
    capture.set(cv.CAP_PROP_FRAME_WIDTH,dim_x)
    while True:
        success, view= capture.read()
        
        
                        
        
        cv.putText(view,"Frame Rate: "+str(1//(time.time()-time_prev)),(20,50),cv.FONT_HERSHEY_TRIPLEX,1,(0,255,0))
        time_prev=time.time()
        mouse_controller=MouseController(view)
        view = mouse_controller.get_view()
        
        cv.imshow("Test", view)    
        
        if cv.waitKey(20) & 0xFF==ord('q'):
            break
    capture.release()

    cv.destroyAllWindows()

if __name__ == '__main__':
    main()