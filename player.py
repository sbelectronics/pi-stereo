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
    def __init__(self, power=None):
        Thread.__init__(self)

        self.immediate = False
        self.station = "None"
        self.player = "None"
        self.player_non_file_player = None
        self.last_queue_item = {}
        self.power = power
        self.queue = Queue()

        self.set_station("pandora")

        self.daemon = True
        self.start()

    def setPlayer(self, player, *args):
        self.destroy_screen("pianobar")
        self.destroy_screen("fmradio")
        self.destroy_screen("fileplayer")
        self.destroy_screen("toneplayer")

        if (player == "pianobar"):
            self.run_player("start_pianobar.sh", *args)
        elif (player == "fmradio"):
            self.run_player("start_fmradio.sh", *args)
        elif (player == "fileplayer"):
            self.run_player("start_fileplayer.sh", *args)
        elif (player == "toneplayer"):
            self.run_player("start_toneplayer.sh", *args)

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

    def get_now_playing(self):
        result = {}

        result["song"] = "unknown"
        result["artist"] = "unknown"
        result["station"] = "unknown"
        result["stationCount"] = "0"
        result["stations"] = []

        # First get all of the pandora state, since we always want to make sure the station array is populated.

        try:
            lines = open("/var/pianobar/now_playing_vars").readlines()
            for line in lines:
                if (not "=" in line):
                    continue
                (k, v) = line.split("=", 1)

                if (k == "artist"):
                    result["artist"] = v
                elif (k == "title"):
                    result['song'] = v
                elif (k == "stationName"):
                    result['station'] = v
                elif (k == "stationCount"):
                    result['stationCount'] = v
                elif (k.startswith("station")):
                    tmp = (k[7:], v)
                    result["stations"].append(tmp)
        except:
            pass

        # Now, if we're using the fileplayer then let's set the title and artist to what was passed to us in the
        # fileplayer request.

        if (self.player == "fileplayer"):
            artist = self.last_queue_item.get("artist")
            if artist:
                result["artist"] = artist
            song = self.last_queue_item.get("song")
            if song:
                result["song"] = song

        return result


    def is_idle(self):
        if (self.player in ["fileplayer", "toneplayer"]):
            # Look for some screen session that's running a fileplayer. If that screen session exists, then the player
            # is still active.
            for dir in os.listdir("/var/run/screen"):
                screenDir = os.path.join("/var/run/screen", dir)
                for fn in os.listdir(screenDir):
                    parts = fn.split(".")
                    if len(parts) == 2:
                        if parts[1] == self.player:
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
            self.setPlayer("fileplayer", '"'+name[5:]+'"')
        elif (name.startswith("tone:")):
            self.setPlayer("toneplayer", name[5:])
        elif name.startswith("radio:"):
            x=int(name[6:])*100000
            #x=x-10000
            self.setPlayer("fmradio", str(x))

        self.station = name

        if (not name.startswith("file:")) and (not name.startswith("tone:")):
            self.last_non_file_player = name

    def set_station(self, name, artist=None, song=None, immediate=True):
        if immediate:
            while not self.queue.empty():
                self.queue.get()
            self.immediate = True

        self.queue.put({"name": name,
                        "artist": artist,
                        "song": song})

    # TODO: next_song() should probably go through the Thread...

    def next_song(self):
        if self.player == "pianobar":
            open("/home/pi/.config/pianobar/ctl","w").write("n\n")
        elif self.player == "fileplayer":
            self.destroy_screen("fileplayer")
        elif self.player == "toneplayer":
            self.destroy_screen("toneplayer")

    def set_pandora_station(self, num):
        open("/home/pi/.config/pianobar/ctl","w").write("s%s\n" % str(num))

    def ban_song(self):
        open("/home/pi/.config/pianobar/ctl","w").write("-\n")

    def love_song(self):
        open("/home/pi/.config/pianobar/ctl","w").write("+\n")

    def run(self):
        while True:
            if not self.queue.empty():
                pop_the_queue = self.is_idle()
                if (self.immediate):
                    self.immediate = False
                    pop_the_queue = True

                if pop_the_queue:
                    item = self.queue.get()
                    self.last_queue_item = item
                    print "popped from queue:", item["name"]
                    self._set_station(item["name"])

            # After we've played any files that were requested, we want to return to non-file (Pandora or FM) mode
            if (self.player in ["fileplayer", "toneplayer"]) and (self.is_idle()):
                if (self.last_non_file_player):
                    print "setting last_non_file_player"
                    self._set_station(self.last_non_file_player)
                if self.power:
                    self.power.on_idle()


            time.sleep(0.1)
