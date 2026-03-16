import aubio
import numpy as np


PITCH_TOLERANCE = 0.8 # minimum confidence for pitch candidates
HOP_SIZE = 512 # number of samples overlapping between two consecutive frames
WIN_SIZE = 4096

def detect_pitch(audio_array, sample_rate, buffer_size):
	print("detect_pitch called")

	# create pitch object
	pitch_o = aubio.pitch("yin", samplerate=sample_rate)

	x = audio_array
	# pad end of array with zeroes
	print(x.shape)
	pad_length = pitch_o.hop_size - x.shape[0] % pitch_o.hop_size
	x_padded = np.pad(x, (0, pad_length), 'constant', constant_values=0)
	# to reshape it in blocks of hop_size
	x_padded = x_padded.reshape(-1, pitch_o.hop_size)

	# input array should be of type aubio.float_type (defaults to float32)
	x_padded = x_padded.astype(aubio.float_type)

	for frame, i in zip(x_padded, range(len(x_padded))):
	    time_str = "%.3f" % (i * pitch_o.hop_size/float(sample_rate))
	    pitch_candidate = pitch_o(frame)[0]
	    print (time_str, "%.3f" % pitch_candidate)
