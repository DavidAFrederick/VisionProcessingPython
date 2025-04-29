import threading
import time

def my_function():
    print("This function runs once per second.")

def execute_periodically(interval, function):
    while True:
        function()
        time.sleep(interval)

if __name__ == "__main__":
    interval_seconds = 1
    # Create a thread that executes the function periodically
    periodic_thread = threading.Thread(target=execute_periodically, args=(interval_seconds, my_function))
    # Set the thread as a daemon so it will exit when the main program exits
    periodic_thread.daemon = True
    # Start the thread
    periodic_thread.start()
    # Keep the main thread alive to allow the periodic thread to run
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Program terminated.")

###########################
import threading
import time

def background_task():
    while True:
        print("Background task running...")
        time.sleep(1)

if __name__ == "__main__":
    background_thread = threading.Thread(target=background_task, daemon=True)
    background_thread.start()

    try:
        while True:
            print("Main thread running...")
            time.sleep(5)
    except KeyboardInterrupt:
        print("Exiting...")