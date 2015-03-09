import sys
import time
from motor import Motor, L293_1, L293_2, L293_ENABLE
from ads1015 import ADS1015, MUX_AIN0, PGA_4V, MODE_CONT, DATA_1600, COMP_MODE_TRAD, COMP_POL_LOW, COMP_NON_LAT, COMP_QUE_DISABLE

class MotorPot:
    def __init__(self, bus, adc_addr=0x48, motor_pin1=L293_1, motor_pin2=L293_2, motor_enable = L293_ENABLE, dirmult=1):
        self.motor = Motor(pin1=motor_pin1, pin2=motor_pin2, enable = motor_enable)
        self.motor.set_speed(0)

        self.adc = ADS1015(bus, adc_addr)

        self.adc.write_config(MUX_AIN0 | PGA_4V | MODE_CONT | DATA_1600 | COMP_MODE_TRAD | COMP_POL_LOW | COMP_NON_LAT | COMP_QUE_DISABLE)

        self.dirmult = dirmult

    def set(self, value):
        settle = 0
        while True:
            v = self.adc.read_conversion()
            if (v < value):
                dir = 1
            else:
                dir = -1

            # the 'P' part of a PID controller...
            error = abs(v - value)
            if (error <= 1):
                speed = 0

                # are we done yet?
                settle=settle+1
                if (settle>10):
                    return
            else:
                settle = 0
                if (error < 10):
                    settle = 0
                    speed = 50
                elif (error < 100):
                    speed = 75
                else:
                    speed = 100

            print v, value, dir, speed

            self.motor.set_dir(dir * self.dirmult)
            self.motor.set_speed(speed)

            time.sleep(0.001)

def main():
    if len(sys.argv)<2:
        print "syntax: motorpot.py <value>"
        return

    print sys.argv

    import smbus
    bus = smbus.SMBus(1)

    motorpot = MotorPot(bus, dirmult=-1)

    if sys.argv[1]=="monitor":
        while True:
            print motorpot.adc.read_conversion()
            time.sleep(0.1)
    else:
        motorpot.set(int(sys.argv[1]))


if __name__== "__main__":
    main()

