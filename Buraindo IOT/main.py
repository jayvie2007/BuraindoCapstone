import subprocess
import time

#The starter script
time.sleep(5)
subprocess.Popen(["python", 'thclockDisplay.py'])
time.sleep(2)
print("thclockDisplay is up")
subprocess.Popen(["python", 'relayHumidity.py'])
time.sleep(2)
print("relay is up")
subprocess.Popen(['sudo','python3' ,'ledControl.py'])
time.sleep(2)
print("led is up")

while True:
    subprocess.Popen(["python", 'blindsControl.py'])
    time.sleep(3)
#The starter script    