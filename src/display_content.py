BACKGROUND_COLOR = (0, 0, 0)

class Display:
	def __init__(self, screen):
		self.screen = screen

	def draw(self, mic_pitch):
		"""Handles the drawing of the entire display"""

		self.screen.fill(BACKGROUND_COLOR)

	def draw_mic_pitch(self):
		pass

	def draw_expected_pitch_bars(self):
		pass

	def draw_note_references(self):
		pass