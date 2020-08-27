import os
import glob
import time
import sys
import math
import Adafruit_DHT
import RPi.GPIO as GPIO

import OLED_Driver as OLED
from PIL  import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor

from hx711 import HX711

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

GPIO.setmode(GPIO.BCM)
GPIO.setup(16,GPIO.IN)

# Software SPI configuration (for MCP3008):
CLK = 22
MISO = 27
MOSI = 17
CS = 23
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

def cleanAndExit():
    print("Cleaning...")

    OLED.Clear_Screen()
    GPIO.cleanup()

    print("Bye!")
    sys.exit()

def loading_text():
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('cambriab.ttf',24)

    draw.text((20, 52), 'Töltés..', fill = "CYAN", font = font)
    OLED.Display_Image(image)

print('Loading...')

try:
    OLED.Device_Init()
    loading_text()   
except:
    cleanAndExit()

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
        return temp_c
        # return "Temperature={}C".format(temp_c)
        # return temp_c, temp_f

#Water temperature sesor -----------------------END--------------------------

#DHT Humidity sesor -----------------------START--------------------------
def dht():
    result = 'hello'
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        result = humidity
    return humidity
    # return "Humidity={}%".format(humidity)
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
    # return'Nedvesseg={}% , Teatartaly={}%'.format(nedvesseg,teatartaly)
    return [nedvesseg, teatartaly]

#MCP3008 analog sesor -----------------------END--------------------------

#HX711 weight sesor -----------------------START--------------------------
referenceUnit = 1

hx = HX711(21, 20)
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

def Test_Text():
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('cambriab.ttf',24)

    draw.text((0, 12), 'Compocity', fill = "BLUE", font = font)
    draw.text((0, 36), 'Ready', fill = "BLUE",font = font)
    draw.text((20, 72), '1.5 inch', fill = "CYAN", font = font)
    draw.text((10, 96), 'R', fill = "RED", font = font)
    draw.text((25, 96), 'G', fill = "GREEN", font = font)
    draw.text((40, 96), 'B', fill = "BLUE", font = font)
    draw.text((55, 96), ' OLED', fill = "CYAN", font = font)

    OLED.Display_Image(image)

def ready_text():
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('cambriab.ttf',24)

    draw.text((0, 40), 'Compocity', fill = "CYAN", font = font)
    draw.text((0, 64), 'Ready!', fill = "CYAN", font = font)
    OLED.Display_Image(image)
    OLED.Delay(2000)
    img = Image.open("logo.png")
    OLED.Display_Image(img)
    # OLED.Clear_Screen()

def timer_text(time):
    # image = Image.open("picture1.jpg")
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('cambriab.ttf',12)

    draw.text((0, 30), 'Olvasd be a QR kodot!', fill = "CYAN", font = font)
    draw.text((0, 50), 'Hatralevo ido: {}'.format(time), fill = "CYAN", font = font)
    OLED.Display_Image(image)

def sensor_text(temperature, humidity, nedvesseg, teatartaly, suly):
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('cambriab.ttf',12)

    draw.text((0, 0), temperature, fill = "CYAN", font = font)
    draw.text((0, 12), humidity, fill = "CYAN", font = font)
    draw.text((0, 24), nedvesseg, fill = "CYAN", font = font)
    draw.text((0, 36), teatartaly, fill = "CYAN", font = font)
    draw.text((0, 48), suly, fill = "CYAN", font = font)
    OLED.Display_Image(image)
    OLED.Delay(6000)
    OLED.Clear_Screen()

print('Ready..Open the compocity')

try:
    # OLED.Device_Init()
    ready_text()
    while True:
        #-------------OLED Init------------#
        if(GPIO.input(16)):
            # OLED.Device_Init()
            # Test_Text()
            print('Welcome')

            temp_data = read_temp()
            print("Temperature={}C".format(temp_data))

            humidity_data = dht()
            print("Humidity={}%".format(humidity_data))

            analog_data = analog()
            
            print('Nedvesseg={}% , Teatartaly={}%'.format(analog_data[0],analog_data[1]))

            val = math.ceil(hx.get_weight(5))
            print('Suly={}g'.format(abs(val)))
            hx.power_down()
            hx.power_up()

            sensor_text("Temperature={}C".format(temp_data),"Humidity={}%".format(humidity_data),"Nedvesseg={}%".format(analog_data[0]),"Teatartaly={}%".format(analog_data[1]),'Suly={}g'.format(abs(val)))

            print('Olvasd be a pontokat')
            t=10
            while t:
                print(t)
                timer_text(t)
                t -= 1
                time.sleep(1)
            print()
            print()
            print('Open the Compocity')
            OLED.Clear_Screen()
except (KeyboardInterrupt, SystemExit):
    cleanAndExit()


