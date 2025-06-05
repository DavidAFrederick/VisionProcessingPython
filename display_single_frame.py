import cv2
import numpy as np

counter = 1
cap = cv2.VideoCapture('output.avi')


# frame_width = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# frame_height =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))
# fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
# out = cv2.VideoWriter("output.avi", fourcc, 5.0, (1280,720))

ret, frame1 = cap.read()
print(f"Size of image {frame1.shape}   counter {counter}")

while cap.isOpened():
    counter = counter + 1
    ret, frame1 = cap.read()
    print(f"Size of image {frame1.shape}   counter {counter}")
    image = cv2.resize(frame1, (1280,720))
    cv2.imshow("feed", image)

    if cv2.waitKey(0) == 27:
        break

cv2.destroyAllWindows()
cap.release()
