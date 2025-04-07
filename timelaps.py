import cv2
import numpy as np
import time
from datetime import datetime


count = 0

cap = cv2.VideoCapture(0)    # Open Camera
ret, frame1 = cap.read()     # Read a frame

frame_width = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
out = cv2.VideoWriter("output.avi", fourcc, 5.0, (1280,720))

while cap.isOpened():

    now = datetime.now()
    current_hour = str(now.hour)
    current_minute = str(now.minute)
    time_string = current_hour + ":" + current_minute

    ret, frame1 = cap.read()
    image = cv2.resize(frame1, (1280,720))
    cv2.putText(image, time_string, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    out.write(image)
    cv2.imshow("feed", image)
    time.sleep(1)

    count = count + 1
    number_of_seconds_to_terminate = 60 * 60 * 6
    # number_of_seconds_to_terminate = 16
    print ("Count: ", count)

    if (cv2.waitKey(1) & 0xFF) == ord('q') or (count >= number_of_seconds_to_terminate):
        break

cv2.destroyAllWindows()
cap.release()
out.release()
