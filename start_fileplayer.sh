#!/bin/bash
FN=$1
date >> /tmp/start_fileplayer.log
echo "start_fileplayer called" >> /tmp/start_fileplayer.log
cd /home/pi
su pi -c "screen -AmdS fileplayer aplay $FN"
echo "after the screen call" >> /tmp/start_fileplayer.log
