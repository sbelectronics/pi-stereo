import sys
from ioexpand import PCF8574

MUX_ADDR = 0x20

class MuxControl(PCF8574):
    def __init__(self, bus, addr):
        PCF8574.__init__(self, bus, addr)
        self.set_channel(0) # default to channel 0

    def set_channel(self, i):
        self.input = i
        self.set_gpio(0, i)

def main():
    import smbus

    if len(sys.argv)<2:
        print "syntax: mux <channel-num>"
        sys.exit(-1)

    bus = smbus.SMBus(1)    
    mux = MuxControl(bus, MUX_ADDR)
    mux.set_channel(int(sys.argv[1]))

if __name__ == "__main__":
    main()
