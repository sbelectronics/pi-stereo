sudo apt-get update
#sudo apt-get -y install json-devel gcrypt-devel gnutls-devel
#sudo apt-get -y install gmake pthreads labao gnutls gcrypt libfaad2 libmad UTF-8
sudo apt-get -y install libevent-pthreads-2.0-5 libao-dev libgnutls-dev libmad0-dev libfaad-dev libjson0-dev

sudo emacs /etc/modprobe.d/alsa-base.conf
  # comment out "options snd-usb-audio index=-2"

# copy pianobar config file from dotconfig/pianobar/config to .config/pianobar/config

emacs .config/pianobar/config
    event_command = /home/pi/.config/pianobar/eventcmd.sh
    fifo = /home/pi/.config/pianobar/ctl

mkfifo /home/pi/.config/pianobar/ctl