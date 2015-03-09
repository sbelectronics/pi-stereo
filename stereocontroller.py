class DummyMotorPot(self):
    def __init__(self):
        self.value = 1234

    def set(self, value):
        self.value = value

StereoPot = None
def startup(noHardware=False):
    global StereoPot
    if noHardware:
        StereoPot = DummyMotorPot()
    else:
        from motorpot import *
        import smbus
        bus = smbus.SMBus(1)
        StereoPot = MotorPot(bus, dirmult=-1, verbose=True)

