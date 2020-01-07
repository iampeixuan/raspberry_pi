from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2


# initialize the camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 20
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)

# capture frames from the camera
print("Started capturing, press 'q' to exit...")
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the image as numpy array 
    image = frame.array

    # show the frame
    cv2.imshow("Camera", image)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

