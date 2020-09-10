import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN)

try:
    while True:
        if((not GPIO.input(16))):
            print('csukd le a compocityt')
            while not GPIO.input(16):
                time.sleep(500)
                print(GPIO.input(16))
            print('scanneld be a pontokat')

except:
    print('hiba')

