import os
import cv2
import time
import numpy as np
from datetime import datetime

# TODO: user input for show/noshow or video name

# install v4l2 driver for pi-cam, cv2 requirement
os.system('sudo modprobe bcm2835-v4l2') 

# camera and video setup
FPS = 10  # GPU memory is set to 200 
INTERVAL = 1 / FPS
W, H = 640, 480

# open camera
cam = cv2.VideoCapture(0)  
cam.set(3, W)
cam.set(4, H)
cam.read()  # warm-up

# create video file, named with current time
folder_name = 'recordings'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
os.chdir(os.getcwd() + os.sep + folder_name)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
video = cv2.VideoWriter('{}.avi'.format(datetime.now().strftime('%Y%m%d_%H%M%S')), fourcc, FPS, (W, H))

try:
    while True:
        ts = datetime.now()
        
        ret, cam_frame = cam.read()
        cv2.putText(cam_frame, ts.strftime('%Y-%m-%d %H:%M:%S'), (10, 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1)
        video.write(cam_frame)
        
        # show the frame
        cv2.imshow("Camera", cam_frame)
        key = cv2.waitKey(1) & 0xFF
        
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            cam.release()
            video.release()
            break
        
        sleep_duration = INTERVAL - (datetime.now() - ts).microseconds / 1000000
        
        if sleep_duration > 0:
            time.sleep(sleep_duration)
        
except KeyboardInterrupt:
    # release the video and save the timestamp
    cam.release()
    video.release()
