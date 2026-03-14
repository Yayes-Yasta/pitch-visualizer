import pyaudio
import numpy as np
import matplotlib.pyplot as plt


FRAMES_PER_BUFFER = 1024

def main():
	pyaudio_object = pyaudio.PyAudio()

	stream = pyaudio_object.open(
		format=pyaudio.paFloat32, 
		channels=1, 
		rate=44100, 
		input=True, 
		frames_per_buffer=FRAMES_PER_BUFFER
		)

	while True:
		data = stream.read(FRAMES_PER_BUFFER)		
		# create the array to be used to process the audio
		frames = np.frombuffer(data, dtype=np.float32) 

if __name__ == '__main__':
	main()