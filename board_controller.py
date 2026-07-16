# PERFEC System Clock
# board_controller.py
# copyright 2026, Tom Hoffman
# MIT License

import time
import cpx
import config

class View(object):
    def __init__(self, model, midi, pix=cpx.pix):
        self.model = model
        self.midi = midi
        self.pix = pix
        # Cache local reference to time function for high-frequency checks
        self._get_time = time.monotonic_ns
        self._dim_white = (32, 32, 32)

    def check_time(self):
        now = self._get_time()
        if (self.model.next_pulse - config.LATENCY_NS) <= now:
            self.model.increment_pulses(now)
            self.send_pulse()

    def run_loop_tick(self):
        """Default loop step behavior."""
        self.check_time()
        self.check_buttons()

    def enter_mode(self):
        self.model.changed = True
        self.model.reset_photon()

    def update_pixels(self, c):
        self.pix.fill(c)
        self.pix[self.model.photon] = self._dim_white
        cpx.pix.show()

class ActiveView(View):
    def __init__(self, model, midi, pix=cpx.pix):
        super().__init__(model, midi, pix)
        self._bg_color = (0, 8, 0)

    def run_loop_tick(self):
        # Active mode hammers the time check in a tight block to preserve precision
        for _ in config.ACTIVE_REPEATS:
            self.check_time()

    def enter_mode(self):
        super().enter_mode()
        self.midi.send_start()

    def check_buttons(self):
        pass

    def update_pixels(self):
        super().update_pixels(self._bg_color)

    def send_pulse(self):
        self.midi.send_clock()
        cpx.led.value = not(cpx.led.value)

class TapView(View):
    def __init__(self, model, midi, pix=cpx.pix):
        super().__init__(model, midi, pix)
        self._bg_color = (8, 0, 0)

    def check_buttons(self):
        if cpx.a_button.went_down() or cpx.b_button.went_down():
            new_ns = self._get_time()
            if self.model.last_tap:
                # Call the updated nanosecond calculation module method
                self.model.update_ns(new_ns)
            else:
                self.model.last_tap = new_ns

    def enter_mode(self):
        super().enter_mode()
        self.model.last_tap = None
        cpx.led.value = False
        self.midi.send_stop()

    def update_pixels(self):
        super().update_pixels(self._bg_color)

    def send_pulse(self):
        pass
