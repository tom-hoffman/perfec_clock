# Testing output consistency.

On Ubuntu (probably other Debian-based Linux distributions as well) you can check the timing of your PERFEC Clock with a one line command:

`aseqdump -p XX:X | perl -MTime::HiRes=time -ne 'BEGIN{$t=time} if(/Clock/){$n=time; printf "Interval: %.2f ms\n", ($n-$t)*1000; $t=$n}'`

Where `XX:X` should be replaced by the number corresponding to your CPX according to this command:

`aseqdump -l`

Google Gemini came up with this. It works for me.