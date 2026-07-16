# SPDX-FileCopyrightText: 2025 Tom Hoffman & E-Cubed students
# SPDX-License-Identifier: MIT
# PERFEC Clock

print("Starting PERFEC Clock...")

import gc
print("Free memory at start (after importing gc): " + str(gc.mem_free()))
import time
import cpx
import config
from model import ApplicationModel
from board_controller import ActiveView, TapView
from minimal_midi import MinimalMidi


# Calculate target nanoseconds per pulse based on starting BPM at boot time:
# (60 seconds * 1,000,000,000 ns) // (BPM * Pulses Per Quarter Note)
initial_ns_per_pulse = 60000000000 // (config.STARTING_BPM * config.PPQN)

# Pass the pre-calculated tempo parameter directly into the model.
mod = ApplicationModel(ns_per_pulse=initial_ns_per_pulse)
midi = MinimalMidi()

# Use cached view instances to avoid creating and destroying objects 
# and triggering garbage collection delays.
view_active = ActiveView(mod, midi)
view_tap = TapView(mod, midi)

# Dictionary key based on switch_is_left boolean.
view_map = {True: view_tap, False: view_active}
last_switch_state = cpx.switch_is_left()
bc = view_map[last_switch_state]
# Initialize LED and neopixels.
cpx.led.value = False
bc.update_pixels()

# Initialize the next pulse tracking using the nanosecond timer
mod.next_pulse = time.monotonic_ns() + mod.ns_per_pulse
midi.send_start()

print("Free memory staring main loop: " + str(gc.mem_free()))

while True:
    # Checks time and buttons.
    bc.run_loop_tick()
    
    # Handle the mode switch.
    current_switch_state = cpx.switch_is_left()
    if current_switch_state != last_switch_state:
        last_switch_state = current_switch_state
        bc = view_map[current_switch_state]
        bc.enter_mode()

    # Re-draw neopixels only when flagged
    if mod.changed:
        bc.update_pixels()
        mod.changed = False
