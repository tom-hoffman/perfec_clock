# PERFEC System Clock
# boot.py
# copyright 2026, Tom Hoffman
# MIT License

# This module contains the main loop of the application.

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




        

