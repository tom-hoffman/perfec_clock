# PERFEC System Clock
# board_controller.py
# copyright 2026, Tom Hoffman
# MIT License

import gc
import time

import cpx
import config

_TAP_COLORS = ((8, 0, 16,), (16, 0, 8), (16, 8, 0), (0, 8, 16))

get_time = time.monotonic_ns

class View(object):

    def __init__(self, model, midi, pix=cpx.pix):
        self.model = model 
        self.midi = midi
        self.pix = pix

    def check_time(self):
        if get_time() >= self.model.next_pulse:
            self.model.increment_pulses()
            self.send_pulse()
            self.update_mode()
            gc.collect()

    def update_mode(self):
        self.model.changed = True
        self.model.reset_photon()
    
    def update_pixels(self, c):
        # Re-draw the neopixels.
        self.pix.fill(c)
        self.pix[self.model.photon] = (32, 32, 32)
        cpx.pix.show()


class ActiveView(View):

    def update_mode(self):
        # Check the switch and return current mode.
        if cpx.switch_is_left():
            super().update_mode()
            self.model.last_tap = get_time()
            cpx.led.value = False
            self.midi.send_stop()
            return TapView(self.model, self.midi, self.pix)
        else:
            return self

    def check_buttons(self):
        pass
    
    def update_pixels(self):
        super().update_pixels((0, 8, 0))

    def send_pulse(self):
        self.midi.send_clock()
        cpx.led.value = not(cpx.led.value)


class TapView(View):

    def check_buttons(self):
        if cpx.a_button.went_down() or cpx.b_button.went_down():
            now = get_time()
            self.model.process_tap(now)

    def update_mode(self):
        if cpx.switch_is_left():
            return self
        else:
            super().update_mode()
            self.midi.send_start()
            return ActiveView(self.model, self.midi, self.pix)    

    def update_pixels(self):
        
        super().update_pixels(_TAP_COLORS[self.model.tap_index])

    def send_pulse(self):
        pass
