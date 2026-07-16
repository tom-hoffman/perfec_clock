# PERFEC System Clock
# config.py
# copyright 2026, Tom Hoffman
# MIT License

# Put starting variables here that might need to be changed by the user.

# Give each Circuit Playground a unique name so you don't get confused!
# Note that a MIDI network should only have one clock
# so you don't need to add an identifying number.
USB_NAME = "CLOCK"

# Starting value for the tempo in Beats Per Minute (BPM).
STARTING_BPM: int = 88

# Pulses (MIDI clock messages) per quarter note.
# The traditional standard is that MIDI devices count 24 pulses
# per quarter note.  
PPQN: int = 24

# Measured baseline internal latency of the processing loop in nanoseconds.
LATENCY_NS = 420000

# Increasing this number makes the time more accurate
# and the board less responsive.
MIDI_REPEAT: int = 1024

# Pre-allocated range loop based on the configuration setting 
# to optimize execution speed without allocating RAM at runtime
# (do not modify directly).
ACTIVE_REPEATS = range(MIDI_REPEAT)