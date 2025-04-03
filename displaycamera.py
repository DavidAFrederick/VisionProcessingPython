import cv2

# Open the default camera
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # If frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Get image properties
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    fps = cap.get(cv2.CAP_PROP_FPS)
    # print(f"Camera   Height: {height}, Width: {width}, FPS: {fps}")

    # print (f"Frame 1 {frame.shape} ")

    frame2 = cv2.resize(frame, (960, 540)) 

    # print (f"Frame 2 {frame2.shape} ")


    # Display the resulting frame
    cv2.imshow('Camera Feed', frame2)

    # Press 'q' to exit
    if cv2.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()