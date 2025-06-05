import cv2
import numpy as np
import time

counter = 0

# Open the default camera
cap = cv2.VideoCapture(0)


width = 1920
height = 1080
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# cap = cv2.VideoCapture('vtest.avi')
frame_width = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))
print (f"Size:  H: {frame_height}   W: {frame_width}")



fourcc = cv2.VideoWriter_fourcc('X','V','I','D')

# out = cv2.VideoWriter("output.avi", fourcc, 5.0, (1280,720))
out = cv2.VideoWriter("output.avi", fourcc, 5.0, (1920,1080))

# 1920,1080

ret, frame1 = cap.read()
print(frame1.shape)

while cap.isOpened():
    counter = counter + 1
    string_counter = str(counter)
    # image = cv2.resize(frame1, (1280,720))
    cv2.putText(frame1, string_counter, (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 3)
    # out.write(image)

    out.write(frame1)

    cv2.imshow("feed", frame1)
    time.sleep(1.0)

    ret, frame1 = cap.read()

    if cv2.waitKey(40) == 27:
        break

cv2.destroyAllWindows()
cap.release()
out.release()
