import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(19, GPIO.IN)

try:
    while True:
        if((not GPIO.input(19))):
            print('csukd le a compocityt')
            while (not GPIO.input(19)):
                time.sleep(1)
                print(GPIO.input(19))
            print('scanneld be a pontokat')

except:
    print('hiba')

