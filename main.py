import pyaudio
import numpy as np
import matplotlib.pyplot as plt


FORMAT = pyaudio.paFloat32
SAMPLE_RATE = 44100 # Hz
FRAMES_PER_BUFFER = 1024

def main():
	pyaudio_object = pyaudio.PyAudio()

	stream = pyaudio_object.open(
		format=FORMAT, 
		channels=1, 
		rate=SAMPLE_RATE, 
		input=True, 
		frames_per_buffer=FRAMES_PER_BUFFER
		)

	while True:
		# read the sound waves from the microphone
		data = stream.read(FRAMES_PER_BUFFER)		
		# create the array to be used to process the audio
		frames = np.frombuffer(data, dtype=np.float32) 

if __name__ == '__main__':
	main()