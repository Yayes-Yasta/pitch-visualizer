import pyaudio


FRAMES_PER_BUFFER = 1024

def main():
	pyaudio_object = pyaudio.PyAudio()

	pyaudio_object.open(
		format=pyaudio.paFloat32, 
		channel=1, 
		rate=44100, 
		input=True, 
		frames_per_buffer=FRAMES_PER_BUFFER
		)

	while True:
		pass

if __name__ == '__main__':
	main()