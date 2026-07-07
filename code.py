# SPDX-FileCopyrightText: 2026 Tom Hoffman & E-Cubed students 
# SPDX-License-Identifier: MIT 

__version__ = "1.0.0 beta"

import gc
print("After gc: " + str(gc.mem_free()))
import time 
print("After time: " + str(gc.mem_free()))
from minimal_midi import MinimalMidi 
print("After minimal_midi: " + str(gc.mem_free()))
import cpx 
print("After cpx: " + str(gc.mem_free()))
from model import ApplicationModel 
print("After model: " + str(gc.mem_free()))
from board_controller import ActiveView, TapView # Pre-import TapView to cache global access
print("After board controller: " + str(gc.mem_free()))

gc.collect()

midi = MinimalMidi()
mod = ApplicationModel()

# Pre-instantiate both views to prevent dynamic heap fragmentation when switching modes
view_active = ActiveView(mod, midi)
view_tap = TapView(mod, midi) 

# Set initial state
bc = view_active.update_mode()
cpx.led.value = False
bc.update_pixels()
print("After object creation: " + str(gc.mem_free()))
gc.collect()
# Initialize master clock time index
mod.next_pulse = time.monotonic_ns() + mod.nanos_per_pulse
midi.send_start()


# Local Micro-Caching: Bind time-critical methods directly to local variable pointers.
# This cuts out python's deep attribute/dictionary path crawling inside the while loop.
_monotonic_ns = time.monotonic_ns
_switch_is_left = cpx.switch_is_left

# Direct view-method tracking anchors
bc_check_time = bc.check_time
bc_check_buttons = bc.check_buttons

# Pre-instantiate both views into a fixed state tuple
# Index True (1): ActiveView, Index False (0): TapView
view_map = {True: view_active, False: view_tap}
gc.collect()
while True:
    # 1. Immediate timing evaluation (Highest priority execution path)
    bc_check_time(_monotonic_ns())
    
    # 2. Input handling
    bc_check_buttons()
    
    # 3. Streamlined state check (Zero code duplication)
    target_view = view_map[_switch_is_left()]
    if bc is not target_view:
        bc = target_view
        bc_check_time = bc.check_time
        bc_check_buttons = bc.check_buttons
        mod.changed = True
        
    # 4. Hardware UI refresh
    if mod.changed:
        bc.update_pixels()
        mod.changed = False