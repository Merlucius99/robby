import RPi.GPIO as GPIO  # import gpio
import time      #import time library
import spidev
from lib_nrf24 import NRF24   #import NRF24 library

def florin(string):
    z = 1
    radio.startListening()
    while not radio.available(0):
        time.sleep(1 / 100)
    receivedMessage = []
    size = radio.getDynamicPayloadSize()
    if size>0:
        print("Dynamic Payload Size: ", size)
        radio.read(receivedMessage, size)
        print("Received: ", receivedMessage)
        print("Translating...")
        n = 0
        while n<len(receivedMessage):
            if receivedMessage[n] >= 33:
                string=string+chr(receivedMessage[n])
            n = n+1
        print("Message: ", string)
    else:
        print("No Payload ", z)
    time.sleep(0.9)
    z = z+1
    
    radio.stopListening()
    return

# 
GPIO.setmode(GPIO.BCM)       # set the gpio mode

  # set the pipe address. this address shoeld be entered on the receiver alo
pipes = [[0xE0, 0xE0, 0xF1, 0xF1, 0xE0], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]
radio = NRF24(GPIO, spidev.SpiDev())   # use the gpio pins
#time.sleep(0.5)
radio.begin(0, 25)   # start the radio and set the ce,csn pin ce= GPIO08, csn= GPIO25
radio.setPayloadSize(32)  #set the payload size as 32 bytes
radio.setChannel(0x76) # set the channel as 76 hex
radio.setDataRate(NRF24.BR_1MBPS)    # set radio data rate
radio.setRetries(15, 15)
radio.setPALevel(NRF24.PA_MAX)  # set PA level

radio.setAutoAck(True)       # set acknowledgement as true 
radio.enableDynamicPayloads()

radio.openReadingPipe(0, pipes[1])     # open the defined pipe for writing
#radio.printDetails()     # print basic detals of radio

sf = 'lalala'
florin(sf)
print(sf)
    



