# Python Script
# https://www.electronicshub.org/raspberry-pi-l298n-interface-tutorial-control-dc-motor-l298n-raspberry-pi/

import RPi.GPIO as GPIO          
from time import sleep
#from joystick_recive import *

x,y,z=0,0,0
#joystick();
print(x,y,z)
print("test")

in1 = 26
in2 = 27
in3 = 6
in4 = 5
enA = 18
enB=17


GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(enA,GPIO.OUT)
GPIO.setup(enB,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
p=GPIO.PWM(enA,1000)
p2=GPIO.PWM(enB,1000)

p.start(25)
p2.start(25)
print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("s-stop f-forward b-backward ri-right le-left rb-righbackward lb-leftbackward l-low m-medium h-high e-exit")
print("\n")    

def move_forward():
    print("forward")
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
    return 

def move_backward():
    print("backward")
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)
    return

def move_right():
    print("right")
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
    return

def move_left():
    print("left")
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
    return

def stop():
    print("stop")
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
    return
     
def move_rightback():
    print("right-backward")
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
    return
    
def move_leftback():
    print("left-backward")
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)
    return
   
 
def low():
    print("low")
    p.ChangeDutyCycle(40)
    p2.ChangeDutyCycle(40)
    return
    

def medium():
    print("medium")
    p.ChangeDutyCycle(70)
    p2.ChangeDutyCycle(70)
    return

def high():
    print("high")
    p.ChangeDutyCycle(100)
    p2.ChangeDutyCycle(100)
    return


def set_speed(y_axis):
    if y_axis >= 500 and y_axis<600:
        low()
    elif y_axis >= 600 and y_axis < 750:
        medium()
    elif y_axis >= 750 and y_axis <900:
        high()
    elif y_axis<500 :
        stop()
    return

def set_direction(x_axis):
    if x_axis >= 500 and x_axis<600:
        low()
    elif x_axis >= 600 and x_axis < 750:
        medium()
    elif x_axis >= 750 and x_axis <900:
        high()
    elif x_axis <500 :
        stop()
    
    return

while True:
    i=0
    
    for i in range(450,900,10):
        
        #move_forward()
        sleep(2)
        x_axis=i
        y_axis=i
        set_speed(y_axis)
        set_direction(x_axis)
        
    
        
