import sys
import time
from threading import Thread
from motor import Motor, L293_1, L293_2, L293_ENABLE
from ads1015 import ADS1015, MUX_AIN0, PGA_4V, MODE_CONT, DATA_1600, COMP_MODE_TRAD, COMP_POL_LOW, COMP_NON_LAT, COMP_QUE_DISABLE

class MotorPot(Thread):
    def __init__(self, bus, adc_addr=0x48, motor_pin1=L293_1, motor_pin2=L293_2, motor_enable = L293_ENABLE, dirmult=1, verbose=False):
        Thread.__init__(self)

        self.motor = Motor(pin1=motor_pin1, pin2=motor_pin2, enable = motor_enable)
        self.motor.set_speed(0)

        self.adc = ADS1015(bus, adc_addr)

        self.adc.write_config(MUX_AIN0 | PGA_4V | MODE_CONT | DATA_1600 | COMP_MODE_TRAD | COMP_POL_LOW | COMP_NON_LAT | COMP_QUE_DISABLE)

        self.dirmult = dirmult

        self.setPoint = None
        self.newSetPoint = False

        self.daemon = True
        self.verbose = verbose

        self.start()

    def set(self, value):
        self.setPoint = value
        self.newSetPoint = True

    def run(self):
        setPoint = None
        while True:
            self.value = self.adc.read_conversion()

            if self.newSetPoint:
                setPoint = self.setPoint
                self.newSetPoint=False
                settle = 0

            if setPoint is not None:
                if (self.value < setPoint):
                    dir = 1
                else:
                    dir = -1

                # the 'P' part of a PID controller...
                error = abs(self.value - setPoint)
                if (error <= 1):
                    speed = 0

                    # are we done yet?
                    settle=settle+1
                    if (settle>10):
                        setPoint = None
                else:
                    settle = 0
                    if (error < 10):
                        settle = 0
                        speed = 50
                    elif (error < 100):
                        speed = 75
                    else:
                        speed = 100

                if self.verbose:
                    print "moving", self.value, setPoint, dir, speed

                self.motor.set_dir(dir * self.dirmult)
                self.motor.set_speed(speed)

            if setPoint is not None:
                # fine-grained timing while we're moving the pot
                time.sleep(0.001)
            else:
                if self.verbose:
                    print "monitor", self.value
                # course-grained if we're just reading it
                time.sleep(0.1)

def main():
    if len(sys.argv)<2:
        print "syntax: motorpot.py <value>"
        return

    print sys.argv

    import smbus
    bus = smbus.SMBus(1)

    motorpot = MotorPot(bus, dirmult=-1, verbose=True)

    if sys.argv[1]!="none":
        motorpot.set(int(sys.argv[1]))

    while True:
        time.sleep(1)


if __name__== "__main__":
    main()

