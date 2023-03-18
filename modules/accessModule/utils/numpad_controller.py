import _thread
import time
import logging


from .numpad_const import *
from .lcd_controller import *

User_Key = "null"
numero_depto = ""


def Keyboard_Scanner():
    global User_Key
    Lock = "UNLOCKED"  # Variable Lock is used to compare against for action to occur

    while True:  # loop forever
        Key_Pressed = "null"
        GPIO.output(R1, GPIO.HIGH)
        GPIO.output(R2, GPIO.LOW)
        GPIO.output(R3, GPIO.LOW)
        GPIO.output(R4, GPIO.LOW)
        if GPIO.input(C1) == True:
            keyPressed("1")  # check each button in column
        if GPIO.input(C2) == True:
            keyPressed("2")
        if GPIO.input(C3) == True:
            keyPressed("3")
        if GPIO.input(C4) == True:
            keyPressed("A")

        GPIO.output(R1, GPIO.LOW)
        GPIO.output(R2, GPIO.HIGH)
        GPIO.output(R3, GPIO.LOW)
        GPIO.output(R4, GPIO.LOW)
        if GPIO.input(C1) == True:
            keyPressed("4")
        if GPIO.input(C2) == True:
            keyPressed("5")
        if GPIO.input(C3) == True:
            keyPressed("6")
        if GPIO.input(C4) == True:
            keyPressed("B")

        GPIO.output(R1, GPIO.LOW)
        GPIO.output(R2, GPIO.LOW)
        GPIO.output(R3, GPIO.HIGH)
        GPIO.output(R4, GPIO.LOW)
        if GPIO.input(C1) == True:
            keyPressed("7")
        if GPIO.input(C2) == True:
            keyPressed("8")
        if GPIO.input(C3) == True:
            keyPressed("9")
        if GPIO.input(C4) == True:
            keyPressed("C")

        GPIO.output(R1, GPIO.LOW)
        GPIO.output(R2, GPIO.LOW)
        GPIO.output(R3, GPIO.LOW)
        GPIO.output(R4, GPIO.HIGH)
        if GPIO.input(C1) == True:
            keyPressed("*")
        if GPIO.input(C2) == True:
            keyPressed("0")
        if GPIO.input(C3) == True:
            keyPressed("#")
        if GPIO.input(C4) == True:
            keyPressed("D")

        if (Lock == "LOCKED") and (Key_Pressed == "null"):
            Lock = "UNLOCKED"

        # Key was pressed and because Lock wasn't locked, this is a new key press
        # Lock the routine from processing another keypress until
        # User_Key is processed in the main loop AND the the button was released
        # which prevents key repeating
        #
        if (Lock == "UNLOCKED") and (Key_Pressed != "null"):
            Lock = "LOCKED"

        time.sleep(0.02)


def keyPressed(key):
    global User_Key
    global numero_depto
    
    if (User_Key == "null"):
        if (key == "A"):
            User_Key = key
            lcd_string("Indique Depto", 1)
        if (key == "B"):
            User_Key = key
            lcd_string("Opcion B", 1)
        if (key == "C"):
            User_Key = key
            lcd_string("Opcion C", 1)
        if (key == "D"):
            User_Key = key
            lcd_string("Opcion D", 1)
    else:
        if (User_Key == "A"):
            if (key == "B"):
                key = ""
                numero_depto = ""
            if (key == "C"):
                lcd_string("Esperando Respuesta", 1)
                lcd_string("Depto " + numero_depto, 2)
            else:    
                numero_depto = numero_depto + key
                lcd_string("Depto: " + numero_depto, 1)
        if (User_Key == "B"):
            numero_depto = numero_depto + key
            lcd_string("Opcion B", 1)
        if (User_Key == "C"):
            numero_depto = numero_depto + key
            lcd_string("Opcion C", 1)
        if (User_Key == "D"):
            numero_depto = numero_depto + key
            lcd_string("Opcion D", 1)
    time.sleep(0.5)
    
