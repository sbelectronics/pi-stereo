#!/bin/bash
FREQ=$1
date >> /tmp/start_tone.log
echo "start_tone called" >> /tmp/start_tone.log
echo "tone: $FREQ" >> /tmp/start_tone.log
cd /home/pi
su pi -c "screen -AmdS toneplayer bash -c \"speaker-test -c 2 -f $FREQ -t sine |& tee -a /tmp/run_toneplayer.log\""
echo "after the screen call" >> /tmp/start_tone.log
