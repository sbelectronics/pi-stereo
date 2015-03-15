class DummyMotorPot:
    def __init__(self):
        self.value = 1234
        self.setPoint = None

    def set(self, value):
        self.setPoint = value
        self.value = value

class DummyPower:
    def __init__(self):
        self.power = False

    def set_power(self, value):
        self.power = value


StereoPot = None
Power = None
def startup(noHardware=False):
    global StereoPot, Power
    if noHardware:
        StereoPot = DummyMotorPot()
        Power = DummyPower()
    else:
        from motorpot import MotorPot
        import smbus
        bus = smbus.SMBus(1)
        StereoPot = MotorPot(bus, dirmult=-1) # , verbose=True)

        from power import PowerControl
        Power = PowerControl()

