#!/usr/bin/python
import sys
import Adafruit_DHT
humiditys, temperatures = Adafruit_DHT.read_retry(11, 23)
def temperature():
   

    return ('Temp: {0:0.1f}C Humidity: {1:0.1f}'.format(temperatures, humiditys))

    
   