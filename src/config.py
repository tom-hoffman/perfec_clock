# config.py

# Put starting variables here that might need to be changed by the user.

# Give each Circuit Playground a unique name so you don't get confused!
# Note that a MIDI network should only have one clock 
# so you don't need to add an identifying number

from micropython import const

USB_NAME = "CLOCK"

# Initial beats per minute
starting_bpm: int = 120


# Pulses per quarter note
ppqn: int = 24

# Correction for inherent latency in SAMD21 running CircuitPython.
# This is based on testing against the Morningstar MIDI Monitor.  
# In theory it should be consistent across boards, 
# but if you need to fine tune yours, here you go!
# A larger number will subtract more time from the calculated rate, 
# giving you more BPM.
_LOOP_OVERHEAD_NS: int = const(240000)

# Starting value for time between MIDI clock pulses 

# Some Python math tips from Gemini
# 1. Calculate the full numerator and denominator using whole numbers
numerator: int = 60 * (10 ** 9)              # 60,000,000,000
denominator: int = starting_bpm * ppqn       # 36

# 2. Apply the integer rounding trick: add (denominator // 2) to the numerator
nanos_per_pulse: int = ((numerator + (denominator // 2)) // denominator) - _LOOP_OVERHEAD_NS


# Number of taps used to calculate new tempo.
TAP_COUNT: int = const(4)

# Number of seconds before resetting the tap tempo.
_TAP_TIMEOUT: int = const(2)

# Converting to nanoseconds (don't edit)
TAP_TIMEOUT_NS: int = const(_TAP_TIMEOUT * (10 ** 9))
