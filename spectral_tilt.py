#!/usr/bin/env python3

import math
import parselmouth
import statsmodels.api as sm

from parselmouth.praat import call

voice_id = "test_voices/f4047_ah.wav"

sound= parselmouth.Sound(voice_id)  # read the sound
window_length_in_millisecs = 32  # allow advanced user to select between 2^5 and 2^12 ms, changing exponent
window_length = window_length_in_millisecs / 1000

# Compute begin and end times, set window
end = call(sound, "Get end time")
midpoint = end / 2

begintime = midpoint - (window_length / 2)
endtime = midpoint + (window_length / 2)
part_to_measure = sound.extract_part(begintime , endtime)
# part_to_measure.save("part_of_sound.wav", "WAV") # option this for advanced users
spectrum = part_to_measure.to_spectrum()
total_bins = spectrum.get_number_of_bins()
dBValue = []
bins = []

# convert spectral values to dB
for i in range(2, total_bins):
    bin_number = (i - 1)
    currentX = bin_number
    realValue = spectrum.get_real_value_in_bin(i)
    imagValue = spectrum.get_imaginary_value_in_bin(i)
    sumOfSquares = realValue ** 2 + imagValue ** 2
    rmsPower = sumOfSquares ** 0.5
    dBValue.append(20 * (math.log10(rmsPower / 0.0002)))
    bins.append(bin_number)

# find maximum dB value, for rescaling purposes
maxdB = max(dBValue)
mindB = min(dBValue)
rangedB = maxdB - mindB

# stretch the spectrum to a normalized range
# that matches the number of frequency values
scalingConstant = ((total_bins - 1) / rangedB)
dBValue = [(value + abs(mindB))*scalingConstant for value in dBValue]

# find slope of regression
model = sm.OLS(dBValue,bins)
results = model.fit()
spectral_tilt = results.params[0]
print(spectral_tilt)