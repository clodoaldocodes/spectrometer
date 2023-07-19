from gpiozero import Button
import gpiozero

PIN = 21
button = Button(PIN)

def say_hello():
    print("Hello!")

def say_goodbye():
    print("Goodbye!")

while True:
    button.when_pressed = say_hello