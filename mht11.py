import Adafruit_DHT
 
# Érzékelő típusának beállítása : DHT11,DHT22 vagy AM2302
sensor=Adafruit_DHT.DHT11
 
# A szenzorunk a következő GPIO-ra van kötve:
gpio=17
 
# A read_retry eljárást használjuk. Ez akár 15x is megpróbálja kiolvasni az érzékelőből az adatot (és minden olvasás előtt 2 másodpercet vár).
humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
 
# A DHT11 kiolvasása nagyon érzékeny az időzítésre és a Pi alkalmanként
# nem tud helyes értéket kiolvasni. Ezért megnézzük, hogy helyesek-e a kiolvasott értékek.
if humidity is not None and temperature is not None:
print('Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature, humidity))
else:
print('Sikertelen olvasas! Ujra probalkozunk')
