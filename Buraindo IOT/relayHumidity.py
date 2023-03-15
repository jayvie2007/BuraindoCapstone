import RPi.GPIO as GPIO
import board
import time
import pyrebase


#RELAY
relay = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay, GPIO.OUT)
GPIO.output( relay, GPIO.LOW )
#RELAY

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

while True:
#Calling value from firebase    
    BlindsOpen = db.child("Smart_Blinds").get("")
    tempvalue = BlindsOpen.val()
    value = [tempvalue[j] for j in tempvalue]
    time.sleep(1)
    humidGet = value[8]
    humidManual = value[17]       
    humidAuto = value[18]
#Calling value from firebase
    
#Relay conditions
#if the humidity is less than 30% and auto is true then open    
    if humidGet <=30 and humidAuto == "true":
        GPIO.output(relay, True)
    elif humidGet >= 45 and humidAuto == "true":
        GPIO.output(relay, False)
#if the humidity is less than 30% and auto is true then open  
        
#if the humidity manual is true and auto is false then open            
    elif humidManual == "true" and humidAuto =="false":
        GPIO.output(relay, True)
#if the humidity manual is true and auto is false then open
        
#if the humidity manual is false then close        
    elif humidManual == "false" and humidAuto =="false":
        GPIO.output(relay, False)
#if the humidity manual is false then close  
#Relay conditions