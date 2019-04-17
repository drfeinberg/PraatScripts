import parselmouth
from parselmouth.praat import call
import glob
import os

output_directory = '/output/'
maximum_period = 0.02
mean_period = 0.01


for wave_file in glob.glob("/home/david/work/stimuli/All_Vowels/to_separate/*.wav"):
    i = 0
    name = os.path.splitext((os.path.basename(wave_file)))[0]
    sound = parselmouth.Sound(wave_file)
    pitch = sound.to_pitch_ac(pitch_floor = 50, pitch_ceiling = 600)
    PointProcess = call([sound, pitch], "To PointProcess (cc)")
    textgrid = call(PointProcess, "To TextGrid (vuv)", maximum_period, mean_period)
    newsounds = call([sound, textgrid], "Extract all intervals", 1, False)
    for sound in newsounds:
        i += 1
        newname = output_directory + '/' + name + '_' + str(i) + ".wav"
        call(sound, 'Write to WAV file', newname)
