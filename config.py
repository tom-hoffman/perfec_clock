# config.py

# Put starting variables here that might need to be changed by the user.

# Give each Circuit Playground a unique name so you don't get confused!
# Note that a MIDI network should only have one clock
# so you don't need to add an identifying number
USB_NAME = "CLOCK"

# Starting value for time between MIDI clock pulses
# the official default is 24 per quarter note
# but this is often increased by doubling
# 28 milliseconds per pulse equates to about 88 bpm.
millis_per_pulse: int = 28

# Pulses per quarter note
ppqn: int = 24

# Increasing this number makes the time slightly more accurate
# and the board somewhat less responsive.
midi_repeat: int = 255
