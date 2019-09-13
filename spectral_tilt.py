#!/usr/bin/env python3

import math
import parselmouth
import statistics


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
part_to_measure = sound.extract_part(begintime, endtime)
part_to_measure.save("part_of_sound.wav", "WAV") # option this for advanced users
spectrum = part_to_measure.to_spectrum()
total_bins = spectrum.get_number_of_bins()
dBValue = []
bins = []

# convert spectral values to dB
for bin in range(total_bins):
    bin_number = bin + 1
    realValue = spectrum.get_real_value_in_bin(bin_number)
    imagValue = spectrum.get_imaginary_value_in_bin(bin_number)
    rmsPower = math.sqrt((realValue ** 2) + (imagValue ** 2))
    db = 20 * (math.log10(rmsPower / 0.0002))
    dBValue.append(db)
    bin_number += 1
    bins.append(bin)

# find maximum dB value, for rescaling purposes
maxdB = max(dBValue)
mindB = min(dBValue)  # this is wrong in Owren's script, where mindB = 0
rangedB = maxdB - mindB

# stretch the spectrum to a normalized range that matches the number of frequency values
scalingConstant = ((total_bins - 1) / rangedB)
scaled_dB_values = []
for value in dBValue:
    scaled_dBvalue = value + abs(mindB)
    scaled_dBvalue *= scalingConstant
    scaled_dB_values.append(scaled_dBvalue)

# find slope
sumXX = 0
sumXY = 0
sumX = sum(bins)
sumY = sum(scaled_dB_values)

for bin in bins:
    currentX = bin
    sumXX += currentX ** 2
    sumXY += currentX * scaled_dB_values[bin]

meanX = statistics.mean(bins)
meanY = statistics.mean(scaled_dB_values)
sXX = (sumXX - ((sumX * sumX) / len(bins)))
sXY = (sumXY - ((sumX * sumY) / len(bins)))
spectral_tilt = (sXY / sXX)
print("spectral_tilt", spectral_tilt)
