from gpiozero import Robot, MotionSensor
from time import sleep
import RPi.GPIO as GPIO

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(25,GPIO.OUT)
#GPIO.setup(1,GPIO.OUT)




robot = Robot(left=(27,26), right=(5,6))
robot.forward()
sleep(5)
# p1=GPIO.PWM(25,100)
# #p2=GPIO.PWM(1,100)
# 
# while True:
#     p1.start(20) #Motor will run at slow speed
#     robot.forward()
#     GPIO.output(25,True)
#     #GPIO.output(1,True)
#     sleep(3)
#     p1.ChangeDutyCycle(100) #Motor will run at High speed
#     #p2.ChangeDutyCycle(100) #Motor will run at High speed
#     
#     robot.forward()
#     GPIO.output(25,True)
#     #GPIO.output(1,True)
#     sleep(3)
#     GPIO.output(25,False)
#     #GPIO.output(1,False)
#     p1.stop()
#     #p2.stop()
robot.stop()

