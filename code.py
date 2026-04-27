# PERFEC System Clock
# boot.py
# copyright 2026, Tom Hoffman
# MIT License

# This module contains the main loop of the application.

import gc
print("After gc: " + str(gc.mem_free()))
import supervisor   # pylint: disable=warning-name


from minimal_midi import MinimalMidi   # pylint: disable=warning-name

print("After minimal_midi: " + str(gc.mem_free()))

import cpx   # pylint: disable=warning-name
print("After cpx: " + str(gc.mem_free()))

from model import ApplicationModel   # pylint: disable=warning-name
print("After model: " + str(gc.mem_free()))

from board_controller import ActiveView   # pylint: disable=warning-name
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






