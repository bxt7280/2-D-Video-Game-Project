import pygame
from enum import Enum

class Direction(Enum):
	UP = "UP"
	DOWN = "DOWN"
	LEFT = "LEFT"
	RIGHT = "RIGHT"
	UP_LEFT = "UP_LEFT"
	UP_RIGHT = "UP_RIGHT"
	DOWN_LEFT = "DOWN_LEFT"
	DOWN_RIGHT = "DOWN_RIGHT"
	NEUTRAL = "NEUTRAL"

# Automatically separates spritesheet into tiles and draws them on screen via index	
class SpriteSheet:
	def __init__(self, filename, cols, rows):
		self.sheet = pygame.image.load(filename)

		self.cols = cols
		self.rows = rows
		self.totalCellCount = cols * rows

		self.rect = self.sheet.get_rect()
		w = self.cellWidth = self.rect.width / cols
		h = self.cellHeight = self.rect.height / rows
		hw, hh = self.cellCenter = (w/2, h/2)

		self.cells = list([(index % cols * w, int(index / cols) * h, w, h) for index in range(self.totalCellCount)])

		self.handle = list([
			(0, 0), (-hw, 0), (-w, 0), 
			(0, -hh), (-hw, -hh), (-w, -hh),
			(0, -h), (-hw, -h), (-w, -h)])
		
	def draw(self, surface, cellIndex, x, y, handle = 0):
		surface.blit(self.sheet, (x + self.handle[handle][0] , y + self.handle[handle][1]), self.cells[cellIndex])