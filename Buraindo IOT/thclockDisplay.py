import RPi.GPIO as GPIO
import adafruit_dht
import board
import time
import pyrebase

from time import sleep, strftime
from datetime import datetime

from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.led_matrix.device import max7219
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, LCD_FONT,TINY_FONT, SINCLAIR_FONT

#FIREBASE
config = {
    "apiKey": "AIzaSyC1D2pTQFJxBBK_BA2ibR1qdhMxk0slUIs",
    "authDomain": "buraindosettime-cef33.firebaseapp.com",
    "databaseURL": "https://buraindosettime-cef33-default-rtdb.firebaseio.com",
    "projectId?": "buraindosettime-cef33",
    "storageBucket": "buraindosettime-cef33.appspot.com",
    "messagingSenderId": "632727726500",
    "appId": "1:632727726500:web:0a74b1a141de84374bf931",
    "measurementId": "G-PL4CDP270R"

    }

firebase = pyrebase.initialize_app(config)
db = firebase.database()
#FIREBASE

#DHT22
dht = adafruit_dht.DHT22(board.D21)
dht = adafruit_dht.DHT22(board.D21, use_pulseio=False)
#DHT22

#MAX7219
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, width=32, height=8, block_orientation=-90, blocks_arranged_in_reverse_order=False)
virtual = viewport(device, width=32, height=16)
serial2 = spi(port=0, device=1, gpio=noop())
device2 = max7219(serial2, width=32, height=8, block_orientation=-90,blocks_arranged_in_reverse_order=False)
virtual2 = viewport(device2, width=32, height=16)
device.contrast(100)
device2.contrast(100)
#MAX7219

#Clearing max7219
with canvas(virtual2) as draw:
    text(draw, (0, 1),"", fill="white", font=proportional(LCD_FONT))
with canvas(virtual) as draw:
    text(draw, (4, 1),"", fill="white", font=proportional(LCD_FONT))
    time.sleep(2)
#Clearing max7219

#First loop display 24 hours format and Temperature
while True:
    time12Temp = 0
    time24Hum = 0
    while time12Temp !=5:
        try:
            temperature = dht.temperature
            humidity = dht.humidity
            time12Temp+=1
            temp = ("T:{:.1f}".format(temperature))
            print("T:{:.1f} H:{}% {}".format(temperature, humidity , time12Temp))
            with canvas(virtual2) as draw:
                text(draw, (0, 1),temp, fill="white", font=proportional(LCD_FONT))
            with canvas(virtual) as draw:
                text(draw, (4, 1), datetime.now().strftime('%H:%M'), fill="white", font=proportional(LCD_FONT))
            time.sleep(1)

            data = {
            "Humidity" : humidity,
            "Temperature" : temperature,
            "Clock" : datetime.now().strftime('%H:%M'),
            "Clock2" : datetime.now().strftime('%I:%M')
            }
            
            db.child("Smart_Blinds").update(data)
                
        except RuntimeError as e:
            print("Reading from DHT failure: ", e.args)
            time.sleep(0.5)
        except KeyboardInterrupt:
            GPIO.cleanup()
            print("Stopped")
#First loop display 24 hours format and Temperature

#Second loop display 12 hours format and Humidity
    while time24Hum != 5:
        try:
            temperature = dht.temperature
            humidity = dht.humidity
            humid = ("H:{}".format(humidity))
            time24Hum+=1
            print("T:{:.1f} H:{}% {}".format(temperature, humidity, time24Hum))
            with canvas(virtual2) as draw:
                text(draw, (1, 1),humid, fill="white", font=proportional(LCD_FONT))
            with canvas(virtual) as draw:
                text(draw, (4, 1), datetime.now().strftime('%I:%M'), fill="white", font=proportional(LCD_FONT))
            time.sleep(1)
            
            data = {
            "Temperature" : temperature,
            "Humidity" : humidity,
            "Clock" : datetime.now().strftime('%H:%M'),
            "Clock2" : datetime.now().strftime('%I:%M')
            }
            db.child("Smart_Blinds").update(data)    
           
        except RuntimeError as e:
            print("Reading from DHT failure: ", e.args)
            time.sleep(0.5)
        except KeyboardInterrupt:
            GPIO.cleanup()
            print("Stopped")
#Second loop display 12 hours format and Humidity            

