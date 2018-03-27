from PyQt5.QtGui import QColor

import random

class Automaton:
	def __init__(self):
		self.states = [
			QColor(255, 255, 255, 255), #off
			QColor(0, 0, 0, 255),		#on
		]
		self.ruleset = ""

	def nextGeneration(self, aTileList):
		for tile in aTileList:
			livecount = 0
			for neighbor in tile.neighbors:
				if neighbor.color == self.states[1]:
					livecount += 1

			if livecount > 2 and tile.color == self.states[0]:
				tile.nextColor = self.states[1]
			elif livecount == 5 and tile.color == self.states[1]:
				tile.nextColor = self.states[0]

	def randomize(self, aTileList):
		for tile in aTileList:
			tile.nextColor = random.choice(self.states)