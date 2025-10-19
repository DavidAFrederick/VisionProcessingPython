import cv2

def display_video_one_frame_at_a_time(video_path):
    """
    Displays an AVI video one frame at a time, advancing to the next frame
    upon a key press.

    Args:
        video_path (str): The path to the AVI video file.
    """
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Could not open video file '{video_path}'")
        return

    frame_number = 0
    while True:
        ret, frame = cap.read()

        if not ret:
            print("End of video stream.")
            break

        frame_number += 1
        cv2.imshow(f"Frame {frame_number}", frame)
        cv2.moveWindow(f"Frame {frame_number}", 50, 50)

        # Wait for a key press (any key) to advance to the next frame
        # If 'q' is pressed, exit the loop
        key = cv2.waitKey(0) & 0xFF
        if key == ord('q'):
            break
        cv2.destroyAllWindows()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Replace 'your_video.avi' with the actual path to your AVI video file
    video_file = "/home/a/vision_movement_files/10_12_20_55_09Movement.avi"
    display_video_one_frame_at_a_time(video_file)