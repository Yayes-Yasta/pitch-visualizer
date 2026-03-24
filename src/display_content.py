import pygame


BACKGROUND_COLOR = (0, 0, 0)

# marker for the microphone pitch
MIC_PITCH_COLOR = (0, 0, 255)
MIC_PITCH_RADIUS = 5

BASE_LINE_Y = 650

PIXELS_PER_NOTE = 10

class Display:
	"""This class is used to handle displaying to the window"""

	def __init__(self, screen):
		"""Takes in the  pygame display object"""

		self.screen = screen

	def draw(self, mic_pitch):
		"""Handles the drawing of the entire display"""

		self.screen.fill(BACKGROUND_COLOR)

		self.draw_mic_pitch(mic_pitch)

	def draw_mic_pitch(self, pitch):
		"""Shows the pitch from the microphone with a marker"""

		position = (pitch * PIXELS_PER_NOTE, BASE_LINE_Y)
		color = MIC_PITCH_COLOR
		radius = MIC_PITCH_RADIUS
		pygame.draw.circle(self.screen, color, position, radius)

	def draw_expected_pitch_bars(self):
		pass

	def draw_note_references(self):
		pass