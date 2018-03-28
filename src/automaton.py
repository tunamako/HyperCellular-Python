from PyQt5.QtGui import QColor

import random
import math

class Automaton:
	def clicked(self, aTile):
		for i, color in enumerate(self.states):
			if aTile.color == color:
				aTile.nextColor = self.states[i+1 if i+1 < len(self.states) else 0]
				return
		aTile.nextColor = self.states[0]

	def randomize(self, aTileList):
		for tile in aTileList:
			tile.nextColor = random.choice(self.states)

	def fill(self, aTileList):
		for tile in aTileList:
			tile.nextColor = self.states[0]


class WireWorld(Automaton):
	def __init__(self):
		self.states = [
			QColor(0, 0, 0, 255), 		#empty
			QColor(230, 230, 0, 255),	#conductor
			QColor(0, 0, 255, 255),		#head
			QColor(255, 0, 0, 255),		#tail
		]

	def nextGeneration(self, aModel):
		for tile in aModel.tiles:
			if tile.color == self.states[2]:
				tile.nextColor = self.states[3]
			elif tile.color == self.states[3]:
				tile.nextColor = self.states[1]
			elif tile.color == self.states[1]:
				headcount = 0
				for n in tile.neighbors:
					if n.color == self.states[2]: 
						headcount += 1
				if headcount == 1:
					tile.nextColor = self.states[2]

class Life(Automaton):
	def __init__(self):
		self.states = [
			QColor(255, 255, 255, 255), #off
			QColor(0, 0, 0, 255),		#on
		]

	def nextGeneration(self, aModel):
		p = aModel.sideCount

		for tile in aModel.tiles:
			livecount = 0
			for neighbor in tile.neighbors:
				if neighbor.color == self.states[1]: livecount += 1

			if livecount < p//2 and tile.color == self.states[1]:
				tile.nextColor = self.states[0]
			if livecount > 3 and tile.color == self.states[1]:
				tile.nextColor = self.states[0]
			if livecount == 3 and tile.color == self.states[0]:
				tile.nextColor = self.states[1]
