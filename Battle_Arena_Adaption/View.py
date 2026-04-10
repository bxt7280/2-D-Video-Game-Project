import pygame
from Sprites import Border, Slime

class View():
	def __init__(self, model):
		# Determine screen size
		screen_size = (800, 800)
		self.screen = pygame.display.set_mode(screen_size, 32)
		self.model = model
		# Pass screen size into instance of model
		self.model.setScreenSize(screen_size)
		self.background = pygame.image.load('./Images/forestBackground.png')

	def update(self):    
		self.screen.fill([0,200,100])
		self.screen.blit(self.background, (0, 0))
		self.drawSprites()	
		pygame.display.flip()

	def drawSprites(self):
		for sprite in self.model.sprites:
			if not isinstance(sprite, Border):
				sprite.currentSpriteSheet.draw(self.screen, sprite.currentSpriteCellIndex, sprite.x, sprite.y)
			if self.model.hitBoxModeOn:
				pygame.draw.rect(self.screen, "red", (sprite.x + sprite.hitboxLeft, sprite.y + sprite.hitboxTop , 
								 sprite.w + sprite.hitboxW, sprite.h + sprite.hitboxH), 1)
				# pygame.draw.rect(self.screen, "black", (sprite.x , sprite.y  , 
				#  				 sprite.w,sprite.h ), 1)
				
				if isinstance(sprite, Slime):
					pygame.draw.line(self.screen, "black", sprite.distVector, self.model.mainCharacter.distVector)
					#print(sprite.distVector.distance_to(self.model.mainCharacter.distVector))