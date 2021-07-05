# Python Script
# https://www.electronicshub.org/raspberry-pi-l298n-interface-tutorial-control-dc-motor-l298n-raspberry-pi/

import RPi.GPIO as GPIO          
from time import sleep

class MOTOR:
    in1 = 26
    in2 = 27
    in3 = 6
    in4 = 5
    enA = 18
    enB = 17
    motionTime = 0.4 #30cm - 0.75 10cm - 0.3
    rotationTime = 0.7

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(MOTOR.in1,GPIO.OUT)
        GPIO.setup(MOTOR.in2,GPIO.OUT)
        GPIO.setup(MOTOR.in3,GPIO.OUT)
        GPIO.setup(MOTOR.in4,GPIO.OUT)
        GPIO.setup(MOTOR.enA,GPIO.OUT)
        GPIO.setup(MOTOR.enB,GPIO.OUT)
        GPIO.output(MOTOR.in1,GPIO.LOW)
        GPIO.output(MOTOR.in2,GPIO.LOW)
        GPIO.output(MOTOR.in3,GPIO.LOW)
        GPIO.output(MOTOR.in4,GPIO.LOW)
        self.p=GPIO.PWM(MOTOR.enA,1000)
        self.p2=GPIO.PWM(MOTOR.enB,1000)
        self.p.start(25)
        self.p2.start(25)
        
    def moveForward(self):
        self.forward()
        sleep(MOTOR.motionTime)
        self.stop()
        
    def moveBackwards(self):
        self.backwards()
        sleep(MOTOR.motionTime)
        self.stop()
        
    def moveRight(self):
        self.right()
        sleep(MOTOR.rotationTime)
        self.stop()
        
    def moveLeft(self):
        self.left()
        sleep(MOTOR.rotationTime)
        self.stop()

    def stop(self):
        print("stop")
        GPIO.output(MOTOR.in1,GPIO.LOW)
        GPIO.output(MOTOR.in2,GPIO.LOW)
        GPIO.output(MOTOR.in3,GPIO.LOW)
        GPIO.output(MOTOR.in4,GPIO.LOW)    

    def forward(self):
        print("forward")
        GPIO.output(MOTOR.in1,GPIO.HIGH)
        GPIO.output(MOTOR.in2,GPIO.LOW)
        GPIO.output(MOTOR.in3,GPIO.HIGH)
        GPIO.output(MOTOR.in4,GPIO.LOW)
        
    def backwards(self):
        print("backwards")
        GPIO.output(MOTOR.in1,GPIO.LOW)
        GPIO.output(MOTOR.in2,GPIO.HIGH)
        GPIO.output(MOTOR.in3,GPIO.LOW)
        GPIO.output(MOTOR.in4,GPIO.HIGH)
        
    def right(self):
        print("right")
        GPIO.output(MOTOR.in1,GPIO.HIGH)
        GPIO.output(MOTOR.in2,GPIO.LOW)
        GPIO.output(MOTOR.in3,GPIO.LOW)
        GPIO.output(MOTOR.in4,GPIO.HIGH)
        
    def left(self):
        print("left")
        GPIO.output(MOTOR.in1,GPIO.LOW)
        GPIO.output(MOTOR.in2,GPIO.HIGH)
        GPIO.output(MOTOR.in3,GPIO.HIGH)
        GPIO.output(MOTOR.in4,GPIO.LOW)
        
    def rightBackwards(self):
        print("right-backward")
        GPIO.output(MOTOR.in1,GPIO.LOW)
        GPIO.output(MOTOR.in2,GPIO.HIGH)
        GPIO.output(MOTOR.in3,GPIO.LOW)
        GPIO.output(MOTOR.in4,GPIO.LOW)
        
    def leftBackwards(self):
        print("left-backward")
        GPIO.output(MOTOR.in1,GPIO.LOW)
        GPIO.output(MOTOR.in2,GPIO.LOW)
        GPIO.output(MOTOR.in3,GPIO.LOW)
        GPIO.output(MOTOR.in4,GPIO.HIGH)
        
    def setSpeed(self, speed):
        print("speed set to: ", speed)
        self.p.ChangeDutyCycle(speed)
        self.p2.ChangeDutyCycle(speed)
