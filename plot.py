import numpy as np
import matplotlib.pyplot as plt
import math
from mapping import MAPPING

class PLOT:
    color = ['ro','go','bo','yo','mo','co','ko']
    angle = [3, 18, 36, 56, 74, 91, 101, 115, 128, 141, 156]
    mapping = MAPPING()
    x,y = [],[]
    x_off,y_off = [],[]

    def reset(self):
        PLOT.x,self.y = [],[]
        PLOT.x_off,PLOT.y_off = [0],[0]

    def generateXY(self, value):
        PLOT.x_offset, PLOT.y_offset, PLOT.angle_offset = PLOT.mapping.getOffset()
        print(PLOT.x_offset, PLOT.y_offset, PLOT.angle_offset)
        for i in range(11):
            if(value[i]>=80): continue
            cx = value[i]*math.cos((PLOT.angle[i]+PLOT.angle_offset)*math.pi/180)+PLOT.x_offset
            cy = value[i]*math.sin((PLOT.angle[i]+PLOT.angle_offset)*math.pi/180)+PLOT.y_offset
            PLOT.x.append(cx)  #x coordinate measured
            PLOT.y.append(cy)  #y coordinate measured
        PLOT.x_off.append(PLOT.x_offset)
        PLOT.y_off.append(PLOT.y_offset)
        return
        
    def showGraph(self):
        print(PLOT.x_off,PLOT.y_off)
        plt.plot(0,0,'rx',PLOT.x,PLOT.y,'bo',PLOT.x_off,PLOT.y_off,'r--',PLOT.x_off[-1],PLOT.y_off[-1],'rs')
        plt.show()
        return
    
    def getOffset(self):
        return self.x_off,self.y_off
