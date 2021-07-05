class MAPPING:
    step = 20

    x_offset, y_offset, angle_offset, direction = 0,0,0,''
    mapHistory = []

    def getOffset(self):
        return MAPPING.x_offset, MAPPING.y_offset, MAPPING.angle_offset
    
    def getHistory(self):
        return MAPPING.mapHistory
    
    def update(self,d):
        MAPPING.direction = d
        MAPPING.mapHistory.append(MAPPING.direction)        
                    
        if MAPPING.direction == 'l': #Left
            MAPPING.angle_offset += 90
            
        if MAPPING.direction == 'r': #Right
            MAPPING.angle_offset -= 90
        
        if (MAPPING.angle_offset >= 360):
            MAPPING.angle_offset = MAPPING.angle_offset - 360
        if (MAPPING.angle_offset <= -360):
            MAPPING.angle_offset = MAPPING.angle_offset + 360
            
        if MAPPING.direction == 'f': #Forward
            if (MAPPING.angle_offset == 0): MAPPING.y_offset += MAPPING.step
            elif MAPPING.angle_offset == 90 or MAPPING.angle_offset == -270: MAPPING.x_offset -= MAPPING.step
            elif MAPPING.angle_offset == 180 or MAPPING.angle_offset == -180: MAPPING.y_offset -= MAPPING.step
            elif MAPPING.angle_offset == 270 or MAPPING.angle_offset == -90: MAPPING.x_offset += MAPPING.step
            
        if MAPPING.direction == 'b': #Backwards
            if (MAPPING.angle_offset == 0): MAPPING.y_offset -= MAPPING.step
            elif MAPPING.angle_offset == 90 or MAPPING.angle_offset == -270: MAPPING.x_offset += MAPPING.step
            elif MAPPING.angle_offset == 180 or MAPPING.angle_offset == -180: MAPPING.y_offset += MAPPING.step
            elif MAPPING.angle_offset == 270 or MAPPING.angle_offset == -90: MAPPING.x_offset -= MAPPING.step
