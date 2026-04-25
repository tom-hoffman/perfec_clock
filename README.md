# PERFEC System: Tap-tempo MIDI Clock

A MIDI clock for the PERFEC System, written in CircuitPython for the Adafruit Circuit Playground Express (CPX).

## Use

The clock has two modes, set by the CPX switch:

* switch right -> **active mode**: neopixels are green;
* switch left -> **tap mode**: neopixels are red.

### active mode

In **active mode**, the clock is sending out MIDI clock messages (pulses).  The red LED flashes when pulses are sent, the white neopixel advances on quarter notes (as specified in `config.py`).  

In this mode the buttons have no effect.  Moving the switch left changes to **tap mode**.

When starting in or switching to active mode, a MIDI start message is sent.  


### tap mode

In **tap mode**, no MIDI clock messages are sent.  In this mode the user can set the tempo by tapping on either button a or b.  

The tempo is based on *the last two taps*.  There is no averaging of a series of taps (in this version).  The rate of the white neopixel's advance reflects the new tempo.

Moving the switch to the right changes to **active mode**.

When switching to **tap mode**, a MIDI stop message is sent.  When switching out of **tap mode** a MIDI start message is sent.


