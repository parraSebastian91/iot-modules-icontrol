# Matrix keypad - digital 4 x 4 - Threaded and with buffering to remove key repeats
# The thread handles the keyboard scanning, leaving the main loop to handle other tasks.
# When a key is pressed, the value is written to a global variable 'User_Key'.
# The thread now stops checking for key presses until User_Key is processed in the main loop and
# the button is released.
# The main loop must process User_Key and then set it to 'null'.

import RPi.GPIO as GPIO

import time
import _thread

# setup the inputs and outputs according to the matrix keypad's wiring
# R1 = machine.Pin(15,machine.Pin.OUT)
# R2 = machine.Pin(14,machine.Pin.OUT)
# R3 = machine.Pin(13,machine.Pin.OUT)
# R4 = machine.Pin(12,machine.Pin.OUT)
# C1 = machine.Pin(11,machine.Pin.IN,machine.Pin.PULL_DOWN)
# C2 = machine.Pin(10,machine.Pin.IN,machine.Pin.PULL_DOWN)
# C3 = machine.Pin(9,machine.Pin.IN,machine.Pin.PULL_DOWN)
# C4 = machine.Pin(8,machine.Pin.IN,machine.Pin.PULL_DOWN)
R1 = 29
R2 = 32
R3 = 33
R4 = 31
C1 = 11
C2 = 12
C3 = 13
C4 = 15
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(R1, GPIO.OUT)
GPIO.setup(R2, GPIO.OUT)
GPIO.setup(R3, GPIO.OUT)
GPIO.setup(R4, GPIO.OUT)
GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

User_Key = "null"  # User pressed key, is set in thread, but can be read in main loop


# This function will handle the keyboard and run in its own thread.
def Keyboard_Scanner():
    global User_Key
    Lock = "UNLOCKED"  # Variable Lock is used to compare against for action to occur

    while True:  # loop forever
        Key_Pressed = "null"  # Set variable to 'null' at start of scan

        # Power each row one by one. While a row is powered, test the four columns
        # to see if any are "high", thus being pressed.  If a button is pressed
        # record that button value in variable Key_Pressed.
        # R1.value(1)  # set power ON for row 1, off for the other three
        # R2.value(0)
        # R3.value(0)
        # R4.value(0)
        GPIO.output(R1, GPIO.HIGH)
        GPIO.output(R2, GPIO.LOW)
        GPIO.output(R3, GPIO.LOW)
        GPIO.output(R4, GPIO.LOW)
        if GPIO.input(C1) == True:
            Key_Pressed = "1"  # check each button in column
        if GPIO.input(C2) == True:
            Key_Pressed = "2"
        if GPIO.input(C3) == True:
            Key_Pressed = "3"
        if GPIO.input(C4) == True:
            Key_Pressed = "A"

        # R1.value(0)  # set power ON for row 2, off for the other three
        # R2.value(1)
        # R3.value(0)
        # R4.value(0)
        GPIO.output(R1, GPIO.LOW)
        GPIO.output(R2, GPIO.HIGH)
        GPIO.output(R3, GPIO.LOW)
        GPIO.output(R4, GPIO.LOW)
        if GPIO.input(C1) == True:
            Key_Pressed = "4"
        if GPIO.input(C2) == True:
            Key_Pressed = "5"
        if GPIO.input(C3) == True:
            Key_Pressed = "6"
        if GPIO.input(C4) == True:
            Key_Pressed = "B"

        # R1.value(0)  # set power ON for row 3, off for the other three
        # R2.value(0)
        # R3.value(1)
        # R4.value(0)
        GPIO.output(R1, GPIO.LOW)
        GPIO.output(R2, GPIO.LOW)
        GPIO.output(R3, GPIO.HIGH)
        GPIO.output(R4, GPIO.LOW)
        if GPIO.input(C1) == True:
            Key_Pressed = "7"
        if GPIO.input(C2) == True:
            Key_Pressed = "8"
        if GPIO.input(C3) == True:
            Key_Pressed = "9"
        if GPIO.input(C4) == True:
            Key_Pressed = "C"

        # R1.value(0)  # set power ON for row 4, off for the other three
        # R2.value(0)
        # R3.value(0)
        # R4.value(1)
        GPIO.output(R1, GPIO.LOW)
        GPIO.output(R2, GPIO.LOW)
        GPIO.output(R3, GPIO.LOW)
        GPIO.output(R4, GPIO.HIGH)
        if GPIO.input(C1) == True:
            Key_Pressed = "*"
        if GPIO.input(C2) == True:
            Key_Pressed = "0"
        if GPIO.input(C3) == True:
            Key_Pressed = "#"
        if GPIO.input(C4) == True:
            Key_Pressed = "D"

        # if lock was Locked, check to see if it can be unlocked
        # If we get through the keypad scan without seeing a Key_Press
        # value other than null, no key is pressed, so lets unlock the function.
        if (Lock == "LOCKED") and (Key_Pressed == "null"):
            Lock = "UNLOCKED"

        # Key was pressed and because Lock wasn't locked, this is a new key press
        # Lock the routine from processing another keypress until
        # User_Key is processed in the main loop AND the the button was released
        # which prevents key repeating
        #
        if (Lock == "UNLOCKED") and (Key_Pressed != "null"):
            Lock = "LOCKED"
            User_Key = Key_Pressed

        time.sleep(0.02)  # slow down the loop a bit as full speed isn't needed


# This starts the thread running
_thread.start_new_thread(Keyboard_Scanner, ())


# Main Loop to do all the other work needed
while True:
    if User_Key != "null":  # Check for value in User_Key and act on it
        Key_Code = User_Key  # Copy User_Key to  a variable used within main loop
        User_Key = "null"  # Reset User_Key to null so it can be written to again
        print("Key Code =", Key_Code)

    # A sleep just to slow things down to mimic work being performed
    time.sleep(0.1)
    # here in the main loop is where all the normal processing happens

GPIO.cleanup()
