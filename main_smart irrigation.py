from time import sleep
import network
from machine import Pin,PWM, ADC
import BlynkLib
Motor = Pin(0, Pin.OUT)


soil_sensor = ADC(26)


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("OVT-0C96BD","12345678")
BLYNK_AUTH = 'sUzw-G3UqU0qzk-3u1_eSyJ0WzCGlmNw'
 
# connect the network       
wait = 10
while wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    wait -= 1
    print('waiting for connection...')
    sleep(1)
 
# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    ip=wlan.ifconfig()[0]
    print('IP: ', ip)
    
 
"Connection to Blynk"
# Initialize Blynk - FORCE UNSECURED CONNECTION
blynk = BlynkLib.Blynk(BLYNK_AUTH, port=80, insecure=True)
 
# Register virtual pin handler
                      #virtual pin V0

def read_moisture():
    data = soil_sensor.read_u16()
    water_percent = round(100 - (data / 65535)*100)
    print("moisture=",data)
    print("water %=",water_percent)
    return water_percent
    
        
'''@blynk.on("V1")
def v1_write_handler(value):
    print("V1", value[0])
    if moisture < 40:
        Motor.on()
    else:
        Motor.off()'''
            

        
    

            
        
while True:
    blynk.run()
    moisture = read_moisture()
    blynk.virtual_write(3,moisture)
    if moisture < 40:
        Motor.on()
    else:
        Motor.off()
    
''' if moisture < 40:
        blynk.log_event("dry", "Please water the plant!")
        print("dry")
    sleep(1) '''
        

    