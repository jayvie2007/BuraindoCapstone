import RPi.GPIO as GPIO
import board
import time
import pyrebase

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

#STEPPER
out1 = 17
out2 = 18
#out2 = 12
out3 = 27
out4 = 22

step_sleep = 0.002

# setting up
GPIO.setup( out1, GPIO.OUT )
GPIO.setup( out2, GPIO.OUT )
GPIO.setup( out3, GPIO.OUT )
GPIO.setup( out4, GPIO.OUT )
# initializing
GPIO.output( out1, GPIO.LOW )
GPIO.output( out2, GPIO.LOW )
GPIO.output( out3, GPIO.LOW )
GPIO.output( out4, GPIO.LOW )

def cleanup():
    GPIO.output( out1, GPIO.LOW )
    GPIO.output( out2, GPIO.LOW )
    GPIO.output( out3, GPIO.LOW )
    GPIO.output( out4, GPIO.LOW )

#Calling value from firebase
BlindsOpen = db.child("Smart_Blinds").get("")
tempvalue = BlindsOpen.val()
value = [tempvalue[j] for j in tempvalue]
time.sleep(1)
blindStop = value[1]
mtime = ('"{}"'.format(value[2]))
ntime = value[3]
blindClose = value[11]
blindOpen = value[12]
isBlindOpen = value[16]
manualSet = value[21]
sampleUp = int(value[23])
sampleZClose = value[24]
#Calling value from firebase

#Stepper conditions
#Open if clocks matches opening and blinds is false then open
if mtime == blindOpen and isBlindOpen == "false" and sampleZClose == "open":
    step_count = 3300
    sampleUp = 0
    manualSet = "temporary"
    sampleZClose = "temporary"
    isBlindOpen = "true"
    data = {
    "sampleUp" : sampleUp,
    "manualSet" : manualSet,
    "sampleZClose" : sampleZClose,
    "isBlindOpen" : isBlindOpen
            }
        
    db.child("Smart_Blinds").update(data)
    try:
        i = 0
        for i in range(step_count):
            if i%4==0:
                GPIO.output( out4, GPIO.LOW )
                GPIO.output( out3, GPIO.LOW )
                GPIO.output( out2, GPIO.LOW )
                GPIO.output( out1, GPIO.HIGH )
            elif i%4==1:
                GPIO.output( out4, GPIO.LOW )
                GPIO.output( out3, GPIO.HIGH )
                GPIO.output( out2, GPIO.LOW )
                GPIO.output( out1, GPIO.LOW )
            elif i%4==2:
                GPIO.output( out4, GPIO.LOW )
                GPIO.output( out3, GPIO.LOW )
                GPIO.output( out2, GPIO.HIGH )
                GPIO.output( out1, GPIO.LOW )
            elif i%4==3:
                GPIO.output( out4, GPIO.HIGH )
                GPIO.output( out3, GPIO.LOW )
                GPIO.output( out2, GPIO.LOW )
                GPIO.output( out1, GPIO.LOW )
            time.sleep( step_sleep )
            if i == step_count - 1:
                print("the blinds is open")
                manualSet = "temporary2"
                sampleZClose = "close"
                isBlindOpen = "true"
                data = {
                "manualSet" : manualSet,
                "isBlindOpen" : isBlindOpen,
                "sampleZClose" : sampleZClose
                    }
                db.child("Smart_Blinds").update(data)
                cleanup()
            
    except KeyboardInterrupt:
            cleanup()
            exit( 1 )
#Open if clocks matches opening and blinds is false then open
            
#Close if clocks matches closing and blinds is true then close            
elif mtime == blindClose and isBlindOpen == "true" and sampleZClose == "close":
    step_count = 3300
    isBlindOpen = "false"
    sampleUp = 10000
    manualSet = "temporary"
    sampleZClose = "temporary"
    data = {
    "sampleUp" : sampleUp,
    "manualSet" : manualSet,
    "sampleZClose" : sampleZClose,
    "isBlindOpen" : isBlindOpen
            }
        
    db.child("Smart_Blinds").update(data)
    try:
        i = 0
        for i in range(step_count):
            if i%4==0:
                GPIO.output( out4, GPIO.HIGH )
                GPIO.output( out3, GPIO.LOW )
                GPIO.output( out2, GPIO.LOW )
                GPIO.output( out1, GPIO.LOW )
            elif i%4==1:
                GPIO.output( out4, GPIO.LOW )
                GPIO.output( out3, GPIO.LOW )
                GPIO.output( out2, GPIO.HIGH )
                GPIO.output( out1, GPIO.LOW )
            elif i%4==2:
                GPIO.output( out4, GPIO.LOW )
                GPIO.output( out3, GPIO.HIGH )
                GPIO.output( out2, GPIO.LOW )
                GPIO.output( out1, GPIO.LOW )
            elif i%4==3:
                GPIO.output( out4, GPIO.LOW )
                GPIO.output( out3, GPIO.LOW )
                GPIO.output( out2, GPIO.LOW )
                GPIO.output( out1, GPIO.HIGH )
            time.sleep( step_sleep )
            if i == step_count - 1:
                print("the blinds is close")
                manualSet = "temporary2"
                sampleZClose = "open"
                isBlindOpen = "false"
                data = {
                "manualSet" : manualSet,
                "isBlindOpen" : isBlindOpen,
                "sampleZClose" : sampleZClose
                    }
                db.child("Smart_Blinds").update(data)
                cleanup()
                
    except KeyboardInterrupt:
        cleanup()
        exit( 1 )
#Close if clocks matches closing and blinds is true then close
        
#Open if manual is true        
elif isBlindOpen == "true" and manualSet == "true" and sampleZClose == "open":
    step_count = 3300
    sampleUp = 0
    manualSet = "temporary"
    isBlindOpen ="true"
    sampleZClose ="temporary"
    data = {
    "sampleUp" : sampleUp,
    "sampleZClose" : sampleZClose,
    "isBlindOpen" : isBlindOpen,
    "manualSet" : manualSet
            }
        
    db.child("Smart_Blinds").update(data)
    try:
        i = 0
        for i in range(step_count):
            if i%4==0:
                GPIO.output( out4, GPIO.LOW )
                GPIO.output( out3, GPIO.LOW )
                GPIO.output( out2, GPIO.LOW )
                GPIO.output( out1, GPIO.HIGH )
            elif i%4==1:
                GPIO.output( out4, GPIO.LOW )
                GPIO.output( out3, GPIO.HIGH )
                GPIO.output( out2, GPIO.LOW )
                GPIO.output( out1, GPIO.LOW )
            elif i%4==2:
                GPIO.output( out4, GPIO.LOW )
                GPIO.output( out3, GPIO.LOW )
                GPIO.output( out2, GPIO.HIGH )
                GPIO.output( out1, GPIO.LOW )
            elif i%4==3:
                GPIO.output( out4, GPIO.HIGH )
                GPIO.output( out3, GPIO.LOW )
                GPIO.output( out2, GPIO.LOW )
                GPIO.output( out1, GPIO.LOW )
            time.sleep( step_sleep )
            if i == step_count - 1:
                print("the blinds is open")
                manualSet = "temporary2"
                sampleZClose = "close"
                isBlindOpen = "true"
                data = {
                "manualSet" : manualSet,
                "isBlindOpen" : isBlindOpen,
                "sampleZClose" : sampleZClose
                    }
                db.child("Smart_Blinds").update(data)
                cleanup()
            
            #print("open")
    except KeyboardInterrupt:
        cleanup()
        exit( 1 )
#Open if manual is true
        
#Close if manual is false        
elif isBlindOpen == "false" and manualSet == "false" and sampleZClose == "close":
    step_count = 3300
    manualSet = "temporary"
    sampleUp = 10000
    isBlindOpen ="false"
    sampleZClose ="temporary"
    data = {
    "sampleZClose" : sampleZClose,
    "isBlindOpen" : isBlindOpen,
    "sampleUp" : sampleUp,
    "manualSet" : manualSet
            }
        
    db.child("Smart_Blinds").update(data)
    try:
        i = 0
        for i in range(step_count):
            if i%4==0:
                GPIO.output( out4, GPIO.HIGH )
                GPIO.output( out3, GPIO.LOW )
                GPIO.output( out2, GPIO.LOW )
                GPIO.output( out1, GPIO.LOW )
            elif i%4==1:
                GPIO.output( out4, GPIO.LOW )
                GPIO.output( out3, GPIO.LOW )
                GPIO.output( out2, GPIO.HIGH )
                GPIO.output( out1, GPIO.LOW )
            elif i%4==2:
                GPIO.output( out4, GPIO.LOW )
                GPIO.output( out3, GPIO.HIGH )
                GPIO.output( out2, GPIO.LOW )
                GPIO.output( out1, GPIO.LOW )
            elif i%4==3:
                GPIO.output( out4, GPIO.LOW )
                GPIO.output( out3, GPIO.LOW )
                GPIO.output( out2, GPIO.LOW )
                GPIO.output( out1, GPIO.HIGH )
            time.sleep( step_sleep )
            if i == step_count - 1:
                print("the blinds is close")
                manualSet = "temporary2"
                sampleZClose = "open"
                isBlindOpen = "false"
                data = {
                "sampleZClose" : sampleZClose,
                "manualSet" : manualSet,
                "isBlindOpen" : isBlindOpen
                    }
                db.child("Smart_Blinds").update(data)
                cleanup()
            #print("close")
            
    except KeyboardInterrupt:
        cleanup()
        exit( 1 )
#Close if manual is false
        
#Open slight per click        
elif sampleUp > 0 and sampleUp <= 10000 and blindStop == "true" and manualSet == "temporary2":
    step_count = 660
    manualSet = "temporary"
    sampleZClose ="temporary"
    blindStop = "temporary"
    isBlindOpen ="true"
    sampleUp = sampleUp - 2000
    data = {
    "Blinds_slider" : blindStop,
    "isBlindOpen" : isBlindOpen,
    "sampleZClose" : sampleZClose,
    "manualSet" : manualSet,
    "sampleUp" : sampleUp
            }    
    db.child("Smart_Blinds").update(data)
    try:
        i = 0
        for i in range(step_count):
            if i%4==0:
                GPIO.output( out4, GPIO.LOW )
                GPIO.output( out3, GPIO.LOW )
                GPIO.output( out2, GPIO.LOW )
                GPIO.output( out1, GPIO.HIGH )
            elif i%4==1:
                GPIO.output( out4, GPIO.LOW )
                GPIO.output( out3, GPIO.HIGH )
                GPIO.output( out2, GPIO.LOW )
                GPIO.output( out1, GPIO.LOW )
            elif i%4==2:
                GPIO.output( out4, GPIO.LOW )
                GPIO.output( out3, GPIO.LOW )
                GPIO.output( out2, GPIO.HIGH )
                GPIO.output( out1, GPIO.LOW )
            elif i%4==3:
                GPIO.output( out4, GPIO.HIGH )
                GPIO.output( out3, GPIO.LOW )
                GPIO.output( out2, GPIO.LOW )
                GPIO.output( out1, GPIO.LOW )
            time.sleep( step_sleep )
            if i == step_count - 1:
                manualSet = "temporary2"
                data = {
                "manualSet" : manualSet
                    }
                db.child("Smart_Blinds").update(data)
                print(sampleUp)
                cleanup()
        if sampleUp == 0:
            sampleZClose = "close"
            data = {
            "sampleZClose" : sampleZClose
                    }
            db.child("Smart_Blinds").update(data)
            print("the blinds can now be close")
    except KeyboardInterrupt:
            cleanup()
            exit( 1 )
#Open slight per click
            
#Close slight per click          
elif sampleUp >= 0 and sampleUp < 10000 and blindStop == "false" and manualSet == "temporary2":
    step_count = 660
    manualSet = "temporary"
    isBlindOpen ="false"
    sampleZClose = "temporary"
    blindStop = "temporary"
    sampleUp = sampleUp + 2000
    data = {
    "Blinds_slider" : blindStop,
    "isBlindOpen" : isBlindOpen,
    "manualSet" : manualSet,
    "sampleUp" : sampleUp,
    "sampleZClose" : sampleZClose
            }    
    db.child("Smart_Blinds").update(data)
    try:
        i = 0
        for i in range(step_count):
            if i%4==0:
                GPIO.output( out4, GPIO.HIGH )
                GPIO.output( out3, GPIO.LOW )
                GPIO.output( out2, GPIO.LOW )
                GPIO.output( out1, GPIO.LOW )
            elif i%4==1:
                GPIO.output( out4, GPIO.LOW )
                GPIO.output( out3, GPIO.LOW )
                GPIO.output( out2, GPIO.HIGH )
                GPIO.output( out1, GPIO.LOW )
            elif i%4==2:
                GPIO.output( out4, GPIO.LOW )
                GPIO.output( out3, GPIO.HIGH )
                GPIO.output( out2, GPIO.LOW )
                GPIO.output( out1, GPIO.LOW )
            elif i%4==3:
                GPIO.output( out4, GPIO.LOW )
                GPIO.output( out3, GPIO.LOW )
                GPIO.output( out2, GPIO.LOW )
                GPIO.output( out1, GPIO.HIGH )
            time.sleep( step_sleep )
            if i == step_count - 1:
                print(sampleUp)
                manualSet = "temporary2"
                data = {
                "manualSet" : manualSet
                    }
                db.child("Smart_Blinds").update(data)
                cleanup()
        if sampleUp == 10000:
            sampleZClose = "open"
            data = {
            "sampleZClose" : sampleZClose
                    }
            db.child("Smart_Blinds").update(data)
            print("the blinds can now be open")
    except KeyboardInterrupt:
        cleanup()
        exit( 1 )
#Close slight per click            
#Stepper conditions
