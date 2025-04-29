import threading
import time
from sshkeyboard import listen_keyboard, stop_listening

# Install SSHKeyboard on RPI5:

# python3  -m venv /home/a/python
# ./pip3 install sshkeyboard


global_key = "-"

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

def task1():
    for index in range(5):
        print("Starting task: ")
        time.sleep(5)
        print ("After delay")
 
def read_key_press(key):
    global global_key
    global_key = key
    stop_listening()

def print_header():
    print ("=================================")
    print ("Move Left for one second  = l ")
    print ("Move Right for one second = r ")
    print ("Quit = q")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
def main():
    # thread1 = threading.Thread(target=task1, args=("Task 1",))
    thread1 = threading.Thread(target=task1, daemon=True)
    thread1.start()

    done = False
    while (not done):
        print_header()
        listen_keyboard(on_press = read_key_press,)

        if (global_key == "up"):
            print ("Up key pressed")

        if (global_key == "down"):
            print ("Down key pressed")

        if (global_key == "l") or (global_key == "left"):
            print ("Move Left for 1 second")

        if (global_key == "r") or (global_key == "right"):
            print ("Move Right for 1 second")

        if (global_key == "q"):
            done = True

    thread1.join()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

if __name__ == "__main__":
    main()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 



