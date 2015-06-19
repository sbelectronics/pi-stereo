#!/bin/bash
date >> /tmp/start_pianobar.log
echo "start_pianobar called" >> /tmp/start_pianobar.log
cd /home/pi
su pi -c "screen -AmdS pianobar ./pianobar_repeat.sh"
echo "after the screen call" >> /tmp/start_pianobar.log
