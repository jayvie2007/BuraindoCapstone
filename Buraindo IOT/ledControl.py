import time
import board
import neopixel
import pyrebase

#Firebase
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
#Firebase

#WS2812B Wiring and LED nodes counts
pixel_pin = board.D12
num_pixels = 150
ORDER = neopixel.GRB
#WS2812B Wiring and LED nodes counts


#Getting data from firebase
while True:
    BlindsOpen = db.child("Smart_Blinds").get("")
    tempvalue = BlindsOpen.val()
    value = [tempvalue[j] for j in tempvalue]
    normal = value[4]
    snake = value[5]
    flick = value[6]
    scroll = value[7]
    ledGet = value[9]
    isLedOpen = value[19]
    ledBrightness = value[20]
#Getting data from firebase
    
#Converting RGB to data to 3 ARRAYS
    brightSplit = ledBrightness.split('"')
    brightJoin = ''.join(brightSplit)
    intBright = float(brightJoin)
    ledArray = ledGet.split('"')
    ledJoin = ''.join(ledArray)
    ledArray2 = ledJoin.split(',')
    ledBright = intBright
    ledR = int(ledArray2[0])
    ledG = int(ledArray2[1])
    ledB = int(ledArray2[2])
#Converting RGB to data to 3 ARRAYS
    
#Initiating WS2812B
    pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness = ledBright, auto_write=False, pixel_order=ORDER
)
#Initiating WS2812B
                    
#LED CONDITIONS
#Turn on LED if true and set to scroll
    if isLedOpen == "true" and scroll == "true":
        print("scroll")
        for i in range(int(num_pixels/2), -1, -1):
            pixels[i] = (ledR,ledG,ledB)
            pixels[num_pixels - i- 1] = (ledR,ledG,ledB)
            pixels.show()
            time.sleep(0.03)
        if i == 0:
            for x in range(int(num_pixels/2)):
                pixels[x] = (0,0,0)
                pixels[num_pixels - x - 1] = (0,0,0)
                pixels.show()
                time.sleep(0.03)
#Turn on LED if true and set to scroll

    #elif isLedOpen == "true" and rainbowFlick =="true":
        #rainbow_flick(0.05)

#Turn on LED if true and set to snake
    elif isLedOpen == "true" and snake == "true":
        print("snake")
        for x in range(0, 150):
            pixels[x] = (ledR,ledG,ledB)
            pixels.show()
            time.sleep(0.01)
#Turn on LED if true and set to snake             
            
#Turn on LED if true and set to flick 
    elif isLedOpen == "true" and flick =="true":
        print("flick")
        for x in range(10):
            for y in range(3):
                for z in range(0, num_pixels, 3):
                    print(x)
                    pixels[z+y] = (ledR,ledG,ledB)
                    time.sleep(0.001)
                    
                pixels.show()
                for z in range(0, num_pixels,3):
                    pixels[z+y] = (0, 0, 0)
#Turn on LED if true and set to flick 

#Turn on LED if true and set to normal                     
    elif isLedOpen == "true" and normal == "true":
        print("normal")
        pixels.fill((ledR,ledG,ledB))
        pixels.show()
#Turn on LED if true and set to normal   

#Turn off LED if false        
    elif isLedOpen == "false":
        pixels.fill((0,0,0))
        pixels.show()
#Turn off LED if false           
#LED CONDITIONS        
