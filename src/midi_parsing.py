import mido


class MidiParser:
	"""This class is an iterator that reads a midi file 
	and calculates the time at which instructions occur"""

	def __init__(self, file_path):
		"""Prepares an array of all raw instructions parsed through mido."""

		messages = []
		file = mido.MidiFile(file_path)
		for msg in file:
			messages.append(msg)

		self.instructions = messages # queue representing all midi instructions
		self.time = 0 # time elapsed since start of the music

	def __iter__(self):
		"""Returns an iterator object."""

		return self

	def __next__(self):
		"""Returns needed information about the next instruction"""

		instruction = self.instructions.pop(0)

		if instruction.type == "end_of_track":
			raise StopIteration

		# in case the instruction is not related to the played notes
		while instruction.type != "note_on" and instruction.type != "note_off":
			if instruction.type == "end_of_track":
				raise StopIteration

			instruction = self.instructions.pop(0)

		self.add_time(instruction.time)

		return {
			"type": instruction.type, 
			"channel": instruction.channel, 
			"note": instruction.note, 
			"time_since_start": self.time
		}

	def add_time(self, time):
		"""adds time to the total time elapsed"""

		self.time += time

	def look_for_end(self, note: int, current_time) -> int:
		"""Returns the next note_off instruction of a note that will happen"""
		
		instructions = self.instructions

		end_time = current_time

		for instruction in instructions:
			end_time += instruction.time

			if instruction.type == "note_off" and instruction.note == note:
				return end_time 

		print("Error: Failed to find the end of the note")
		return None
