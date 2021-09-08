import cv2 as cv
import numpy as np
import mediapipe as mp


class HandDetector:
    _results = None
    _mphands = mp.solutions.hands
    _hands = _mphands.Hands()
    _mpDraw = mp.solutions.drawing_utils

    def __init__(self, view=None, max_hands=2, detection_conf=0.5, track_conf=0.5):
        self._view = view
        self.max_hands = max_hands
        self.detection_conf = detection_conf
        self.track_conf = track_conf
        self._hands = self._mphands.Hands(
            False, max_hands, detection_conf, track_conf)
        if(self._view is not None):
            imgRGB = cv.cvtColor(view, cv.COLOR_BGR2RGB)
            self._results = self._hands.process(imgRGB)

    def set_view(self, view):
        self._view = view
        if(not(view is None)):
            imgRGB = cv.cvtColor(view, cv.COLOR_BGR2RGB)
            self._results = self._hands.process(imgRGB)

    def display_hand(self, connect_lines=True, display_names=False, highlight_pos=None):
        view = self._view

        if self._results.multi_hand_landmarks:
            h, w= view.shape[0],view.shape[1]
            for hand in self._results.multi_hand_landmarks:
                for id, lm in enumerate(hand.landmark):
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    if (highlight_pos is not None) and (id == highlight_pos):
                        cv.circle(view, (cx, cy), 10, (240, 255, 0), -1)
                    if(display_names):

                        cv.putText(view, str(id), (cx-10, cy-10),
                                   cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
                self._mpDraw.draw_landmarks(
                    view, hand, self._mphands.HAND_CONNECTIONS) if connect_lines else self._mpDraw.draw_landmarks(view, hand)

    def display_full_view(self, name="Hand Detector", exit_key="q", connect_lines=True, display_names=False, video_capture=0):
        capture = cv.VideoCapture(video_capture)
        while True:
            success, view = capture.read()
            self.set_view(view)
            self._display_hand(connect_lines=connect_lines,
                               display_names=display_names)
            cv.imshow(name, view)
            if cv.waitKey(20) & 0xFF == ord('q'):
                break
        capture.release()
        cv.destroyWindow(name)

    def get_results(self, hand_num=0, hand_pos=-1, ratio=False):

        view = self._view
        landmarks = []
        if self._results.multi_hand_landmarks:
            h, w, c = view.shape
            for hand_id, hand in enumerate(self._results.multi_hand_landmarks):
                if(hand_id == hand_num):
                    if hand_pos < 0:

                        for id, lm in enumerate(hand.landmark):
                            cx, cy = int(lm.x*w), int(lm.y*h)
                            landmarks.append(
                                (id, lm.x if ratio else cx, lm.y if ratio else cy, lm.z))
                    else:
                        lm = hand.landmark[hand_pos]
                        cx, cy = int(lm.x*w), int(lm.y*h)
                        landmarks.append(
                            (hand_pos, lm.x if ratio else cx, lm.y if ratio else cy, lm.z))

        return landmarks


class ResultAnalysis:
    _finger = [False, False, False, False, False]
    _is_ready = False
    _positions =[[False,True,False,False,False],[False,True,False,False,False],[False,True,True,False,False],[False,True,True,True,False],[False,True,True,True,True],[True,True,True,True,True]]
    # position 0: closed fist 1:index finger 2: index and middle 3: index, middle, and ring 4: index,middle,ring and pinky 5: all fingers
    def __init__(self, results):
        self._results = results
        if(len(results) != 0):
            index = 4
            self._is_ready = True
            finger_list = [False,False,False,False,False]
            for i in range(len(self._finger)):
                id1, x1, y1, z1 = self._results[index]
                id2, x2, y2, z2 = self._results[index-1]

                if y2 > y1:
                    finger_list[i] = True
                else:
                    finger_list[i] = False
                
                
                index += 4
            self._finger=finger_list    
            

    def is_ready(self):
        return self._is_ready

    def count_fingers(self):
        return self._finger.count(True)

    def is_finger_up(self, num):
        if 0 < num < 6:
            return self._finger[num]
        else:
            raise ValueError("Finger number " + num + " does not exist")

    def get_fingers_up(self, num_list):
        finger_list = []
        for num in num_list:
            finger_list.append(self._finger[num])
        return finger_list

    def get_position(self):
        fingers = self._finger
        
        if fingers[1] and not (fingers[2]) and not fingers[3] and not fingers[4]:
            return 1
        elif fingers[1] and (fingers[2]) and not fingers[3] and not fingers[4]:
            return 2
        elif fingers[1] and (fingers[2]) and fingers[3] and not fingers[4]:
            return 3
        elif fingers[1] and (fingers[2]) and  fingers[3] and fingers[4]:
            return 4
        return -1