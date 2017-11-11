ADDR=198.0.0.215
#ADDR=198.0.0.241
rsync -avz --exclude "__history" --exclude "*~" --exclude "*.img" --exclude "home-pi-*" --exclude "dot*" --exclude "*.conf" --exclude "*.pyc" --exclude "royalty_free" --exclude ".git" -e ssh . pi@$ADDR:/home/pi/stereo
