# Ben Thiele - Battle Arena
import pygame
from Model import Model
from Controller import Controller
from View import View

class Game():
	def __init__(self):
		print("Use the arrow keys to move. Press Esc to quit.")
		pygame.init()

		self.clock = pygame.time.Clock()

		self.m = Model()
		self.v = View(self.m)
		self.c = Controller(self.m, self.v)
		
	def run(self):
		while self.c.keepGoing:		
			self.c.update()
			self.m.update()
			self.v.update()
			self.clock.tick(30)
			#print(clock.get_fps())
		print("Goodbye")

game = Game()
game.run()


