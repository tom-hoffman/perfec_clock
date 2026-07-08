# PERFEC System Clock # model.py 
# copyright 2026, Tom Hoffman # MIT License

import gc
import config

# Cache constants locally to bypass global dictionary lookups
_PPQN = config.ppqn
_TAP_COUNT = config.TAP_COUNT
_TAP_TIMEOUT_NS = config.TAP_TIMEOUT_NS
_LOOP_OVERHEAD_NS = config._LOOP_OVERHEAD_NS

class ApplicationModel(object):
    '''Highly optimized state model for a strict straight-time tap-tempo clock.'''
    def __init__(self, nanos_per_pulse=config.nanos_per_pulse, pulses=0, last_tap=0, next_pulse=None, photon=0, changed=True, tap_index=0, taps_received=0):
        self.nanos_per_pulse = nanos_per_pulse
        # Prime the clock at the final tick boundary so the next incoming pulse triggers step 0 instantly
        self.pulses = pulses if pulses is not None else (_PPQN - 1)
        self.last_tap = last_tap
        self.next_pulse = next_pulse
        self.photon = photon
        self.changed = changed
        
        # Avoid sharing mutable default arguments in constructor
        self.tap_history = [0] * _TAP_COUNT
        self.tap_index = tap_index
        self.taps_received = taps_received
        
        # Optimization: Maintain a running history sum to eliminate costly sum() calls
        self._tap_history_sum = 0

    def increment_pulses(self):
        '''Time-critical execution path for processing clock beats.'''
        # Straight-time calculation: direct addition without conditional branching
        self.next_pulse += self.nanos_per_pulse

        p = self.pulses + 1
        if p >= _PPQN:
            # Advance photon and reset counter directly
            ph = self.photon + 1
            self.photon = 0 if (ph >= 10) else ph
            self.pulses = 0
            self.changed = True
            gc.collect()
        else:
            self.pulses = p

    def zero_pulses(self):
        # Priming state for clean external clock starts
        self.pulses = _PPQN - 1
        self.changed = True

    def reset_photon(self):
        self.photon = 9
        self.pulses = _PPQN - 1
        self.changed = True

    def advance_photon(self):
        ph = self.photon + 1
        self.photon = 0 if (ph >= 10) else ph
        self.pulses = 0
        self.changed = True

    def update_nanos(self, new_time):
        if self.last_tap and (new_time - self.last_tap) > _TAP_TIMEOUT_NS:
            self.taps_received = 0  
            self.tap_index = 0

    def reset_taps(self, now):
        self.taps_received = 0
        self.tap_index = 0
        self._tap_history_sum = 0
        self.last_tap = now

    def process_tap(self, now):
        '''Calculates tempo on the fly with running sums to prevent execution lag.'''
        last = self.last_tap
        if (last == 0) or ((now - last) >= _TAP_TIMEOUT_NS):
            self.taps_received = 0
            self.tap_index = 0
            self._tap_history_sum = 0
            self.last_tap = now
            return

        delta = now - last
        idx = self.tap_index
        received = self.taps_received

        # Optimization: Subtract the old delta being overwritten before adding the new one
        # This completely removes the slow sum(self.tap_history) function tax
        self._tap_history_sum = self._tap_history_sum - self.tap_history[idx] + delta
        self.tap_history[idx] = delta

        # Optimized index boundaries rollover instead of modulo (%) arithmetic
        idx += 1
        if idx >= _TAP_COUNT:
            idx = 0
        self.tap_index = idx

        if received < _TAP_COUNT:
            received += 1
            self.taps_received = received

        avg_delta = self._tap_history_sum // received
        self.nanos_per_pulse = (avg_delta // _PPQN) - _LOOP_OVERHEAD_NS
        self.last_tap = now
        self.changed = True
