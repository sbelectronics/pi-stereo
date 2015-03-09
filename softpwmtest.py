import RPi.GPIO as IO
#import RPi.GPIO as PWM

L293_1 = 22
L293_2 = 23
L293_ENABLE = 18

IO.setmode(IO.BCM)
IO.setup(L293_ENABLE, IO.OUT)
IO.setup(L293_1, IO.OUT)
IO.setup(L293_2, IO.OUT)

IO.output(L293_1, True)
IO.output(L293_2, False)
IO.output(L293_ENABLE, False)

#servo = PWM.Servo()                                                                                               
#servo.set_servo(L293_ENABLE, 1200)    

pwm = IO.PWM(L293_ENABLE,100)
pwm.start(100)


while True:
    cmd = raw_input("Command, f/r 0..9, E.g. f5 :")
    direction = cmd[0]
    speed = int(cmd[1])
    if direction == "f":
        IO.output(L293_1, False)
        IO.output(L293_2, True)
    else:
        IO.output(L293_1, True)
        IO.output(L293_2, False)    
    pwm.ChangeDutyCycle(100*speed/9)
    #servo.set_servo(L293_ENABLE, speed*100)
