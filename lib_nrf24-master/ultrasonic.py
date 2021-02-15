#Libraries
import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

def Ultrasonic():
        #set GPIO Pins
    GPIO_TRIGGER = 20
    GPIO_ECHO = 21
    servo_pin = 16
    duty_cycle = 7.5    # Should be the centre for a SG90
     
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
     
    if __name__ == '__main__':
        try:
            while True:
                for duty_cycle in range(1,13,1):
                    pwm_servo.ChangeDutyCycle(duty_cycle)
                    time.sleep(3)
                    dist = distance()
                    print ("Measured Distance = %.1f cm" % dist)
                    time.sleep(3)
     
            # Reset by pressing CTRL + C
        except KeyboardInterrupt:
            print("Measurement stopped by User")
        finally:
            GPIO.cleanup()   
    
    return