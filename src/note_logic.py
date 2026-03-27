class Note:
	def __init__(self, note, start_time):
		self.note = note
		self.start_time = start_time
		self.end_time = None

	def get_error(self, mic_note):
		return mic_note - self.note
