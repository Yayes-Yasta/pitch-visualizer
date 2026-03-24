import pyaudio
import numpy as np
from src.pitch_detection import detect_pitch
import aubio
import pygame


FORMAT = pyaudio.paFloat32
SAMPLE_RATE = 44100 # Hz
FRAMES_PER_BUFFER = 2048 # number of frames per stream reading

def main():
	# pygame initialization
	pygame.init()
	screen = pygame.display.set_mode((1280, 720))
	running = True

	# pyaudio initialization
	pyaudio_object = pyaudio.PyAudio()
	stream = pyaudio_object.open(
		format=FORMAT, 
		channels=1, 
		rate=SAMPLE_RATE, 
		input=True, 
		frames_per_buffer=FRAMES_PER_BUFFER
		)

	while running:
		# read the sound waves from the microphone
		data = stream.read(FRAMES_PER_BUFFER)		
		# create the array to be used to process the audio
		audio_array = np.frombuffer(data, dtype=np.float32)

		detect_pitch(audio_array, SAMPLE_RATE)

		pygame.display.flip()

		for event in pygame.event.get():
			if event.type == pygame.QUIT():
				running = False

if __name__ == '__main__':
	main()