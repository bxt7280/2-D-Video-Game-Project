import pygame
from Sprites import Border, Slime, MainCharacter
from Map import Map
from Util import camera, Direction

class View():
	def __init__(self, model, screen, screenSize):
		# Determine screen size
		self.screen = screen		
		self.screen_size = screenSize
		self.model = model
		# self.currentMap = Map("./Maps/testMap/testMap.tmx", self.screen)
		# self.currentMapSize = (800, 800)		
		self.currentMap = Map("./Maps/testMapLarge/testMapLarge.tmx", self.screen)
		self.currentMapSize = (2400, 2400)
		self.model.currentMapSize = self.currentMapSize 
		self.background = pygame.image.load("./Images/forestBackground.png")

		# User text input
		self.displayTextSpriteSelect = False
		self.base_font = pygame.font.Font(None, 32)
		self.user_text = ""

	def update(self):   
		#print(self.model.mainCharacter.x, self.model.mainCharacter.y)
		#print(self.camera.x, self.camera.y)
		self.screen.fill("darkblue") 
		#self.screen.fill([0,200,100])
		#self.screen.blit(self.background, (0 - camera.x, 0 - camera.y))
		
		self.drawMap()
		
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
				if isinstance(sprite, MainCharacter):
					pygame.draw.rect(self.screen, "red", (sprite.x + sprite.hitboxLeft - camera.x, 
								sprite.y + sprite.hitboxTop - camera.y, sprite.w + sprite.hitboxW, sprite.h + sprite.hitboxH), 1)
				
				if isinstance(sprite, Slime):
					pygame.draw.circle(self.screen, "red", (sprite.hitboxCenter[0] - camera.x, sprite.hitboxCenter[1] - camera.y), sprite.radius, 1)
					#pygame.draw.line(self.screen, "black", (sprite.hitboxCenter[0] - camera.x, sprite.hitboxCenter[1] - camera.y) , 
					#				(self.model.mainCharacter.distVector.x - camera.x, self.model.mainCharacter.distVector.y - camera.y))
				
				pygame.draw.rect(self.screen, "black", (sprite.x - camera.x , sprite.y - camera.y, 
				sprite.w,sprite.h ), 1)
				

	def drawHealthBar(self):
		playerHP = round(self.model.mainCharacter.hp/self.model.mainCharacter.maxHp * 100, 2)	
		playerHpSurface = self.base_font.render("Life: " + str(playerHP) + "%", True, (255,255,255))
		self.screen.blit(playerHpSurface,(self.screen_size[0] - 350, 0))

		healthBar = pygame.image.load("./Images\HPBarBoldFull_Test1.png").convert_alpha()
		healthBarRect = healthBar.get_rect()

		#self.screen.blit(healthBar, (0, 0))
		#pygame.draw.rect(self.screen, "black", healthBarRect, 1)
		healthBarRect.x = 22
		healthBarRect.y = 149
		#healthBarRect.w = 340
		healthBarRect.w = 340 * (playerHP/100)
		healthBarRect.h = 54

		#pygame.draw.rect(self.screen, "red", healthBarRect, 1)

		self.screen.blit(healthBar, (self.screen_size[0] - 350, self.screen_size[1] - 778), healthBarRect)

		#pygame.draw.rect(self.screen, "white", (self.screen_size[0] - 200, self.screen_size[1] - 778, 200, 36), 2)
		#pygame.draw.rect(self.screen, "black", (self.screen_size[0] - 200 + 2, self.screen_size[1] - 778 + 2, 196, 32), 2)	
		#pygame.draw.rect(self.screen, "#CC0000", (self.screen_size[0] - 200 + 4, self.screen_size[1] - 778 + 4, 192 * (playerHP/100), 28))
		# pygame.draw.rect(self.screen, "#990000", (self.screen_size[0] - 200 + 4, self.screen_size[1] - 778 + 4, 192 * (playerHP/100), 3))
		# pygame.draw.rect(self.screen, "white", (self.screen_size[0] - 200 + 4, self.screen_size[1] - 778 + 12, 192 * (playerHP/100), 6))
				
		#pygame.draw.rect(self.screen, "#CC0000", (self.screen_size[0] - 200 + 2, self.screen_size[1] - 778 + 2, 196 * (playerHP/100), 32))

	# Infinite scrolling map
	def drawMap(self):
		# Center image
		self.currentMap.drawWithOffset(-camera.x, -camera.y)

		# Moving Right
		if camera.x + camera.width > self.currentMapSize[0]:
			#self.currentMap.drawWithOffset(self.currentMapSize[0] - camera.x, -camera.y)
			#print("right painted")
			pass
		# Moving Left
		if camera.x < 0:
			#self.currentMap.drawWithOffset(-self.currentMapSize[0] + -camera.x, -camera.y)
			#print("left painted")
			pass	
		# Moving Up
		if camera.y < 0:
			#self.currentMap.drawWithOffset(-camera.x, -self.currentMapSize[1] + -camera.y)
			#print("up painted")
			pass
		# Moving Down
		if camera.y + camera.height > self.currentMapSize[1]:
			#self.currentMap.drawWithOffset(-camera.x, self.currentMapSize[1] -camera.y)
			#print("down painted")
			pass

		# Diagonals				
		# Right-Up
		if camera.x + camera.width > self.currentMapSize[0] and camera.y < 0:
			#self.currentMap.drawWithOffset(self.currentMapSize[0] - camera.x, -self.currentMapSize[1] + -camera.y)	
			#print("right up painted")
			pass
		# Right-Down
		if camera.x + camera.width > self.currentMapSize[0] and camera.y + camera.height > self.currentMapSize[1]:
			#self.currentMap.drawWithOffset(self.currentMapSize[0] - camera.x, self.currentMapSize[1] -camera.y)
			#print("right down painted")
			pass 	
		# Left-Up
		if camera.x < 0 and camera.y < 0:
			#self.currentMap.drawWithOffset(-self.currentMapSize[0] + -camera.x, -self.currentMapSize[1] + -camera.y)
			#print("left up painted")
			pass
		# Left-Down
		if camera.x < 0 and camera.y + camera.height > self.currentMapSize[1]:
			#self.currentMap.drawWithOffset(-self.currentMapSize[0] + -camera.x, self.currentMapSize[1] -camera.y)
			#print("left down painted")
			pass
