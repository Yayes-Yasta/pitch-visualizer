import pygame
import numpy as np


PLAYBACK_ENABLED = True

class Note:
	"""Note objects represent every Note that should be played"""

	def __init__(self, note, start_time):
		"""Takes in the note (pitch) to be played and the time at which it 
		start. The time at which it ends is determined later through the midi 
		parsing."""

		self.note: int = note
		self.start_time = start_time
		self.end_time = None

		self.playing = False

	def get_error(self, mic_note):
		"""Calculates the error between this note and the mic note"""

		return mic_note - self.note

	def play(self, parser, time):
		"""Plays the note as audio"""

		if not PLAYBACK_ENABLED:
			return

		if self.playing:
			return

		self.playing = True

		note: int = self.note

		# find duration
		start_time = self.start_time
		end_time = self.end_time
		if not end_time:
			end_time = parser.look_for_end(note, time)

		duration = end_time - start_time # in seconds

		# set up sine wave for sound of note
		bitrate = 44100 # Hz
		time_values = np.arange(int(duration * bitrate)) / bitrate	

		amplitude = 32767
		frequency = 440 * (2 ** ((note - 69) / 12)) # midi to Hz formula

		signal = np.sin(2 * np.pi * frequency * time_values)
		
		# ease the starts and ends of each note by making start and end quiet
		attack = min(int(0.01 * bitrate), len(signal) // 2)
		release = min(int(0.01 * bitrate), len(signal) // 2)
		envelope = np.ones_like(signal)
		envelope[:attack] = np.linspace(0, 1, attack)
		envelope[-release:] = np.linspace(1, 0, release)

		signal *= envelope

		signal = signal.reshape(int(duration * bitrate), 1)
		signal = np.repeat(signal, 2, axis=1)

		signal = np.int16(signal * amplitude)

		sound = pygame.sndarray.make_sound(signal)
		sound.play()

