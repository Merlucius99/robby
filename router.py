from smbus import SMBus
import time
import RPi.GPIO as GPIO 
import math
from motorDriver import MOTOR
from joystick import JOYSTICK
from mapping import MAPPING
from plot import PLOT

plot = PLOT()
mapping = MAPPING()
joystick = JOYSTICK()
motor = MOTOR()
motor.setSpeed(50)

class ROUTER:
    firePin = 22
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(ROUTER.firePin,GPIO.OUT)
        GPIO.output(ROUTER.firePin,GPIO.LOW)
    def joystick(self,joystickValues):
        direction = joystick.getDirection(joystickValues)
        self.manageInput(direction)
        return direction
        
    def console(self):
        direction = input()
        self.manageInput(direction)
        return direction
        
    def manageInput(self, x):
        if x=='s':
            motor.stop()
            x='z'

        elif x=='f':
            motor.moveForward()
            mapping.update(x)
            x='z'

        elif x=='b':
            motor.moveBackwards()
            mapping.update(x)
            x='z'
        
        elif x=='r':
            motor.moveRight()
            mapping.update(x)
            x='z'
        
        elif x=='l':
            motor.moveLeft()
            mapping.update(x)
            x='z'
        
        elif x=='m':
            mapping.update(x)
            x='z'
        
        elif x=='p':
            plot.showGraph()
            x='z'
            
        elif x=='e':
            GPIO.cleanup()
            print("GPIO Clean up")
        
        else:
            print("<<<  wrong data  >>>")
            print("please enter the defined data to continue.....")
            
    angle = [3, 18, 36, 56, 74, 91, 101, 115, 128, 141, 156]
    last_wall = ''
    def autonomous(self, distance, fire):

        if(fire == 111):
            print("Fire!!!!")
            print("Fire ON")
            GPIO.output(ROUTER.firePin,GPIO.HIGH)
            time.sleep(2)
            print("Fire OFF")
            GPIO.output(ROUTER.firePin,GPIO.LOW)
            return 's'
        if(fire == 1 or fire == 11):
            print("Fire RIGHT")
            return 'r'
        if(fire == 100 or fire == 110):
            print("Fire LEFT")
            return 'l'
        if(fire == 10):
            print("Fire FRONT")
            return 'f'
        
        history = mapping.getHistory()
        x = []
        y = []
        left = 100
        front = 100
        right = 100
        
        length_front = 3
        length_left = 4
        length_right = 4
        
        for i in range(11):          
            if distance[i] == 100:
                x.append(100)
                y.append(100)
            else:
                x.append(distance[i]*math.cos(ROUTER.angle[i]*math.pi/180))
                y.append(distance[i]*math.sin(ROUTER.angle[i]*math.pi/180))
                
        if not length_front == 0:    
            front = (abs(y[4])+abs(y[5])+abs(y[6]))/length_front
        if not length_right == 0:  
            right = (abs(x[0])+abs(x[1])+abs(x[2])+abs(x[3]))/length_right
            if right <= 40:
                ROUTER.last_wall = 'r'
        if not length_left == 0:  
            left = (abs(x[10])+abs(x[9])+abs(x[8])+abs(x[7]))/length_left
            if left <= 40:
                ROUTER.last_wall = 'l'
        print(left,front,right)
        if front >= 40:
            if ROUTER.last_wall == 'r' and right >= 90:
                return 'r'
            if ROUTER.last_wall == 'l' and left >= 90:
                return 'l'
            return 'f'
        
        if left >= 40:
            return 'l'
            
        if right >= 40:
            return 'r'
        return 'b'
