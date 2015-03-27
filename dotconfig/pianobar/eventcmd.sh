#!/bin/bash
# create variables
rm -f /home/pi/.config/pianobar/now_playing_vars.tmp
while read L; do
    k="`echo "$L" | cut -d '=' -f 1`"
    v="`echo "$L" | cut -d '=' -f 2`"
    export "$k=$v"
    echo "$k=$v" >> /home/pi/.config/pianobar/now_playing_vars.tmp
done < <(grep -e '^\(title\|artist\|album\|stationName\|songStationName\|pRet\|pRetStr\|wRet\|wRetStr\|songDuration\|songPlayed\|rating\|coverArt\|stationCount\|station[0-9]*\)=' /dev/stdin) # don't overwrite $1...

mv /home/pi/.config/pianobar/now_playing_vars.tmp /home/pi/.config/pianobar/now_playing_vars

case "$1" in
        songstart)
                 echo -e "$title\n$artist\n$stationName" > /home/pi/.config/pianobar/now_playing
esac
