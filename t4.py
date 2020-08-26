import os
import glob
import time
import sys
import math
import Adafruit_DHT
import RPi.GPIO as GPIO

from hx711 import HX711

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

GPIO.setmode(GPIO.BCM)
GPIO.setup(16,GPIO.IN)

# Software SPI configuration (for MCP3008):
CLK = 11
MISO = 9
MOSI = 10
CS = 8
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

#DHT Humidity sensor config
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 18

#Water temperature sesor -----------------------START--------------------------
# These tow lines mount the device:
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
# Get all the filenames begin with 28 in the path base_dir.
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_rom():
    name_file = device_folder+'/name'
    f = open(name_file, 'r')
    return f.readline()


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    # Analyze if the last 3 characters are 'YES'.
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    # Find the index of 't=' in a string.
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        # Read the temperature .
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return "Temperature={}C".format(temp_c)
        # return temp_c, temp_f

#Water temperature sesor -----------------------END--------------------------

#DHT Humidity sesor -----------------------START--------------------------
def dht():
    result = 'hello'
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        result = humidity
    return "Humidity={}%".format(humidity)
    # return "Temp={0:0.1f}C Humidity={1:0.1f}%".format(
    #     temperature, humidity)

#DHT Humidity sesor -----------------------END--------------------------

#MCP3008 analog sesor -----------------------START--------------------------
def analog():
    values = [0]*8
    for i in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
        values[i] = mcp.read_adc(i)
    # Print the ADC values.
    nedvesseg = 100-math.floor(mcp.read_adc(0)/10.24)
    teatartaly = math.floor(mcp.read_adc(4)/10.24)
    # return'| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values)
    return'Nedvesseg={}% , Teatartaly={}%'.format(nedvesseg,teatartaly)

#MCP3008 analog sesor -----------------------END--------------------------

#HX711 weight sesor -----------------------START--------------------------
referenceUnit = 1

def cleanAndExit():
    print("Cleaning...")

    GPIO.cleanup()

    print("Bye!")
    sys.exit()

hx = HX711(21, 20)

# I've found out that, for some reason, the order of the bytes is not always the same between versions of python, numpy and the hx711 itself.
# Still need to figure out why does it change.
# If you're experiencing super random values, change these values to MSB or LSB until to get more stable values.
# There is some code below to debug and log the order of the bits and the bytes.
# The first parameter is the order in which the bytes are used to build the "long" value.
# The second paramter is the order of the bits inside each byte.
# According to the HX711 Datasheet, the second parameter is MSB so you shouldn't need to modify it.
hx.set_reading_format("MSB", "MSB")

# HOW TO CALCULATE THE REFFERENCE UNIT
# To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
# In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
# and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
# If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
hx.set_reference_unit(113)
#hx.set_reference_unit(referenceUnit)

hx.reset()

hx.tare()

# print("Tare done! Add weight now...")

# to use both channels, you'll need to tare them both
hx.tare_A()
#hx.tare_B()

#HX711 weight sesor -----------------------END--------------------------

# print(' rom: ' + read_rom())
# print('Reading MCP3008 values, press Ctrl-C to quit...')
# Print nice channel column headers.
# print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8)))
# print('-' * 57)
print('Ready..Open the compocity')

while True:
    try:
        if(GPIO.input(16)):
            print('Welcome')
            print(read_temp())
            # print(' C=%3.3f  F=%3.3f' % read_temp())
            print(dht())
            print(analog())
            val = hx.get_weight(5)
            print('Suly={}g'.format(abs(val)))
            hx.power_down()
            hx.power_up()
            print('Olvasd be a pontokat')
            t=10
            while t:
                print(t)
                t -= 1
                time.sleep(1)
            print()
            print()
            print('Open the Compocity')
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()

