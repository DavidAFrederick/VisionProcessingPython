import cv2
import numpy as np

cap = cv2.VideoCapture(0)

ret, frame1 = cap.read()
ret, frame2 = cap.read()

mask_enabled = True
mask_enabled = False

while cap.isOpened():

# Creating a Mask or Region of Interest (ROI)
#  1080H x 1920W

    ret, frame2 = cap.read()

    if (mask_enabled):

        ## Get the shape of the image from the camera
        h, w, c = frame2.shape

        ## Create a blank image of the same size
        blank_image2 = 255 * np.zeros(shape=(h, w, c), dtype=np.uint8)
        # blank_image2 = 255 * np.ones(shape=(h, w, c), dtype=np.uint8)
        # cv2.rectangle(img, pt1, pt2, color[, thickness[, lineType[, shift]]])
        # cv2.rectangle(blank_image2,(0,300), (1919,700), (255, 255, 255))

        ## Draw a rectangle on the image
        cv2.rectangle(blank_image2, (0,300), (1919,700), 255, -1)
        
        ## Make the image a gray scale
        graymask = cv2.cvtColor(blank_image2, cv2.COLOR_BGR2GRAY)

        ## Apply the mask
        masked_image = cv2.bitwise_and(frame2, frame2, mask=graymask)

        # blank_image3 = cv2.resize(masked_image, (960,540))
        # cv2.imshow("Maskded:", blank_image3)

        frame2 = masked_image
        # print ("Masked")

    diff = cv2.absdiff(frame1, frame2)    
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # print(":",len(contours))
    # print(contours)
# 
    thresholdsize = 600
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        

        # if (len(contours) > 3 ):

        #     pass
        # if cv2.contourArea(contour) > thresholdsize:
        #     print ("|",cv2.contourArea(contour),"|" )

        if cv2.contourArea(contour) < thresholdsize:
            continue

        h2 = int(h/2)
        w2 = int(w/2)
        x_start = x + w2
        y_start = y + h2
        x_end   = x_start + 4
        y_end   = y_start + 4

        # cv2.rectangle (frame1, (x,y),               (x+w, y+h),     (0, 255, 0), 2)  #  Original
        cv2.rectangle (frame1, (x,y),   (x+w, y+h),     (0, 255, 0), 2)
        # cv2.rectangle (frame1, (x_start,y_start),(x_end, y_end), (0, 0, 255), 2)
        # cv2.rectangle   (frame1, ( x+(w/2), y+(h/2)), (x+w-(w/2), y+h-(h/2) ), (255, 0, 0), 2)
        ##cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
        ##            1, (0, 0, 255), 3)

    frame3 = cv2.resize(frame1, (960,540))
    cv2.imshow("feed", frame3)         #<<<<<<<<
    # cv2.imshow("Blank:", blank_image2)
    frame1 = frame2

    # if cv2.waitKey(1) == ord("q"):        # origina
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
