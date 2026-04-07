import sys
import time

import pyaudio
import numpy as np
import aubio
import pygame

from src.pitch_detection import detect_pitch
from src.game_logic import Game
from src.midi_parsing import MidiParser


FORMAT = pyaudio.paFloat32
SAMPLE_RATE = 44100 # Hz
FRAMES_PER_BUFFER = 2048 # number of frames per stream reading
SIZE = (1280, 720)

def main():
	"""This program takes a midi file as an output 
	and produces a rhythm game according to it"""

	if len(sys.argv) != 2:
		print("Usage: python main.py [midi file path]")
		return
	midi_file_name = sys.argv[1]

	# pygame initialization
	pygame.init()
	pygame.mixer.init(channels=1)
	pygame.font.init()
	font = pygame.font.SysFont("Comic Sans MS", 30)
	screen = pygame.display.set_mode(SIZE)
	running = True

	# pyaudio initialization
	pyaudio_object = pyaudio.PyAudio()
	stream = pyaudio_object.open(
		format=FORMAT, 
		channels=1, 
		rate=SAMPLE_RATE, 
		input=True, 
		frames_per_buffer=FRAMES_PER_BUFFER,
		input_device_index=None
		)

	midi_instructions = MidiParser(midi_file_name)
	game = Game(screen, midi_instructions, font)

	start_time = time.time()

	while running:
		# read the sound waves from the microphone
		data = stream.read(FRAMES_PER_BUFFER)		
		# create the array to be used to process the audio
		audio_array = np.frombuffer(data, dtype=np.float32)

		pitch = detect_pitch(audio_array, SAMPLE_RATE)

		game.update(pitch, time.time() - start_time)
		pygame.display.flip()

		for event in pygame.event.get():
			if event.type == pygame.QUIT: running = False

	pygame.quit()

if __name__ == '__main__':
	main()
