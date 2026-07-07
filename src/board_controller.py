# PERFEC System Clock # board_controller.py 
# copyright 2026, Tom Hoffman # MIT License

import cpx

# Pre-cache tuple data and internal objects for zero-allocation access
_TAP_COLORS = ((8, 0, 16), (16, 0, 8), (16, 8, 0), (0, 8, 16))
_PIX = cpx.pix
_LED = cpx.led
_A_BUTTON_WENT_DOWN = cpx.a_button.went_down
_B_BUTTON_WENT_DOWN = cpx.b_button.went_down

class View(object):
    def __init__(self, model, midi, pix=_PIX):
        self.model = model
        self.midi = midi
        self.pix = pix
        
        # Micro-cache standard class function hooks
        self._model_increment_pulses = model.increment_pulses
        self._send_pulse = self.send_pulse

    def check_time(self, current_ns):
        # Optimization: Accept current_ns argument directly from code.py loop
        # Crucial Fix: Completely removed `gc.collect()` which was causing massive timing jitter
        if current_ns >= self.model.next_pulse:
            self._model_increment_pulses()
            self._send_pulse()

    def update_mode(self):
        self.model.changed = True
        self.model.reset_photon()

    def update_pixels(self, c):
        # Optimized flat writing block bypassing multi-step parent methods
        pix = self.pix
        pix.fill(c)
        pix[self.model.photon] = (32, 32, 32)
        pix.show()

class ActiveView(View):
    def __init__(self, model, midi, pix=_PIX):
        super().__init__(model, midi, pix)
        self._midi_send_clock = midi.send_clock

    def update_mode(self):
        # State swapping shifts entirely to code.py; this acts as a setup hook
        super().update_mode()
        _LED.value = False
        self.midi.send_stop()
        return self

    def check_buttons(self):
        pass

    def update_pixels(self):
        # Direct local execution without calling super() inheritance structures
        pix = self.pix
        pix.fill((0, 8, 0))
        pix[self.model.photon] = (32, 32, 32)
        pix.show()

    def send_pulse(self):
        self._midi_send_clock()
        _LED.value = not _LED.value

class TapView(View):
    def __init__(self, model, midi, pix=_PIX):
        super().__init__(model, midi, pix)
        self._model_process_tap = model.process_tap

    def check_buttons(self):
        # Short-circuit button checking via micro-cached digital IO methods
        if _A_BUTTON_WENT_DOWN() or _B_BUTTON_WENT_DOWN():
            import time
            self._model_process_tap(time.monotonic_ns())

    def update_mode(self):
        # State swapping shifts entirely to code.py; this acts as a setup hook
        super().update_mode()
        self.midi.send_start()
        return self

    def update_pixels(self):
        # Direct local pixel drawing to optimize visual rendering latency
        pix = self.pix
        pix.fill(_TAP_COLORS[self.model.tap_index])
        pix[self.model.photon] = (32, 32, 32)
        pix.show()

    def send_pulse(self):
        pass
