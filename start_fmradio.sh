#!/bin/bash
STATION=$1
date >> /tmp/start_fmradio.log
echo "start_pianobar called" >> /tmp/start_fmradio.log
cd /home/pi
su pi -c "screen -AmdS fmradio ./fmradio_repeat.sh $STATION"
echo "after the screen call" >> /tmp/start_fmradio.log
