import cv2
import time
import numpy as np
import sys
from accelerometer import Accelerometer
from line_us import LineUs

# Open LineUs robot
my_line_us = LineUs('line-us.local')
time.sleep(1)
# Set speed
my_line_us.g94(30)

# Open camera
cap = cv2.VideoCapture(0)

# Open acceleromenter
accel = Accelerometer("/dev/ttyACM0")

# Create windows
img = np.zeros((int(1125/2),int(2000/2),3))
cv2.namedWindow('Drawing image')
cv2.namedWindow('Camera')

x = 0
y = 0

# Main loop
while(1):
    time.sleep(0.001)

    # Get camera frame
    ret, gray = cap.read()
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Read accelerometer values
    accel_values = accel.read_accel()
    
    # Update internal values
    x += int((accel_values[0]/10))
    y += int((accel_values[1]/10))

    x = max(min(x, 2000), 0)
    y = max(min(y, 1125), 0)

    print("accel x: %d y: %d" % (int((accel_values[0]/100)), int((accel_values[1]/100))))
    print("final x: %d y: %d" % (x,y))

    # Send it
    my_line_us.g01(y, x, 0)
    cv2.circle(img,(int(x/2),int(y/2)),1,(0,0,255),-1)

    # Show images
    cv2.imshow('Camera',gray)
    cv2.imshow('Drawing image',img)
    
    # Close
    k=cv2.waitKey(1)&0xFF
    if k==27:
        break

# Close everything
time.sleep(1)
my_line_us.disconnect()
cap.release()
cv2.destroyAllWindows()