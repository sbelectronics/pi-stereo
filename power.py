from threading import Thread
from motor import L293_3, L293_4, L293_ENABLE2
import RPi.GPIO as IO
import time

INPUT_1 = 7

class PowerControl(Thread):
    def __init__(self, pin1=L293_3, pin2=L293_4, enable=L293_ENABLE2):
        Thread.__init__(self)

        self.pin1 = pin1
        self.pin2 = pin2
        self.enable = enable

        print "pin1=",pin1, "pin2=",pin2, "enable=", enable

        IO.setmode(IO.BCM)
        IO.setup(INPUT_1, IO.IN)
        IO.setup(self.enable, IO.OUT)
        IO.setup(self.pin1, IO.OUT)
        IO.setup(self.pin2, IO.OUT)

        IO.output(self.pin1, False)
        IO.output(self.pin2, False)
        IO.output(self.enable, True)

        self.power = False
        self.newPower = None

        self.daemon = True

        self.start()

    def set_power(self, value):
        self.newPower = value

    def run(self):
        last_input1 = True # inputs have pullups

        while True:
            if (self.newPower is not None):
                print "power change", self.power, self.newPower
                self.power = self.newPower
                self.newPower = None
                IO.output(self.pin1, self.power)

            input1 = IO.input(INPUT_1)
            if (last_input1 != input1):
                print "input1 trigger"
                last_input1 = input1

                if input1:
                    # respond to button down
                    self.newPower = not self.power

            time.sleep(0.01)




