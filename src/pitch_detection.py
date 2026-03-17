import aubio
import numpy as np


PITCH_TOLERANCE = 0.7 # minimum confidence for pitch candidates
HOP_SIZE = 512 # number of samples for each pitch calculation

def detect_pitch(audio_array, sample_rate):
	"""Estimates and returns the pitch of a raw audio_array"""

	# create pitch object
	pitch_o = aubio.pitch("yin", hop_size=HOP_SIZE, samplerate=sample_rate)
	pitch_o.set_tolerance(PITCH_TOLERANCE)
	pitch_o.set_unit("midi")

	# pad end of array with zeroes to make the length a multiple of hop_size
	array_length = audio_array.shape[0]
	pad_length = HOP_SIZE - array_length % HOP_SIZE
	padded_array = np.pad(audio_array, (0, pad_length), constant_values=0)

	# reshape it into blocks of hop_size
	frame_array = padded_array.reshape(-1, pitch_o.hop_size)
	frame_count = frame_array.shape[0]

	# collect all pitch calculations
	pitch_profile = np.empty(frame_count) 

	for frame, i in zip(frame_array, range(frame_count)):
	    pitch_profile[i] = pitch_o(frame) # calculate the pitch

	return np.median(pitch_profile)