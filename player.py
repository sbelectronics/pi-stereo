import os
import time

"""
from player import PlayerControl
PlayerControl().destroy_screen("pianobar")
PlayerControl().run_player("start_pianobar.sh")
"""

class PlayerControl:
    def __init__(self):
        self.station = "None"
        self.player = "None"
        self.set_station("pandora")

    def setPlayer(self, player, *args):
        self.destroy_screen("pianobar")
        self.destroy_screen("fmradio")

        if (player == "pianobar"):
            self.run_player("start_pianobar.sh", *args)
        elif (player == "fmradio"):
            self.run_player("start_fmradio.sh", *args)

        self.player = player

    def destroy_screen(self, name):
        for dir in os.listdir("/var/run/screen"):
            screenDir = os.path.join("/var/run/screen", dir)
            for fn in os.listdir(screenDir):
                parts = fn.split(".")
                if len(parts)==2:
                    if name in parts[1]:
                        # using screen has issues with usernames
                        #os.system("screen -X -S %s quit" % parts[0])
                        # so just kill the damn thing instead
                        print "kill process %s" % parts[0]
                        os.system("kill %s" % parts[0])

    def run_player(self, name, *args):
        fn = os.path.join("/home/pi", name)
        os.system(" ".join([fn] + list(args)))

    def set_station(self, name):
        if (name == self.station):
            return
        if (name=="pandora"):
            self.setPlayer("pianobar")
        else:
            x=int(name)*100000
            x=x-20000
            self.setPlayer("fmradio", str(x))
        self.station = name

