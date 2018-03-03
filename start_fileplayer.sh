#!/bin/bash
FN=$1
date >> /tmp/start_fileplayer.log
echo "start_fileplayer called" >> /tmp/start_fileplayer.log
echo "filename: $FN" >> /tmp/start_fileplayer.log
cd /home/pi
su pi -c "screen -AmdS fileplayer bash -c \"aplay \\\"$FN\\\" |& tee -a /tmp/run_fileplayer.log\""
echo "after the screen call" >> /tmp/start_fileplayer.log
