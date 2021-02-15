#NRF Transmitter Side Code (Raspberry Pi):

import RPi.GPIO as GPIO  # import gpio
import time      #import time library
import spidev
from lib_nrf24 import NRF24   #import NRF24 library
from Temperature import *



# 
GPIO.setmode(GPIO.BCM)       # set the gpio mode
#pins for motors
in1 = 26
in2 = 27
in3 = 6
in4 = 5
enA = 18
enB=17
#set gpio mode for pwm motors
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





def nrfsend():
      # set the pipe address. this address shoeld be entered on the receiver alo
    pipes = [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]
    radio = NRF24(GPIO, spidev.SpiDev())   # use the gpio pins
    radio.begin(0, 25)   # start the radio and set the ce,csn pin ce= GPIO08, csn= GPIO25
    radio.setPayloadSize(32)  #set the payload size as 32 bytes
    radio.setChannel(0x76) # set the channel as 76 hex
    radio.setDataRate(NRF24.BR_1MBPS)    # set radio data rate
    radio.setPALevel(NRF24.PA_MIN)  # set PA level

    radio.setAutoAck(True)       # set acknowledgement as true 
    radio.enableDynamicPayloads()
    radio.enableAckPayload()

    radio.openWritingPipe(pipes)     # open the defined pipe for writing

    radio.printDetails()     # print basic detals of radio

    sendMessage = list(temperature())  #the message to be sent


    while True:


        start = time.time()      #start the time for checking delivery time
        radio.write(sendMessage)   # just write the message to radio 
        print("Sent the message: {}".format(sendMessage))  # print a message after succesfull send

        time.sleep(3)  # give delay of 3 seconds
        
    return

def nrfrecieve():
    
    
         # set the pipe address. this address shoeld be entered on the receiver alo
    pipes = [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]
    radio = NRF24(GPIO, spidev.SpiDev())   # use the gpio pins
    radio.begin(0, 25)   # start the radio and set the ce,csn pin ce= GPIO08, csn= GPIO25
    radio.setPayloadSize(32)  #set the payload size as 32 bytes
    radio.setChannel(0x76) # set the channel as 76 hex
    radio.setDataRate(NRF24.BR_1MBPS)    # set radio data rate
    radio.setRetries(15, 15)
    radio.setPALevel(NRF24.PA_MAX)  # set PA level

    radio.setAutoAck(True)       # set acknowledgement as true 
    radio.enableDynamicPayloads()

    radio.openReadingPipe(0, pipes)     # open the defined pipe for writing
    radio.printDetails()     # print basic detals of radio


    z = 1
    while(1):
        radio.startListening()
        while not radio.available(0):
            print("Radio unavailable...")
            time.sleep(1 / 100)
        receivedMessage = []
        size = radio.getDynamicPayloadSize()
        if size>0:
            print("Dynamic Payload Size: ", size)
            radio.read(receivedMessage, size)
            print("Received: ", receivedMessage)
            print("Translating...")
            string = []
            n = 0
            while n<len(receivedMessage):
                if receivedMessage[n] >= 33:
                    string.append(chr(receivedMessage[n]))
                n = n+1
            print("Message: ", string)
        else:
            print("No Payload ", z)
        time.sleep(0.7)
        z = z+1
#------------------------------------------------------------------------------------------    
#JOYSTICK RECIEVE
            
        j=0
        global x_axis,y_axis,sw # x(joyx), y(joyx) and sw(switch joystick) global variables
        x_axis,y_axis,sw=' ',' ',' '
        for i in range(0,len(receivedMessage)):
            if receivedMessage[i]!=46:
                if j==0:
                    x_axis=x_axis+chr(receivedMessage[i])
                if j==1:
                    y_axis=y_axis+chr(receivedMessage[i])
                if j==2:
                    sw=sw+chr(receivedMessage[i])
                    j=j+1
                    break
                
            else:
                j=j+1
        
        print(x_axis, y_axis,sw)
#-------------------------------------------------------------------------------------            
#end of joystick recieve
             
# 
# #-----------------------------------------------------------------------------------------
# #MOTOR PWM START
        p.start(25)
        p2.start(25)
          

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
           
         
        def speed(duty):
            #print("speed: %d"%duty)
            p.ChangeDutyCycle(duty)
            p2.ChangeDutyCycle(duty)
            return
        


        def set_speed(y_axis):
            if int(y_axis) >= 430 and int(y_axis)<480:
                speed(10)
            elif int(y_axis) >= 500 and int(y_axis)<550:
                speed(20)
            elif int(y_axis) >= 550 and int(y_axis) < 600:
                speed(45)
        
            elif int(y_axis) >= 600 and int(y_axis) <700:
                speed(70)
         
            elif int(y_axis)>700 :
                speed(100)
                
                
            elif int(y_axis) >= 400 and int(y_axis) <450:
                stop()
            elif int(y_axis) >= 300 and int(y_axis) <400:
                speed(10)
            elif int(y_axis) >= 200 and int(y_axis) <300:
                speed(30)
            elif int(y_axis) >= 100 and int(y_axis) <200:
                speed(60)
        
            elif int(y_axis) <100:
                speed(90)
            return

        def set_direction(x_axis):
            if(int(y_axis)>500):
                if int(x_axis)<400:
                    move_left()
                elif int(x_axis) >= 500:
                    move_right()
                elif int(x_axis) > 400 and  int(x_axis) < 500 and int(y_axis)>500 :
                    move_forward()
            else:
                if int(x_axis)<400:
                    move_leftback()
                elif int(x_axis) >= 500:
                    move_rightback()
                elif int(x_axis) > 400 and  int(x_axis) < 500 and int(y_axis)<300:
                    move_backward()
            
            return

        
                
        
        
        set_direction(x_axis)        
        set_speed(y_axis)

#      end of pwm motor control speed       
            
#-----------------------------------------------------------------------------------------------------            
            
           
        
        
    return

def ultrasonic():
        #set GPIO Pins
    GPIO_TRIGGER = 20
    GPIO_ECHO = 21
    servo_pin = 16
    duty_cycle = 1   # Should be the centre for a SG90
     
    #set GPIO direction (IN / OUT) for ultrasonic
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    # Configure the Pi to use pin names (i.e. BCM) and allocate I/O for microservo
    GPIO.setup(servo_pin, GPIO.OUT)

    # Create PWM channel on the servo pin with a frequency of 50Hz
    pwm_servo = GPIO.PWM(servo_pin, 50)
    pwm_servo.start(duty_cycle)
 
     
    def distance():
        # set Trigger to HIGH
        GPIO.output(GPIO_TRIGGER, True)
     
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
     
        StartTime = time.time()
        StopTime = time.time()
     
        # save StartTime
        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()
     
        # save time of arrival
        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()
     
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
     
        return distance
    
    
    try:
        
        for duty_cycle in range(1,13,1):
            e=0 #contor
            while(e==0):                 
                dist1 = distance()
                time.sleep(1/100)
                dist2 = distance()
                time.sleep(1/100)
                dist3 = distance()
                if(abs(dist1-dist2)<1 and abs(dist2-dist3)<1):
                    e=1 #while exit
                    print ("Distance = %.1f cm in position %d" % (dist1,duty_cycle))
                    pwm_servo.ChangeDutyCycle(duty_cycle)
                else:
                    print (dist2-dist1)
                    
                time.sleep(0.7)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
    finally:
        GPIO.cleanup()   
    return

    

#nrfsend()
#nrfrecieve()

ultrasonic()
#nrfrecieve()

