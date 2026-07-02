# PERFEC System Clock
# boot.py
# copyright 2026, Tom Hoffman
# MIT License

# sets the name of the Circuit Playground as it appears to a PC
# from https://github.com/todbot/circuitpython-tricks#usb

# Note that all the USB indicators might not show up without unplugging the board
# and (on Ubunutu) flushing the USB cache:
# `sudo systemctl restart alsa-state``

import usb-midi
import supervisor
import config
import storage

supervisor.set_usb_identification(
	manufacturer="PERFEC Systems",
	product=config.USB_NAME
)

storage.remount("/", readonly=False)
m = storage.getmount("/")
m.label = config.USB_NAME
storage.remount("/", readonly=True)

usb_midi.set_names(streaming_interface_name = "CLOCK OUT")
