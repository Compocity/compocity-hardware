import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(16,GPIO.IN)    ## 37-es tüske beállítása bemenetnek
input = GPIO.input(16)    ## a 37-es tüske értékének betöltése az input nevű változásba
while True:               ## ciklus indítása
  print(GPIO.input(16))
  time.sleep(2)

