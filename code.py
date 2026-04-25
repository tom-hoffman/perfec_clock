# SPDX-FileCopyrightText: 2025 Tom Hoffman & E-Cubed students
# SPDX-License-Identifier: MIT

# Modular Playground Tap Tempo Clock

# Module Description:
# This is a CircuitPython implementation of a
# tap tempo MIDI clock.
# CircuitPython is not exactly ideal for precise timing,
# so we need to make some concessions to maximize accuracy.

# If we're in Active mode, main loop just checks the timing 
# to send out a MIDI tick and occasionally the switch to 
# see if we should change modes.

# Tap mode stops the clock, because we want to be able to do that
# to reset the sequencers.

# This could be modified to keep the clock running at all times.

# In tap mode, we calculate the tempo based on the timing of 
# button taps.  For simplicity we're just doing the last two
# taps (not an average of more).


import gc
print("After gc: " + str(gc.mem_free()))

import supervisor

from minimal_midi import MinimalMidi
print("After minimal_midi: " + str(gc.mem_free()))

import cpx

print("After cpx: " + str(gc.mem_free()))

from model import ApplicationModel
print("After model: " + str(gc.mem_free()))

from board_controller import ActiveView 
print("After board controller: " + str(gc.mem_free()))

midi = MinimalMidi()

mod = ApplicationModel() 

bc = ActiveView(mod, midi).update_mode()
cpx.led.value = False
bc.update_pixels()

print("After object creation: " + str(gc.mem_free()))

mod.next_pulse = supervisor.ticks_ms() + mod.millis_per_pulse
midi.send_start()

while True:
    bc.check_time()
    bc.check_buttons()
    bc = bc.update_mode()
    if mod.changed:
        bc.update_pixels()
        mod.changed = False




        

