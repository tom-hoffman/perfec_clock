import time
from micropython import const
import config



class ApplicationModel(object):
    '''Stores the state of the Clock.'''
    
    def __init__(self, 
                 ns_per_pulse,  # Required argument passed directly from code.py calculation
                 pulses=0, 
                 last_tap=None, 
                 next_pulse=None, 
                 photon=0, 
                 changed=True):
        self.ns_per_pulse = ns_per_pulse
        self.pulses = pulses
        self.last_tap = last_tap
        self.next_pulse = next_pulse
        self.photon = photon
        self.changed = changed
        # Cache reference to local performance method to avoid global lookups
        self._get_time = time.monotonic_ns

    def increment_pulses(self, current_ns) -> None:
        '''Called when a pulse is triggered to update the model using the actual time.'''
        self.pulses += 1
        # Base the next target on exactly when this tick completed plus the step duration
        self.next_pulse = current_ns + self.ns_per_pulse
        if self.pulses >= config.PPQN:
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

    def update_ns(self, current_ns):
        # Calculate nanoseconds per pulse directly using raw integer math
        self.ns_per_pulse = (current_ns - self.last_tap) // config.PPQN
        self.last_tap = current_ns
