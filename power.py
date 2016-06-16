from threading import Thread
from motor import L293_3, L293_4, L293_ENABLE2
import RPi.GPIO as IO
import socket
import time
import traceback

INPUT_1 = 7

MULT_0 = 16
MULT_1 = 26
#MULT_2 = 20
#MULT_3 = 21

RELAY_BOARD_IP = "198.0.0.238"

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

        IO.setup(MULT_0, IO.OUT)
        IO.setup(MULT_1, IO.OUT)
#        IO.setup(MULT_2, IO.OUT)
#        IO.setup(MULT_3, IO.OUT)

        IO.output(self.pin1, False)
        IO.output(self.pin2, False)
        IO.output(self.enable, True)

        self.power = False
        self.newPower = None
        self.turnOnTime = None

        self.daemon = True

        self.set_input(2)

        self.start()

    def set_input(self, value):
        self.input = value
        value = value + 4
        IO.output(MULT_0, value&1)
        IO.output(MULT_1, (value>>1)&1)
#        IO.output(MULT_2, (value>>2)&1)
#        IO.output(MULT_3, (value>>3)&1)

    def set_power(self, value):
        self.newPower = value
        try:
            if value:
                msg = "1 on"
            else:
                msg = "1 off"
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(msg, (RELAY_BOARD_IP, 1234))
        except:
            traceback.print_exc("failed to notify the relay board")

    def delay_off(self, amount):
        self.set_power(False)
        if (not self.power) and (self.turnOnTime is not None) and (self.turnOnTime > time.time()):
            self.turnOnTime = self.turnOnTime + amount
        else:
            self.turnOnTime = time.time() + amount

    def next_song(self):
        open("/home/pi/.config/pianobar/ctl","w").write("n\n")

    def set_station(self, num):
        open("/home/pi/.config/pianobar/ctl","w").write("s%s\n" % str(num))

    def ban_song(self):
        open("/home/pi/.config/pianobar/ctl","w").write("-\n")

    def love_song(self):
        open("/home/pi/.config/pianobar/ctl","w").write("+\n")

    def run(self):
        last_input1 = True # inputs have pullups

        while True:
            # check for a turn-on event from delay_off()
            if (self.turnOnTime is not None) and (time.time() > self.turnOnTime):
                self.newPower = True
                self.turnOnTime = None

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




