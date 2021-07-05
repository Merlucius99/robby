import RPi.GPIO as GPIO  # import gpio
import time      #import time library
from plot import PLOT
from i2c import I2C
from router import ROUTER



i2c = I2C()
plot = PLOT()
router = ROUTER()

direction = 'f'
values = []
joystickValues = []
sensors = []
offsetHistory = [[],[]]

while(1):
#     print("Move joystick!!")
#     time.sleep(5)
#    manageInput(direction)
#    direction = router.console()
    
    sensors, values, joystickValues = i2c.getValues()
    print(sensors)
    print(values)
    print(joystickValues)

    direction = router.autonomous(values, sensors[2])
    router.manageInput(direction)
    
    
    if(direction == 'f' or direction == 'b'):
        plot.generateXY(values)
    #plot.showGraph()
    time.sleep(1)