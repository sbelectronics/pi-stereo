#!/bin/bash

# NOTE: had to use the full path (/usr/local/bin/rtl_fn) on the pi4
# NOTE: had to remove the k from the 32k passed to aplay on the pi4

STATION=$1
while [[ 1 ]]; do
     # mono at twice the frequency to make the digi+ happy 
     /usr/local/bin/rtl_fm -M wbfm -s 250000 -f $STATION -r 64k | aplay -r 32 -f S16_LE -c 2  
     # mono for USB
#    rtl_fm -M wbfm -f $STATION -r 48k | aplay -r 48 -f S16_LE
done
