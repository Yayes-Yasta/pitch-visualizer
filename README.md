# pitch-visualizer
This program takes in a midi file and compares the played notes to the microphone input to produce a rhythm game. This only works when one note is played at a time, which makes it useful for practicing singing but does not work with chords.

## Usage
```
python main.py [midi_file_name]
```
Example:
```
python main.py demo.midi
```

The program should be able to run with any midi file but if it plays multiple notes belonging to the same channel at the same time, it will ignore one of the notes. 

## Demonstration
![Demo Gif](https://github.com/Yayes-Yasta/pitch-visualizer/blob/main/demo.gif?raw=true)

## Installation
### Prerequisites
- Python (ideally 3.13 or older, otherwise issues with Pyaudio might arise)
- gcc (For PyAudio)
### Installing Python Dependencies
Run this command:
```
pip install -r requirements.txt
```
This could not work on the first try because PyAudio and Aubio might act up. If this fails, possible fixes are:
- Change the Python version (3.13 or older worked for me)
- Read the error message, you might need to install something that is missing
