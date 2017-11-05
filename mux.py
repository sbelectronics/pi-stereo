import sys
from ioexpand import PCF8574

MUX_ADDR = 0x20

class MuxControl(PCF8574):
    def __init__(self, bus, addr):
        PCF8574.__init__(self, bus, addr)
        self.bus.write_byte(self.addr, 0x00)  # all IO are outputs

    def set_channel(self, i):
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
