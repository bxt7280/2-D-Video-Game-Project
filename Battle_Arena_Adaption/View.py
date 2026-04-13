import pygame
from Sprites import MainCharacter, Border, Slime

class View():
	def __init__(self, model):
		# Determine screen size
		self.screen_size = (800, 800)
		self.screen = pygame.display.set_mode(self.screen_size, 32)
		self.model = model
		# Pass screen size into instance of model
		self.model.setScreenSize(self.screen_size)
		self.background = pygame.image.load("./Images/forestBackground.png")

		# User text input
		self.displayTextSpriteSelect = False
		self.base_font = pygame.font.Font(None, 32)
		self.user_text = ""

		# For red pulsating effect on mainCharacter
		self.currentAlpha = 255
		self.alphaDirectionSwitch = True

	def update(self):    
		self.screen.fill([0,200,100])
		self.screen.blit(self.background, (0, 0))
		self.drawSprites()
		if self.displayTextSpriteSelect:	
			text_surface = self.base_font.render("Sprite Type: " + self.user_text, True, (255,255,255))
			self.screen.blit(text_surface,(0,0))
		
		playerHP = str(round(self.model.mainCharacter.hp/self.model.mainCharacter.maxHp * 100, 2))	
		playerHpSurface = self.base_font.render("HP: " + playerHP, True, (255,255,255))
		self.screen.blit(playerHpSurface,(700, 0))
		pygame.display.flip()

	def drawSprites(self):
		for sprite in self.model.sprites:
			if not isinstance(sprite, Border):
				if isinstance(sprite, MainCharacter) and self.model.mainCharacter.pulsateRed == True :
					self.assignCurrentAlpha()
					sprite.currentSpriteSheet.drawWithAlpha(self.screen, sprite.currentSpriteCellIndex, sprite.x, sprite.y, 0, self.currentAlpha)
				else:
					sprite.currentSpriteSheet.draw(self.screen, sprite.currentSpriteCellIndex, sprite.x, sprite.y)
				
				if self.model.mainCharacter.pulsateRed == False:
					self.currentAlpha = 255

			if self.model.hitBoxModeOn:
				pygame.draw.rect(self.screen, "red", (sprite.x + sprite.hitboxLeft, sprite.y + sprite.hitboxTop , 
								 sprite.w + sprite.hitboxW, sprite.h + sprite.hitboxH), 1)
				# pygame.draw.rect(self.screen, "black", (sprite.x , sprite.y  , 
				#  				 sprite.w,sprite.h ), 1)
				
				if isinstance(sprite, Slime):
					pygame.draw.line(self.screen, "black", sprite.distVector, self.model.mainCharacter.distVector)
					#print(sprite.distVector.distance_to(self.model.mainCharacter.distVector))

	def assignCurrentAlpha(self):
		if self.alphaDirectionSwitch == True:
			if self.currentAlpha <= 155:
				self.alphaDirectionSwitch = False
			else:
				self.currentAlpha -= 10
		else:
			if self.currentAlpha >= 255:
				self.alphaDirectionSwitch = True
			else:
				self.currentAlpha += 10