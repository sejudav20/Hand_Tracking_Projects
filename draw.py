import cv2 as cv
import numpy as np
import mediapipe as mp
import time
from hand_detector import HandDetector
from hand_detector import ResultAnalysis
import tkinter as tk
from tkinter import filedialog


class DrawInterface:
    line_width = 6
    mode = 1
    color = (0, 0, 255)
    button_bar = []
    dragables = []
    x_prev = 0
    y_prev = 0
    clicked = None

    def __init__(self, capture):
        self.canvas = np.zeros((int(capture.get(cv.CAP_PROP_FRAME_HEIGHT)), int(
            capture.get(cv.CAP_PROP_FRAME_WIDTH)), 3), dtype='uint8')
        self.hd = HandDetector(max_hands=1, detection_conf=0.5, track_conf=0.5)
        self._init_buttons()

    def _init_buttons(self):
        self.b = Button(10, 5, 60, img='pen-red.jpg', ratio=5)

        self.b2 = Button(101, 5, 60, img='pen-green.jpg', ratio=5)
        self.b3 = Button(181, 5, 60, img='pen-blue.jpg', ratio=5)
        self.b4 = Button(261, 5, 60, img='eraser.jpg', ratio=5)
        self.b5 = Button(341, 5, 60, img='img_icon.jpg', ratio=5)
        self.b6 = Button(421, 5, 60, img='select.png', ratio=5)
        self.b7 = Button(501, 5, 60, img='zoom_in.jpg', ratio=5)
        self.b8 = Button(581, 5, 60, img='zoom_out.jpg', ratio=5)
        self.button_bar.append(self.b)
        self.button_bar.append(self.b2)
        self.button_bar.append(self.b3)
        self.button_bar.append(self.b4)
        self.button_bar.append(self.b5)
        self.button_bar.append(self.b6)
        self.button_bar.append(self.b7)
        self.button_bar.append(self.b8)

    def _draw_task_bar(self, view):
        cv.rectangle(
            view, (0, 0), (view.shape[1], view.shape[0]*2//10), (255, 255, 255), -1)
        self.b.draw(view)
        self.b2.draw(view)
        self.b3.draw(view)
        self.b4.draw(view)
        self.b5.draw(view)
        self.b6.draw(view)
        self.b7.draw(view)
        self.b8.draw(view)

    def change_color(self, c):
        self.mode = 1
        if c == 'b':
            self.color = (255, 0, 0)
        elif c == 'g':
            self.color = (0, 255, 0)
        elif c == 'r':
            self.color = (0, 0, 255)

    def set_erasable(self):

        self.mode = 2

    def overlay_img(self):
        filetypes = (
            ('png files', '*.png'),
            ('Jpeg files', '*.jpg'),
            ('gif files', '*.'))
        root = tk.Tk()
        root.withdraw()
        img_path = filedialog.askopenfilename(filetypes=filetypes)
        print("Image path===============",img_path)
        if(img_path is not None and img_path !=""):
            img = cv.imread(img_path)
            self.dragables.append(Dragable(img,200,100))

    def _check_overlay_clicked(self,x,y):
        for dragable in self.dragables:
            if dragable.isClicked(x,y):
                self.clicked=dragable
                break
    def draw_overlays(self, view):
        for dragable in self.dragables:
            dragable.draw(view)
    def _on_select(self):
        self.mode=3
    def _on_zoom_in(self):
        self.mode=4
    def _on_zoom_out(self):
        self.mode=5

    def draw(self, view):
        self.hd.set_view(view)
        self.hd.display_hand(highlight_pos=8)
        lms = self.hd.get_results()
        r_analysis = ResultAnalysis(lms)
        view = cv.flip(view, 1)
        self._draw_task_bar(view)
        self.draw_overlays(view)
        

        if r_analysis.is_ready():
            finger_position = r_analysis.get_position()
            id, x, y, z = lms[8]
            
            xf = view.shape[1]-x
            # y=view.shape[1]-y
            if y > view.shape[0]*2//10:
                if finger_position == 2 and self.mode == 1:
                    self.paint(xf, y)
                    cv.circle(view, (view.shape[1]-x, y),
                              10, (0, 255, 255), thickness=-1)
                elif finger_position > 1 and self.mode == 2:
                    self.x_prev = 0
                    self.y_prev = 0

                    id11, x11, y11, z11 = lms[11]
                    eraser_size = 50
                    cv.rectangle(view, (view.shape[1]-x11+eraser_size, y11-eraser_size), (
                        view.shape[1]-x11-eraser_size, y11+eraser_size), (226, 174, 180), thickness=-1)

                    x11f1 = view.shape[1]-(x11+eraser_size)
                    x11f2 = view.shape[1]-(x11-eraser_size)
                    self.canvas[(y11-eraser_size):(y11+eraser_size),
                                x11f1:x11f2, :] = 0
                
                
                else:
                    cv.circle(view, (view.shape[1]-x, y),
                              3, (0, 0, 255), thickness=-1)
                    self.x_prev = 0
                    self.y_prev = 0
                if self.mode==5:
                    if self.clicked is None:
                            
                        self._check_overlay_clicked((xf), y)
                    elif finger_position==2:
                        self.clicked.increase_x(view)
                        self.clicked=None
                    elif finger_position ==4:
                        self.clicked.increase_y(view)
                        self.clicked=None            
                                
                    else:
                            
                        self.clicked=None    
                if self.mode==4:
                    if self.clicked is None:
                            
                        self._check_overlay_clicked((xf), y)
                    elif finger_position==2:
                        self.clicked.decrease_x(view)
                        self.clicked=None
                    elif finger_position ==4:
                        self.clicked.decrease_y(view)
                        self.clicked=None            
                                
                    else:
                            
                        self.clicked=None
                                
                if self.mode==3:
                    
                    if self.clicked is None:
                        
                        self._check_overlay_clicked((xf), y)
                    elif finger_position==2:
                            self.clicked.translate(xf, y,view)
                    elif finger_position ==4:
                        self.dragables.remove(self.clicked)
                        self.clicked=None            
                            
                    else:
                        
                        self.clicked=None
                
            else:
                self.b.if_clicked(self.change_color,
                                  view.shape[1]-x, y, finger_position == 2, param="r", other_buttons=self.button_bar)
                self.b2.if_clicked(self.change_color,
                                   view.shape[1]-x, y, finger_position == 2, param="g", other_buttons=self.button_bar)
                self.b3.if_clicked(self.change_color,
                                   view.shape[1]-x, y, finger_position == 2, param="b", other_buttons=self.button_bar)
                self.b4.if_clicked(self.set_erasable,
                                   view.shape[1]-x, y, finger_position == 2, other_buttons=self.button_bar)
                self.b5.if_clicked(self.overlay_img,
                                   view.shape[1]-x, y, finger_position == 2, other_buttons=self.button_bar)
                self.b6.if_clicked(self._on_select,
                                   view.shape[1]-x, y, finger_position == 2, other_buttons=self.button_bar)
                self.b7.if_clicked(self._on_zoom_out,
                                   view.shape[1]-x, y, finger_position == 2, other_buttons=self.button_bar)
                self.b8.if_clicked(self._on_zoom_in,
                                   view.shape[1]-x, y, finger_position == 2, other_buttons=self.button_bar)
    
                if finger_position >= 2:

                    cv.circle(view, (view.shape[1]-x, y),
                              10, (255, 255, 0), thickness=-1)
                else:

                    cv.circle(view, (view.shape[1]-x, y),
                              10, (0, 255, 0), thickness=-1)

        flipped = view
        gray = cv.cvtColor(self.canvas, cv.COLOR_BGR2GRAY)
        d, thresh = cv.threshold(gray, 50, 255, cv.THRESH_BINARY_INV)
        imginv = cv.cvtColor(thresh, cv.COLOR_GRAY2BGR)
        img = cv.bitwise_and(flipped, imginv)
        img = cv.bitwise_or(img, self.canvas)
        return img

    def paint(self, x, y):
        if self.x_prev == 0 and self.y_prev == 0:
            cv.circle(self.canvas, (x, y),
                      self.line_width, self.color, -1)
            self.x_prev = x
            self.y_prev = y
        else:
            cv.line(self.canvas, (self.x_prev, self.y_prev),
                    (x, y), self.color, self.line_width)
            self.x_prev = x
            self.y_prev = y


class Dragable:
    
    def __init__(self, img, x, y):
        self.original=img
        self.img = img
        self.x = x
        self.y = y
        self.dim = (100, 100)
        self.prev_dim= (100,100)

    def draw(self, view):
        img=self.original
        
        try:
            view[self.y:self.y+self.dim[1],self.x:self.x+self.dim[0]
                ] = cv.resize(img, ( self.dim[0],self.dim[1]), interpolation=cv.INTER_AREA)
        except ValueError:
            self.dim=self.prev_dim
            view[self.y:self.y+self.dim[1],self.x:self.x+self.dim[0]
                ] = cv.resize(img, ( self.dim[0],self.dim[1]), interpolation=cv.INTER_AREA)

    def resize(self,w,h):
        self.dim=(w,h)
    def increase_x(self,view):
        w,h= self.dim
        if not(self.x+w>= view.shape[1] and self.y+h>= view.shape[0]):

            self.prev_dim = self.dim    
            self.dim=(int(w*1.1),h)
    def increase_y(self,view):
        w,h= self.dim
        self.prev_dim = self.dim  
        if not(self.x+w>= view.shape[1] and self.y+h>= view.shape[0]):

            
            self.dim=(w,int(h*1.1))
        
    def decrease_x(self,view):
        w,h= self.dim
        self.prev_dim = self.dim  
        if not(self.x+w>= view.shape[1] and self.y+h>= view.shape[0]):

            
            self.dim=(int(w*0.9),h)
    def decrease_y(self,view):
        w,h= self.dim
        self.prev_dim = self.dim   
        if not(self.x+w>= view.shape[1] and self.y+h>= view.shape[0]):

            
            self.dim=(w,int(h*0.9))
            
        
    def translate(self,nx,ny,view):
        if not(nx+self.dim[0]>= view.shape[1] or ny+self.dim[1]>= view.shape[0]) or ny<=view.shape[0]*2//10:
            
            self.x=nx
            self.y=ny
        

    def isClicked(self,mx,my):
        
        return self.x<=mx<=self.x+self.dim[0] and self.y<=my<=self.y+self.dim[1]
    

class Button:
    _color = (255, 0, 0)

    def __init__(self, x, y, size, img=None, ratio=5):

        self._x = x
        self._y = y
        self._size = size
        self.size = size
        self._ratio = ratio
        self._img = img
        self._activate = False
        if img is not None:
            self._img = cv.imread(img)

    def set_inactive(self):
        self._activate = False

    def draw(self, view):
        self._view = view
        cv.rectangle(
            self._view, (self._x, self._y), ((self._x)+self._size, self._y+self._size), self._color, -1)
        if self._activate:
            cv.rectangle(
                self._view, (self._x, self._y), ((self._x)+self._size, self._y+self._size), (0, 0, 0), 2)
        if self._img is not None:
            dim = view[self._y+self._ratio:((self._y)+self._size-self._ratio),
                       self._x+self._ratio:((self._x)+self._size-self._ratio)].shape

            view[self._y+self._ratio:((self._y)+self._size-self._ratio), self._x+self._ratio:(
                (self._x)+self._size-self._ratio)] = cv.resize(self._img, (dim[1], dim[0]), interpolation=cv.INTER_AREA)

    def get_view(self):
        return self._view

    def if_clicked(self, function, mx, my, isClick, param=None, other_buttons=None):
        if isClick:

            if ((self._x) < mx < (self._x+self._size)) and ((self._y) < my < (self._y+self._size)):
                if other_buttons is not None:
                    for button in other_buttons:
                        button.set_inactive()
                self._activate = True
                if param is not None:
                    function(param)
                else:
                    function()

            if self._activate:
                self._color = (0, 155, 155)

            else:
                self._color = (255, 0, 0)


def main():
    capture = cv.VideoCapture(0)
    # Mode = 1 for regular point drag drop  Mode 2 draw  Mode 3 2 hand zoom
    mode = 1
    time_prev = 0

    d_interface = DrawInterface(capture)
    while True:
        success, view = capture.read()
        img = d_interface.draw(view)

        cv.putText(img, "Frame Rate: "+str(1//(time.time()-time_prev)),
                   (20, 50), cv.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0))
        time_prev = time.time()

        cv.imshow("Draw", img)
        if cv.waitKey(20) & 0xFF == ord('q'):
            break
    capture.release()

    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
