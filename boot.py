# PERFEC System Clock
# boot.py
# copyright 2026, Tom Hoffman
# MIT License

# sets the name of the Circuit Playground as it appears to a PC
# from https://github.com/todbot/circuitpython-tricks#usb

<<<<<<< HEAD
# Also essentially spamming all the other USB MIDI related names
# to try to ensure your DAW and OS will be able to differentiate
# between different modules.
=======
# Note that all the USB indicators might not show up without unplugging the board
# and (on Ubunutu) flushing the USB cache:
# `sudo systemctl restart alsa-state``
>>>>>>> 7d4acad (Performance improvements and better tap w/help from Gemini.)

import usb-midi
import supervisor
import config
import storage
import usb_midi
import supervisor



supervisor.set_usb_identification(
	manufacturer="PERFEC Systems",
	product=config.USB_NAME
)

storage.remount("/", readonly=False)
m = storage.getmount("/")
n = config.USB_NAME
m.label = n
usb_midi.set_names(streaming_interface_name = n + "-STR",
				   audio_control_interface_name =n  + "-AUD",
				   in_jack_name = n + "-IN",
				   out_jack_name = n + "-OUT")
supervisor.set_usb_identification(manufacturer="PERFEC", 
                                  product=n)
storage.remount("/", readonly=True)

usb_midi.set_names(streaming_interface_name = "CLOCK OUT")
