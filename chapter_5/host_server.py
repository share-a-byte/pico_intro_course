import network
import time
import socket
from machine import Pin, ADC, PWM

led = Pin("LED", Pin.OUT)
temp_sensor = ADC(4)
pwm_pin = PWM(Pin(16))
pwm_pin.freq(1000)

def read_temperature():
    conversion_factor = 3.3 / (65535)
    
    reading = temp_sensor.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706) / 0.001721
    
    return temperature

state = "OFF"

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    while wlan.isconnected() == False:
        print("connecting, please wait...")
        time.sleep(1)
        
    print("connected! IP = ", wlan.ifconfig()[0])
    
def open_socket():
    address = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(address)
    s.listen(3)
    return s

def web_page(state, temperature):
    html = f"""<!DOCTYPE html>
    <html>
    <head> <title>Pico W</title> </head>
    <body> <h1>Pico W HTTP Server</h1>
    <form action="./on">
    <input type="submit" value="Turn Light On" />
    </form>
    <form action="./off">
    <input type="submit" value="Turn Light Off" />
    </form>
    <p>LED state: {state} </p>
    <p>Temperature is: {temperature} </p>
    <input type="range" min="0" max="100" value="50" onchange="window.location.href = '/slider1?' + this.value "/>
    </body>
    </html>
    """
    return str(html)

def ap_setup():
    ssid = "my-wifi"
    password = "password"
    ap = network.WLAN(network.AP_IF) # access point
    ap.config(essid=ssid, password=password)
    ap.active(True)
    
    while ap.active() == False:
        print("Connecting..")
        time.sleep(1)
        
    print("Connected to ip: ", ap.ifconfig()[0])

# connect()
ap_setup()
s = open_socket()

try:
    while True:
        client = s.accept()[0]
        request = client.recv(1024)
        request = str(request)
        print(request)
        path, parameters = None, None
        
        try:
            request = request.split()[1]
            path, parameters = request.split("?")
            print(request)
        except:
            pass
        
        if path == "/on":
            led.value(1)
            state = "ON"
        elif path == "/off":
            led.value(0)
            state = "OFF"
        elif path == "/slider1":
            pwm = int(int(parameters) * 65535 / 100)
            pwm_pin.duty_u16(pwm)
            print(pwm)
            
        temperature = read_temperature()
        
        html = web_page(state, temperature)
        client.send('HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n')
        client.send(html)
        request = str(request)
        print(request)
        client.close()
    
except OSError as e:
    print("Found exception: ", e)
    client.close()