from micropython import const
import supervisor

import config

_TICKS_PERIOD = const(1<<29)

class ApplicationModel(object):
    '''This class should contain properties that store the state of the application.'''
    def __init__(self, 
                 nanos_per_pulse=config.nanos_per_pulse, 
                 pulses=0,
                 last_tap=0,
                 next_pulse=None,
                 photon=0,
                 changed=True,
                 tap_history = [0] * config.TAP_COUNT,
                 tap_index = 0,
                 taps_received = 0):
        self.nanos_per_pulse = nanos_per_pulse
        self.pulses = pulses
        self.last_tap = last_tap
        self.next_pulse = next_pulse
        self.photon = photon
        self.changed = changed
        self.tap_history = tap_history
        self.tap_index = tap_index
        self.taps_received = taps_received

    def increment_pulses(self) -> bool:
        '''Called when a pulse is triggered to update the model.'''
        self.pulses += 1
        self.next_pulse += self.nanos_per_pulse
        if self.pulses >= config.ppqn:
            self.advance_photon()

    def zero_pulses(self):
        self.pulses = 0
        self.changed = True

    def reset_photon(self):
        self.photon = 0
        self.zero_pulses()

    def advance_photon(self):
        self.photon = (self.photon + 1) % 10
        self.zero_pulses()

    def update_nanos(self, new_time: int):
        if self.last_tap and (new_time - self.last_tap) > config.TAP_TIMEOUT_NS:
            self.total_taps = 0
            self.tap_index = 0

    def reset_taps(self, now: int):
        self.taps_received = 0
        self.tap_index = 0
        self.last_tap = now

    def process_tap(self, now: int):
        if (self.last_tap == 0) or ((now - self.last_tap) >= config.TAP_TIMEOUT_NS):
            self.reset_taps(now)
        else: 
            delta: int = now - self.last_tap
            self.tap_history[self.tap_index] = delta
            self.tap_index = (self.tap_index + 1) % config.TAP_COUNT
            if self.taps_received < config.TAP_COUNT:
                self.taps_received += 1
            avg_delta: int = sum(self.tap_history) // self.taps_received
            self.nanos_per_pulse = (avg_delta // config.ppqn) - config._LOOP_OVERHEAD_NS
            self.last_tap = now
        self.changed = True
