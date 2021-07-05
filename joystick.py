from smbus import SMBus
import time

class JOYSTICK:
    
    def getDirection(self, values):
        x = values[0]
        y = values[1]
        print(x,y)
        if(x>=50 and x<=150):
            if(y>=0 and y<=50):
                return "f"
            if(y>=150 and y<=204):
                return "b"
        if(y>=50 and y<=150):
            if(x>=0 and x<=50):
                return "l"
            if(x>=150 and x<=204):
                return "r"
        return "m"