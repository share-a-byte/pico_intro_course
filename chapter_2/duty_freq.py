# Set the LED voltage output pin to be PVM based on potentiometer

# Step 1: Set LED voltage output pin to be PVM

from machine import Pin, PWM, ADC
import time

led_power = Pin(16, Pin.OUT)
pwm_power = PWM(led_power, freq=1000, duty_u16=1000)

max_range = 65535

potentiometer = ADC(26)

while True:
    val = potentiometer.read_u16()
    pwm_power.duty_u16(val)
    time.sleep(0.5)