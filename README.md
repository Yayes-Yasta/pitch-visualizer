# pitch-visualizer

The program is a rhythm game that uses real-time microphone input and compares the pitch to notes from a MIDI file. It is built in Python, mainly using PyAudio, aubio and pygame. 

## Usage
```
python main.py [midi_file_name]
```
Example:
```
python main.py demo.midi
```

## Demonstration
![Demo Gif](https://github.com/Yayes-Yasta/pitch-visualizer/blob/main/demo.gif?raw=true)

## Features
- Real-time pitch detection of microphone input
- Any monophonic MIDI file can be used
- Visual feedback like in a rhythm game
- Playback of notes that should be played

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

## Main tools
- Python
- PyAudio (For microphone input)
- aubio (For pitch detection calculations)
- pygame (For the visual game window)
- mido (For parsing MIDI files)

## Limitations
It should be able to run with any MIDI file but if it plays multiple notes belonging to the same channel at the same time, it will ignore one of the notes. 
If multiple notes are played at the same time, a pitch cannot be confidently detected. This means that this program does not work well with chords but might be helpful for singing
