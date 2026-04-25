from micropython import const
import supervisor

import config

_TICKS_PERIOD = const(1<<29)
_TICKS_MAX = const(_TICKS_PERIOD-1)
_TICKS_HALFPERIOD = const(_TICKS_PERIOD//2)

class ApplicationModel(object):
    '''This class should contain properties that store the state of the application.'''
    def __init__(self, 
                 millis_per_pulse=config.millis_per_pulse, 
                 pulses=0,
                 last_tap=None,
                 next_pulse=None,
                 photon=0,
                 changed=True):
        self.millis_per_pulse = millis_per_pulse
        self.pulses = pulses
        self.last_tap = last_tap
        self.next_pulse = next_pulse
        self.photon = photon
        self.changed = changed

    def increment_pulses(self) -> bool:
        '''Called when a pulse is triggered to update the model.'''
        self.pulses += 1
        self.next_pulse += self.millis_per_pulse
        if self.pulses >= config.ppqn:
            self.advance_photon()

    def is_time_to_advance(self) -> bool:
        return self.ticks_less(self.next_pulse, supervisor.ticks_ms())

    def zero_pulses(self):
        self.pulses = 0
        self.changed = True

    def reset_photon(self):
        self.photon = 0
        self.zero_pulses()

    def advance_photon(self):
        self.photon = (self.photon + 1) % 10
        self.zero_pulses()

    def update_millis(self, m):
        self.millis_per_pulse = self.ticks_diff(m, self.last_tap) // config.ppqn
        self.last_tap = m

    # below from https://docs.circuitpython.org/en/latest/shared-bindings/supervisor/index.html
    @staticmethod
    def ticks_diff(ticks1, ticks2):
        "Compute the signed difference between two ticks values, assuming that they are within 2**28 ticks"
        diff = (ticks1 - ticks2) & _TICKS_MAX
        diff = ((diff + _TICKS_HALFPERIOD) & _TICKS_MAX) - _TICKS_HALFPERIOD
        return diff

    @staticmethod
    def ticks_less(ticks1, ticks2):
        "Return true if ticks1 is less than ticks2, assuming that they are within 2**28 ticks"
        return ApplicationModel.ticks_diff(ticks1, ticks2) < 0
