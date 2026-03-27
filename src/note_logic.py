class Note:
	"""Note objects represent every Note that should be played"""

	def __init__(self, note, start_time):
		"""Takes in the note (pitch) to be played and the time at which it 
		start. The time at which it ends is determined later through the midi 
		parsing."""

		self.note = note
		self.start_time = start_time
		self.end_time = None

	def get_error(self, mic_note):
		"""Calculates the error between this note and the mic note"""

		return mic_note - self.note
