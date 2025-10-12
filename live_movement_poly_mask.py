import cv2
import numpy as np
import time

loop_counter = 0
#
#


#------------------------------------------------
mask_enabled = False
mask_enabled = True

show_movement = False
# show_movement = True

# Camera default size 1024, 1280

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# Create a blank image to be used as a mask

height = 1024   # height
width = 1280  # width
colordepth = 3
blank_image = 255 * np.zeros(shape=(height, width, colordepth), dtype=np.uint8)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

pts = np.array([[0,600],[450,350],[1280,350],[1280,500],[0,800]], np.int32)
pts = pts.reshape((-1,1,2))
# print (pts)

    # [[[   0  500]]
    #  [[ 560  390]]
    #  [[1500  350]]
    #  [[1600  600]]
    #  [[   0  800]]]

#  original size 1600 - x 900
# In NumPy, the reshape() function modifies the shape of an array without altering its data. 
# It returns a new array with the specified dimensions, provided the total number of elements remains constant.

# cv2.polylines(frame3,[pts],isClosed=True,color=(255,0,0),thickness=3)   # BGR format
cv2.fillPoly(blank_image, [pts], color=(255, 255, 255)) # Green color
# cv2.imshow("blank_image", blank_image)       

# print ("Waiting 5")
# time.sleep (5)

graymask = cv2.cvtColor(blank_image, cv2.COLOR_BGR2GRAY)


#------------------------------------------------
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

ret, frame1 = cap.read()
# time.sleep(5)
# ret, frame2 = cap.read()
# print (f"Size of image original image:  FIRST READS {frame1.shape}   {frame2.shape}")
# time.sleep(5)

previous_image = frame1   # Clean, unmarked frames
#========================================================

#========================================================



while cap.isOpened():

    ret, frame2 = cap.read()
    # print (f"Size of image original image: {frame2.shape}")

    # frame3 = cv2.resize(frame2, (1600,900))
    # print (f"Size of image image: {frame3.shape}")


    if (mask_enabled):      # Create an image and mask it.  Result is masked_image

        ## Get the shape of the image from the camera
        ######  h, w, c = frame2.shape

        ## Create a blank image of the same size
        ###### blank_image2 = 255 * np.zeros(shape=(h, w, c), dtype=np.uint8)
        # blank_image2 = 255 * np.ones(shape=(h, w, c), dtype=np.uint8)
        # cv2.rectangle(img, pt1, pt2, color[, thickness[, lineType[, shift]]])
        # cv2.rectangle(blank_image2,(0,300), (1919,700), (255, 255, 255))

        ## Draw a rectangle on the image
        ###### cv2.rectangle(blank_image2, (0,300), (1919,700), 255, -1)
        
        ## Make the image a gray scale
        # graymask = cv2.cvtColor(blank_image, cv2.COLOR_BGR2GRAY)

        ## Apply the mask
        masked_image = cv2.bitwise_and(blank_image, frame2, mask=graymask)

        # blank_image3 = cv2.resize(masked_image, (960,540))
        # cv2.imshow("Masked:  frame2", masked_image)
        # time.sleep(5)

        # frame2 = masked_image
        # print ("Masked")
    else:
        masked_image = frame2

    if (show_movement):

        masked_image_with_lines = masked_image

        # display the current masked_image and wait 10 seconds
        # cv2.imshow("masked_image_with_lines==", masked_image_with_lines)       
        # print ("Showing:  masked_image_with_lines========")
        # time.sleep (20)



        diff = cv2.absdiff(previous_image, masked_image)    # masked_image is the latest image with masking
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
####            cv2.rectangle (frame1, (x,y),   (x+w, y+h),     (0, 255, 0), 2)
            cv2.rectangle (masked_image_with_lines, (x,y),   (x+w, y+h),     (0, 255, 0), 2)
            # cv2.rectangle (frame1, (x_start,y_start),(x_end, y_end), (0, 0, 255), 2)
            # cv2.rectangle   (frame1, ( x+(w/2), y+(h/2)), (x+w-(w/2), y+h-(h/2) ), (255, 0, 0), 2)
            ##cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
            ##            1, (0, 0, 255), 3)
        # frame3 = masked_image
        previous_image = masked_image

        print ("Showing image with single lines  2")
        cv2.imshow("WindowName", masked_image_with_lines)       

        # time.sleep(5)



    else:
        frame3 = frame2
        masked_image_with_lines = frame2

    ### frame3 = cv2.resize(frame1, (1600,900))
        
    # pts = np.array([[0,500],[560,350],[1500,350],[1600,500],[0,800]], np.int32)
    # pts = pts.reshape((-1,1,2))
    # # print (pts)

    #     # [[[   0  500]]
    #     #  [[ 560  390]]
    #     #  [[1500  350]]
    #     #  [[1600  600]]
    #     #  [[   0  800]]]

    # # In NumPy, the reshape() function modifies the shape of an array without altering its data. 
    # # It returns a new array with the specified dimensions, provided the total number of elements remains constant.

    # # cv2.polylines(frame3,[pts],isClosed=True,color=(255,0,0),thickness=3)   # BGR format
    # cv2.fillPoly(frame3, [pts], color=(0, 255, 0)) # Green color

    # Create a window named 'image'
    cv2.namedWindow('WindowName', cv2.WINDOW_AUTOSIZE)
    cv2.imshow("WindowName", masked_image_with_lines)       
    cv2.moveWindow("WindowName", 50, 50)
        
    # frame1 = frame2

    loop_counter = loop_counter + 1

    if (loop_counter > 100):
        break

    # if cv2.waitKey(1) == ord("q"):        # origina
    if (cv2.waitKey(1000) & 0xFF) == ord('q'):
        break


cv2.destroyAllWindows()
cap.release()
