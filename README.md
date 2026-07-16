# PERFEC System: Tap-tempo MIDI Clock

A simple MIDI clock for the PERFEC System, written in CircuitPython for the Adafruit Circuit Playground Express (CPX). 

The starting tempo can be set through configuration and changed by tapping the buttons ("tap-tempo").

This implementation is optimized for accuracy, with average jitter of around 0.5 milliseconds.

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

## Configuration

In `config.py`, the following can be adjusted:
* `USB_NAME`: "CLOCK" by default.
* `millis_per_pulse`: initial tempo based on milliseconds between MIDI clock messages. 28 by default (about 88 bpm).
* `ppqn`: pulses per quarter notes. This controls the rate of white neopixel advances.  24 is the default MIDI standard for quarter notes.
* `midi_repeat`: in active mode, number of times that the time is checked before checking to see if the switch moved.  256 by default.

## Installation

The `.py` files can be dragged directly onto a CPX's `CIRCUITPY` drive.

## Coding notes

Note that this package is small enough as to not requre precompilation into `.mpy` files, so there is no `make.py` file.

The priority in this version is timing precision for both the MIDI pulses and reading the button taps.  Many possible features were deferred in the interest of keeping this version clean and fast, given the inherent slowness and unreliable precision in running CircuitPython on a CPX!

Other components of the PERFEC System expect MIDI start and stop messages to reset sequences, so it is important to implement those at appropriate times.

This package is based on the **MMB template**.  Since this package only sends three global MIDI messages (and receives none), there is no separate `midi_controller.py` and the modified version of `minimal_midi.py` is extra minimal.

I tried using more `super()` class calls in `board_controller.py` to get rid of repetitive code in the subclasses.

## Testing output consistency.

On Ubuntu (probably other Debian-based Linux distributions as well) you can check the timing of your PERFEC Clock with a one line command:

`aseqdump -p XX:X | perl -MTime::HiRes=time -ne 'BEGIN{$|=1; $t=time} if(/Clock/){$n=time; printf "Interval: %.2f ms\n", ($n-$t)*1000; $t=$n}'`

Where `XX:X` should be replaced by the number corresponding to your CPX according to this command:

`aseqdump -l`

You may need to install the `alsa-utils` package:

```
sudo apt update
sudo apt install alsa-utils
```

Google Gemini came up with this. It works for me.
