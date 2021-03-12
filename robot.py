import socket
import time
import cv2
import numpy as np
import sys
from accelerometer import Accelerometer
from line_us import LineUs
from utils import assert_exit

drawing = False

#this function will be called whenever the mouse is right-clicked
def mouse_callback(event, x, y, flags, params):
    global drawing
    if event==cv2.EVENT_LBUTTONDOWN:
        drawing=True
    elif event==cv2.EVENT_LBUTTONUP:
        drawing=False

    if drawing:
        my_line_us.g01(2*y, 2*x, 0)
        cv2.circle(img,(x,y),1,(0,0,255),-1)
    else:
        my_line_us.g01(2*y, 2*x, 2000)
        cv2.circle(img,(x,y),1,(250,0,255),-1)

print("Test")

my_line_us = LineUs('line-us.local')
print(my_line_us.get_hello_string())
time.sleep(1)
cap = cv2.VideoCapture(2)

img = np.zeros((int(1125/2),int(2000/2),3))
cv2.namedWindow('Test')
cv2.namedWindow('frame')
cv2.setMouseCallback('Test', mouse_callback)

while(1):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame',gray)
    cv2.imshow('Test',img)
    k=cv2.waitKey(1)&0xFF
    if k==27:
        break


time.sleep(1)
my_line_us.disconnect()
cap.release()
cv2.destroyAllWindows()