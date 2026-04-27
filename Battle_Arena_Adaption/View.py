import pygame
from Sprites import Border, Slime

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
		#self.screen.fill("black") 
		#self.screen.fill([0,200,100])
		self.screen.blit(self.background, (0, 0))
		self.drawSprites()
		if self.displayTextSpriteSelect:	
			text_surface = self.base_font.render("Sprite Type: " + self.user_text, True, (255,255,255))
			self.screen.blit(text_surface,(0,0))
		
		self.drawHealthBar()

		pygame.display.flip()

	def drawSprites(self):
		for sprite in self.model.sprites:
			if not isinstance(sprite, Border):
				sprite.draw(self.screen)
	
			if self.model.hitBoxModeOn:
				pygame.draw.rect(self.screen, "red", (sprite.x + sprite.hitboxLeft, sprite.y + sprite.hitboxTop , 
								 sprite.w + sprite.hitboxW, sprite.h + sprite.hitboxH), 1)
				pygame.draw.rect(self.screen, "black", (sprite.x , sprite.y  , 
				  				 sprite.w,sprite.h ), 1)
				
				if isinstance(sprite, Slime):
					pygame.draw.line(self.screen, "black", sprite.distVector, self.model.mainCharacter.distVector)
					#print(sprite.distVector.distance_to(self.model.mainCharacter.distVector))

	def drawHealthBar(self):
		playerHP = round(self.model.mainCharacter.hp/self.model.mainCharacter.maxHp * 100, 2)	
		playerHpSurface = self.base_font.render("Life: " + str(playerHP) + "%", True, (255,255,255))
		self.screen.blit(playerHpSurface,(self.screen_size[0] - 200, 0))

		pygame.draw.rect(self.screen, "white", (self.screen_size[0] - 200, self.screen_size[1] - 778, 200, 36), 2)
		pygame.draw.rect(self.screen, "black", (self.screen_size[0] - 200 + 2, self.screen_size[1] - 778 + 2, 196, 32), 2)	
		pygame.draw.rect(self.screen, "#CC0000", (self.screen_size[0] - 200 + 4, self.screen_size[1] - 778 + 4, 192 * (playerHP/100), 28))
		# pygame.draw.rect(self.screen, "#990000", (self.screen_size[0] - 200 + 4, self.screen_size[1] - 778 + 4, 192 * (playerHP/100), 3))
		# pygame.draw.rect(self.screen, "white", (self.screen_size[0] - 200 + 4, self.screen_size[1] - 778 + 12, 192 * (playerHP/100), 6))
				
		#pygame.draw.rect(self.screen, "#CC0000", (self.screen_size[0] - 200 + 2, self.screen_size[1] - 778 + 2, 196 * (playerHP/100), 32))

		
		