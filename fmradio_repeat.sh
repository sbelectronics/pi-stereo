#!/bin/bash
STATION=$1
while [[ 1 ]]; do
     # mono at twice the frequency to make the digi+ happy 
     rtl_fm -M wbfm -s 250000 -f $STATION -r 64k | aplay -r 32k -f S16_LE -c 2  
     # mono for USB
#    rtl_fm -M wbfm -f $STATION -r 48k | aplay -r 48k -f S16_LE
done
