from threading import Thread
from Queue import Queue
import os
import time

"""
from player import PlayerControl
PlayerControl().destroy_screen("pianobar")
PlayerControl().run_player("start_pianobar.sh")
"""

class PlayerControl(Thread):
    def __init__(self):
        Thread.__init__(self)

        self.immediate = False
        self.station = "None"
        self.player = "None"
        self.player_non_file_player = None
        self.queue = Queue()

        self.set_station("pandora")

        self.daemon = True
        self.start()

    def setPlayer(self, player, *args):
        self.destroy_screen("pianobar")
        self.destroy_screen("fmradio")
        self.destroy_screen("fileplayer")

        if (player == "pianobar"):
            self.run_player("start_pianobar.sh", *args)
        elif (player == "fmradio"):
            self.run_player("start_fmradio.sh", *args)
        elif (player == "fileplayer"):
            self.run_player("start_fileplayer.sh", *args)

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

    def is_idle(self):
        if (self.player == "fileplayer"):
            # Look for some screen session that's running a fileplayer. If that screen session exists, then the player
            # is still active.
            for dir in os.listdir("/var/run/screen"):
                screenDir = os.path.join("/var/run/screen", dir)
                for fn in os.listdir(screenDir):
                    parts = fn.split(".")
                    if len(parts) == 2:
                        if parts[1] == "fileplayer":
                            return False

        # FM and Pandora are always idle

        return True

    def _set_station(self, name):
        print "set_station", name

        if (name == self.station) and (not name.startswith("file:")):
            return
        if (name.startswith("pandora")):
            self.setPlayer("pianobar")
        elif (name.startswith("file:")):
            self.setPlayer("fileplayer", name[5:])
        else:
            x=int(name)*100000
            #x=x-10000
            self.setPlayer("fmradio", str(x))

        self.station = name

        if (not name.startswith("file:")):
            self.last_non_file_player = name

    def set_station(self, name, immediate=True):
        if immediate:
            while not self.queue.empty():
                self.queue.get()
            self.immediate = True

        self.queue.put(name)

    def run(self):
        while True:
            if not self.queue.empty():
                pop_the_queue = self.is_idle()
                if (self.immediate):
                    self.immediate = False
                    pop_the_queue = True

                if pop_the_queue:
                    self._set_station(self.queue.get())

            # After we've played any files that were requested, we want to return to non-file (Pandora or FM) mode
            if (self.player == "fileplayer") and (self.is_idle()) and (self.last_non_file_player):
                self._set_station(self.last_non_file_player)

            time.sleep(0.1)
