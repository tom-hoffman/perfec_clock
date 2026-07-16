# PERFEC System Clock
# minimal_midi.py
# copyright 2026, Tom Hoffman
# MIT License

# Customized ultra-minimal MIDI implementation for this module.

# This version only sends three global messages.

import usb_midi
from micropython import const

_CLOCK = const(b'\xF8')
_START = const(b'\xFA')
_STOP = const(b'\xFC')

# These "ports" are not to be confused with MIDI channels, etc.
_OUTIE = usb_midi.ports[1]

class MinimalMidi(object):
    """Sends MIDI Clock, Start and Stop messages."""
    
    def __init__(self):
        # Cache the port's write method to bypass dictionary lookups in loops
        self._write = _OUTIE.write

    def send_clock(self):
        self._write(_CLOCK)

    def send_start(self):
        self._write(_START)

    def send_stop(self):
        self._write(_STOP)
