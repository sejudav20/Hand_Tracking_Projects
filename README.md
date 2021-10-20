# Hand_Tracking_Projects
Hand Tracking Projects Using Opencv
Created three main projects rock paper scissors, draw and mouse_controls each have its respective module.
All three use the HandDetector and ResultAnalysis in hand_detector.py to identify and track hand gestures through Google's
mediapipe library
## Rock Paper Scissors
The program starts a screen with a timer prompting rock, paper scissors and then on shoot it will take a look at the hand position shown to the camera.
The computer randomly chooses between the three options as well. The screen then displays the winner while starting the next game. By default the game can be closed
by pressing q
![image](https://user-images.githubusercontent.com/23585933/138020117-ccea0046-554c-4977-95ae-1bd36e425daa.png)

## Draw
The program starts a camera screen. If the camera detects a hand a pointer will show up. If the user puts up two fingers it is counted as a press, three fingers is a drag and four
fingers is used in some modes. There are several buttons along the button bar which can be selected by showing two fingers. Including changing color, erase previous changes,
and add photos to overlay on your screen. The program provides enough tools to help explain and teach without the need for a stylus or a separate tablet.
![image](https://user-images.githubusercontent.com/23585933/138019504-db9c40de-e676-48ae-80c1-53965fed3fd8.png)

## Mouse Controls
This module when run uses pyautogui in combination with hand detector to control the mouse on your screen. With one finger you can move the mouse. Two fingers to click,
and three fingers to drag.

![image](https://user-images.githubusercontent.com/23585933/138019912-5d9366fd-5af4-47c4-b039-45d7014bde0e.png)
