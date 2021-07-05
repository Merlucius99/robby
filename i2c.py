from smbus import SMBus
import time

class I2C:
    address = 0x08 # bus address
    bus = SMBus(1) # indicates /dev/ic2-1 
        
    def getValues(self):
        sensors = []
        values = []
        joystick = []
        for i in range(3):
            sensors.append(I2C.bus.read_byte(I2C.address))
        for i in range(11):
            values.append(I2C.bus.read_byte(I2C.address))
        for i in range(3):
            joystick.append(I2C.bus.read_byte(I2C.address))
        return sensors, values, joystick
