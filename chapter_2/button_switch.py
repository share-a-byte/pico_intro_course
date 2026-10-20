from machine import Pin
import time

# set up pin 15 as an input with a pull-down resistor
button = Pin(15, Pin.IN, Pin.PULL_UP)



while True:
    print(button.value()) # read the digital state of the button pin and then print it to shell
    time.sleep(0.1) # without this sleep you may run into issue, it just slows it down a little
