import pygame
import pygame.midi
from src.midi_parsing import MidiParser
from src.note_logic import Note


BACKGROUND_COLOR = (0, 0, 0)

BAR_COLOR = (255, 255, 255)

# marker for the microphone pitch
MIC_PITCH_COLOR = (0, 0, 255)
MIC_PITCH_RADIUS = 5

BASE_LINE_Y = 650
BASE_LINE_COLOR = (255, 255, 255)

PIXELS_PER_NOTE = 10
PIXELS_PER_SECOND = 100

class Game:
	"""This class is used to handle the rhythm game logic"""

	def __init__(self, screen, instructions, font):
		"""Takes in the  pygame display object and 
		the midi instructions to be displayed on the screen"""

		self.screen = screen
		self.font = font
		self.width, self.height = self.screen.get_size()

		self.instructions = instructions

		self.current_notes = set()
		self.midway_notes = {} # notes that extend beyond the screen

		self.midi_instructions = instructions
		self.next_instruction = next(instructions)

		self.pitch_error = 0
		self.done = False

	def update(self, mic_pitch, time):
		"""Handles the drawing of the entire display"""

		self.time = time

		self.screen.fill(BACKGROUND_COLOR)

		self.handle_notes(mic_pitch)
		self.draw_base_line()
		self.draw_mic_pitch(mic_pitch)
		self.show_error()

	def draw_mic_pitch(self, pitch):
		"""Shows the pitch from the microphone with a marker"""

		position = (pitch * PIXELS_PER_NOTE + MIC_PITCH_RADIUS, BASE_LINE_Y)
		color = MIC_PITCH_COLOR
		radius = MIC_PITCH_RADIUS
		pygame.draw.circle(self.screen, color, position, radius)

	def handle_notes(self, mic_note):
		"""Handles the logic of the notes"""

		time = self.time
		ahead_time = time + BASE_LINE_Y / PIXELS_PER_SECOND
		behind_time = time - (self.height - BASE_LINE_Y) / PIXELS_PER_SECOND

		self.pitch_error = float("inf")

		self.update_active_notes(ahead_time)

		# combines all finished and unfinished notes in one set
		# I'm sure this is inefficient but I will leave it be for now
		notes = self.current_notes.copy()
		for i in self.midway_notes:
			notes.add(self.midway_notes[i])

		for note in notes:
			start_time = note.start_time
			end_time = note.end_time

			self.draw_note_bar(note, ahead_time, start_time, end_time)


			# for currently playing notes
			if (start_time <= time and not end_time) or start_time <= time <= end_time:
				self.update_error(note, mic_note)
				note.play(self.midi_instructions, time)

			# if note has left the screen, remove it from the note set
			elif end_time and end_time < behind_time:
				self.current_notes.remove(note)

	def draw_note_bar(self, note, ahead_time, start_time, end_time):
		"""Draws the bar of a note"""

		x = note.note * PIXELS_PER_NOTE
		y = None
		width = PIXELS_PER_NOTE
		height = None
		
		# if note is finished
		if end_time:
			y = (ahead_time - end_time) * PIXELS_PER_SECOND
			height = (end_time - start_time) * PIXELS_PER_SECOND
		# if note is unfinished
		else:
			y = 0
			height = (ahead_time - start_time) * PIXELS_PER_SECOND

		rectangle = pygame.Rect(x, y, width, height)
		pygame.draw.rect(self.screen, BAR_COLOR, rectangle)

	def draw_base_line(self):
		"""Draws the line that represents the current time"""

		start_pos = (0, BASE_LINE_Y) 
		end_pos = (self.width, BASE_LINE_Y)
		pygame.draw.line(self.screen, BASE_LINE_COLOR, start_pos, end_pos)

	def update_active_notes(self, ahead_time):
		"""Fetches the next midi instructions if necessary 
		and adds notes to active_notes and midway_notes"""

		if self.done:
			return

		while ahead_time > self.next_instruction["time_since_start"]:
			instruction = self.next_instruction

			channel = instruction["channel"]
			instruction_time = instruction["time_since_start"]

			if instruction["type"] == "note_on":
				self.note_on(channel, instruction_time, instruction["note"])

			else:
				self.note_off(channel, instruction_time)

			# get the next instruction or stop if the song has ended
			try:
				self.next_instruction = next(self.instructions)

			except StopIteration:
				self.done = True
				print("End reached")
				break

	def note_on(self, channel, instruction_time, note):
		"""Handles the start of a note 
		(when it gets added to the screen but is not yet played)"""

		# if the same channel is already playing a note, stop that note
		if self.midway_notes.get(channel): 
			self.note_off(channel, instruction_time)

		note_object = Note(note, instruction_time)

		# adds the note to the unfinished notes
		self.midway_notes[channel] = note_object

	def note_off(self, channel, instruction_time):
		"""Handles the stop of a note"""

		"""If multiple notes are played per channel, there might be an attempt 
		to turn off a note that was already forced off by this program.
		If that happens, ignore the note_off instruction"""
		if not self.midway_notes.get(channel):
			return

		note = self.midway_notes[channel]

		# adds note to the finished notes
		note.end_time = instruction_time
		self.current_notes.add(note)

		# removes note from the unfinished notes
		del self.midway_notes[channel]

	def update_error(self, note, mic_note):
		"""Updates the pitch error"""

		error = note.get_error(mic_note)

		if abs(error) < abs(self.pitch_error):
			self.pitch_error = error

	def show_error(self):
		"""Displays the pitch error as text"""

		error = self.pitch_error
		
		color = (255, 0, 0) if abs(error) > 0.5 else (0, 255, 0)

		feedback = "+" if error > 0 else ""
		feedback += str(error)

		text = self.font.render(feedback, False, color)

		self.screen.blit(text, (100, 100))

	def play_note(self):
		pass