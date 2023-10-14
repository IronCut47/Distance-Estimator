import RPi.GPIO as GPIO          
from time import sleep

run_time = 3

in1 = 23
in2 = 24
en1 = 25

in3 = 27
in4 = 22
en2 = 4

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en1,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p1 = GPIO.PWM(en1,1000)

GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
p2 = GPIO.PWM(en2,1000)

p1.start(0)
p2.start(0)

def run_left_motor():
    print("Running left motor for 3 seconds.")
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    p1.ChangeDutyCycle(75)
    sleep(run_time)
    GPIO.output(in1, GPIO.LOW)
    p1.ChangeDutyCycle(0)


def run_right_motor():
    print("Running right motor for 3 seconds.")
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    p2.ChangeDutyCycle(75)
    sleep(run_time)
    GPIO.output(in3, GPIO.LOW)
    p2.ChangeDutyCycle(0)


def run_both_motors():
    print("Running both motors for 3 seconds.")
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    p1.ChangeDutyCycle(75)
    p2.ChangeDutyCycle(75)
    sleep(run_time)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)
    

# while(1):

#     x = input()
    
#     if x == 'L':
#         print("Running first motor")
#         GPIO.output(in1,GPIO.HIGH)
#         GPIO.output(in2,GPIO.LOW)
#         p1.ChangeDutyCycle(75)
#         x = 'z'

#     elif x == 'R':
#         print("Running second motor")
#         GPIO.output(in3,GPIO.HIGH)
#         GPIO.output(in4,GPIO.LOW)
#         p2.ChangeDutyCycle(75)
#         x = 'z'

#     elif x == 'M':
#         print("Running both motors")
#         GPIO.output(in1,GPIO.HIGH)
#         GPIO.output(in2,GPIO.LOW)
#         GPIO.output(in3,GPIO.HIGH)
#         GPIO.output(in4,GPIO.LOW)
#         p1.ChangeDutyCycle(75)
#         p2.ChangeDutyCycle(75)
#         x = 'z'

#     elif x == 'S':
#         print("Stopping both motors")
#         GPIO.output(in1,GPIO.LOW)
#         GPIO.output(in2,GPIO.LOW)
#         GPIO.output(in3,GPIO.LOW)
#         GPIO.output(in4,GPIO.LOW)
#         p1.ChangeDutyCycle(0)
#         p2.ChangeDutyCycle(0)
#         x = 'z'

#     elif x == 'E':
#         GPIO.cleanup()
#         print("GPIO Clean up")
#         break
    