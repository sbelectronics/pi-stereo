class DummyMotorPot:
    def __init__(self):
        self.value = 1234
        self.setPoint = None
        self.moving = False

    def set(self, value):
        self.setPoint = value
        self.value = value

class DummyPower:
    def __init__(self):
        self.power = False

    def set_power(self, value):
        self.power = value

class DummyPlayer:
    def __init__(self):
        self.station = "None"

    def set_station(self, value):
        self.station = value


StereoPot = None
Power = None
Player = None
Mux = None
def startup(noHardware=False):
    global StereoPot, Power, Player, Mux
    if noHardware:
        StereoPot = DummyMotorPot()
        Power = DummyPower()
        Player = DummyPlayer()
        Mux = DummyMux()
    else:
        #import RPi.GPIO as IO
        #IO.setwarnings(False)

        from motorpot import MotorPot
        import smbus
        bus = smbus.SMBus(1)
        #StereoPot = DummyMotorPot()
        StereoPot = MotorPot(bus, dirmult=-1) # , verbose=True)

        from power import PowerControl
        Power = PowerControl()

        from player import PlayerControl
        Player = PlayerControl()

        from mux import MuxControl, MUX_ADDR
        Mux = MuxControl(bus, addr = MUX_ADDR)

