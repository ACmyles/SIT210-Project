import RPi.GPIO as GPIO
import time
import requests
import os
import sys
from datetime import datetime

fw = open("log.txt","a")

solenoid_1 = 3
solenoid_2 = 5

GPIO.setmode(GPIO.BOARD)
GPIO.setup(solenoid_1, GPIO.OUT)
GPIO.setup(solenoid_2, GPIO.OUT)

def menu():
    os.system("clear")
    print("--------------Garden Watering System--------------\n")

    choice = input("""
A: Start Automatic Watering
B: Turn On
C: Turn Off
D: Print Log
Q: Quit

Choose option: """)

    if choice.lower() == "a":
        loop()
    elif choice.lower() == "b":
        water_on()
    elif choice.lower() == "c":
        water_off()
    elif choice.lower() =="d":
        print(1)
    elif choice.lower() =="q":
        GPIO.cleanup()
        fw.close()
        sys.exit()
    else:
        print("Invalid character. Please enter a valid selection.")
        menu()

def get_soil_moisture(channel):
    access_token = os.getenv('ACCESS_TOKEN')
    x = requests.get(f"https://api.particle.io/v1/devices/e00fce68ecb0a7597d865534/{channel}?access_token={access_token}")
    x = x.json()
    return x['result']

def water_on():
    channel = int(input("Enter channel (1 or 2)"))
    if (channel == 1):
        GPIO.output(solenoid_1, GPIO.HIGH)
    elif (channel == 2):
        GPIO.output(solenoid_2, GPIO.HIGH)
    menu()
    
def water_off():
    channel = int(input("Enter channel (1 or 2)"))
    if (channel == 1):
        GPIO.output(solenoid_1, GPIO.LOW)
    elif (channel == 2):
        GPIO.output(solenoid_2, GPIO.LOW)
    menu()

# def get_rain():

def loop():
    try:
        while True:
            soil_moisture_1 = get_soil_moisture("soilSensor")
            soil_moisture_2 = get_soil_moisture("soilSensor2")

            if soil_moisture_1 < 2000:
                print(f"{datetime.now()} - soil moisture low ({soil_moisture_1}) on sensor 1, watering for 60 seconds.")
                fw.write(f"{datetime.now()} - soil moisture low ({soil_moisture_1}) on sensor 1, watering for 60 seconds.\n")
                GPIO.output(solenoid_1, GPIO.HIGH)
            else:
                print(f"{datetime.now()} - soil moisture adequate ({soil_moisture_1}) on sensor 1.")
                fw.write(f"{datetime.now()} - soil moisture adequate ({soil_moisture_1}) on sensor 1.\n")

            if soil_moisture_2 < 2000:
                print(f"{datetime.now()} - soil moisture low ({soil_moisture_2}) on sensor 2, watering for 60 seconds.")
                fw.write(f"{datetime.now()} - soil moisture low ({soil_moisture_2}) on sensor 2, watering for 60 seconds.\n")
                GPIO.output(solenoid_2, GPIO.HIGH)
            else:
                print(f"{datetime.now()} - soil moisture adequate ({soil_moisture_2}) on sensor 2.")
                fw.write(f"{datetime.now()} - soil moisture adequate ({soil_moisture_2}) on sensor 2.\n")

            time.sleep(60)
            GPIO.output(solenoid_1, GPIO.LOW)
            GPIO.output(solenoid_2, GPIO.LOW)
    except KeyboardInterrupt:
        menu()

menu()