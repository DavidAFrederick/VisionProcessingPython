
#==(Libraries)========================================================
import cv2
import numpy as np
import time

#==(Variables and Constants)==========================================
first_pass = True
loop_counter = 0
number_of_loops = 3000

mask_enabled = False
mask_enabled = True

show_movement = False
show_movement = True

# Camera default size 1024, 1280
height = 1024   # height
width = 1280  # width
colordepth = 3

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def create_mask_for_blanking(_height, _width, _colordepth):        #  not  sure of the return variable type
    # Create a blank image to be used as a mask
    _blank_image = 255 * np.zeros(shape=(_height, _width, _colordepth), dtype=np.uint8)

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

    cv2.fillPoly(_blank_image, [pts], color=(255, 255, 255)) # Green color

    _graymask = cv2.cvtColor(_blank_image, cv2.COLOR_BGR2GRAY)

    # cv2.imshow("graymask", _graymask) 
    # cv2.waitKey(6000)
    # cv2.destroyWindow("graymask")

    return _graymask

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def get_camera(_height,_width):

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, _width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, _height)
    ret, frame1 = cap.read()          # First picture is not used
    print (f"Size of image original image:  FIRST READS {frame1.shape} ")
    return cap

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def get_image_from_camera (_camera):
    ret, _frame = _camera.read()
    return _frame

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def apply_mask_to_image(mask_for_image, camera_image, bypass_this_function = True):

    if (bypass_this_function):
        return camera_image
    else:
        _bw_camera_image = cv2.cvtColor(camera_image, cv2.COLOR_BGR2GRAY)
        masked_image = cv2.bitwise_and(mask_for_image, _bw_camera_image, mask=graymask)

        return masked_image

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def detect_and_box_movement(original_image, _frame1, _frame2):
    # original_frame = _frame1.copy()
    # _diff_frame = cv2.absdiff(_frame1, _frame2)   
    _gray_frame = cv2.absdiff(_frame1, _frame2)   
    # _gray_frame = cv2.cvtColor(_diff_frame, cv2.COLOR_BGR2GRAY)

    # if (loop_counter > 10):
    #     cv2.imshow("_frame1", _frame1) 
    #     cv2.waitKey(2000)
    #     cv2.destroyWindow("_frame1")

    #     cv2.imshow("_frame2", _frame2)     #  Frame 2 has rectangles
    #     cv2.waitKey(2000)
    #     cv2.destroyWindow("_frame2")


    _blur_frame = cv2.GaussianBlur(_gray_frame, (5,5), 0)
    _, _thresh_frame = cv2.threshold(_blur_frame, 20, 255, cv2.THRESH_BINARY)
    _dilated_frame = cv2.dilate(_thresh_frame, None, iterations=3)
    contours, _ = cv2.findContours(_dilated_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    thresholdsize = 600
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < thresholdsize:
            continue

        h2 = int(h/2)
        w2 = int(w/2)
        x_start = x + w2
        y_start = y + h2
        x_end   = x_start + 4
        y_end   = y_start + 4

        cv2.rectangle (original_image, (x,y),   (x+w, y+h),     (0, 255, 0), 2)

    return original_image

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def display_processed_image (image):
    # Create a window named 'image'
    windowName = "Frame: "
    # cv2.namedWindow('WindowName', cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow(windowName, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(windowName, image)       
    cv2.moveWindow(windowName, 50, 50)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def release_resources(_camera):
    cv2.destroyAllWindows()
    _camera.release()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

#==(Main)==================================================================================
graymask = create_mask_for_blanking(height, width, colordepth)
camera = get_camera(height,width)

while camera.isOpened() and (loop_counter < number_of_loops):

    frame1_original_image = get_image_from_camera(camera)
    masked_grayed_image = apply_mask_to_image(graymask, frame1_original_image, False)

    if (first_pass):
        masked_grayed_frame2 = masked_grayed_image
        first_pass = False

    highlighted_frame = detect_and_box_movement(frame1_original_image, masked_grayed_image, masked_grayed_frame2)  # masked_grayed_frame2 has rectangles

    display_processed_image(highlighted_frame)

    if (cv2.waitKey(2) & 0xFF) == ord('q'):
        break

    masked_grayed_frame2 = masked_grayed_image.copy()
    loop_counter = loop_counter + 1


release_resources(camera)


#==(End of Main)============================================================================







