import os
import sys
import cv2
import time
import numpy as np
from datetime import datetime


if __name__ == '__main__':
    # get user input
    args = sys.argv[1:]
    show_frame = True
    try:
        if args[0] in  ["no_show", "noshow", "no"]:
            show_frame = False
            print("Not displaying camera frame.")
        else:
            print("Unknown argument.")
    except IndexError:
        pass
    
    # install v4l2 driver for pi-cam, cv2 requirement
    os.system('sudo modprobe bcm2835-v4l2') 

    # camera and video setuP (REMEMBER TO TUNE THIS BASED ON YOUR SETTINGS!)
    FPS = 15  
    INTERVAL = 1 / FPS
    W, H = 640, 480

    # open camera and warm-up
    cam = cv2.VideoCapture(0)  
    cam.set(3, W)
    cam.set(4, H)
    cam.read()  

    # create video file, named with current time
    folder_name = 'recordings'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    os.chdir(os.getcwd() + os.sep + folder_name)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_name = '{}.avi'.format(datetime.now().strftime('%Y%m%d_%H%M%S'))
    video = cv2.VideoWriter(video_name, fourcc, FPS, (W, H))
    
    # start recording
    print("Started recording {}, press 'ctrl+c' to stop.".format(video_name))
    try:
        while True:
            # get new camera frame and write to video file
            ts = datetime.now()
            success, cam_frame = cam.read()
            cv2.putText(cam_frame, ts.strftime('%Y-%m-%d %H:%M:%S'), (10, 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1)
            video.write(cam_frame)
            
            # display the frame, stop reocrding if `q` was pressed
            if show_frame:
                cv2.imshow("Camera", cam_frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    cam.release()
                    video.release()
                    break
            
            # try to match the FPS setting
            time_taken = (datetime.now() - ts).microseconds / 1000000
            sleep_duration = INTERVAL - time_taken
            if sleep_duration > 0:
                time.sleep(sleep_duration)
            #print(time_taken, 1/time_taken)
            
    except KeyboardInterrupt:
        cam.release()
        video.release()
