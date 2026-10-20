from machine import Pin
import time

pin_16 = Pin(16, Pin.OUT)

while True:
    pin_16.value(1)
    time.sleep(2)
    
    print("hello")
    
    pin_16.value(0)
    time.sleep(2)