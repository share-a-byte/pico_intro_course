import ssd1306
import time
from machine import Pin, I2C

IS2_SCL_PIN = 9
IS2_SDA_PIN = 8
I2C_FREQ = 400000
OLED_ADDR = 0x3c

# Initialize I2C perhipheral
i2c = I2C(0, scl=Pin(IS2_SCL_PIN), sda=Pin(IS2_SDA_PIN), freq=I2C_FREQ)

# Initialise OLED display
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=OLED_ADDR)

# Initialise Atmospheric Sensor
# sensor = PiicoDev_BME280() # initialise the sensor

while True:
    oled.fill(0)
    oled.text("Hello world!", 40, 40)
    oled.show()