# Ben Thiele - Battle Arena
import pygame
from Model import Model
from Controller import Controller
from View import View
from Util import camera

class Game():
	def __init__(self):
		print("Use the arrow keys to move. Press Esc to quit.")
		pygame.init()
		self.screen_size = (800, 800)
		self.screen = pygame.display.set_mode(self.screen_size, 32)
		camera.width = self.screen_size[0]
		camera.height = self.screen_size[1]
		self.clock = pygame.time.Clock()

		self.m = Model(self.screen, self.screen_size)
		self.v = View(self.m, self.screen, self.screen_size)
		self.c = Controller(self.m, self.v)
		
	def run(self):
		while self.c.keepGoing:		
			self.c.update()
			self.m.update()
			self.v.update()
			self.clock.tick(30)
			print(self.clock.get_fps())
			
		print("Goodbye")

game = Game()
game.run()


