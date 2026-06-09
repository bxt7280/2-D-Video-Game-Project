import pygame
from Sprites import Obstacle, Slime, MainCharacter
from Map import Map
from Util import camera

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
		self.model.obstacles = self.currentMap.extractObstacles()
		self.background = pygame.image.load("./Images/forestBackground.png")

		# User text input
		self.displayTextSpriteSelect = False
		self.base_font = pygame.font.Font(None, 32)
		self.user_text = ""

	def update(self):   
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
			if not isinstance(sprite, Obstacle):
				sprite.draw(self.screen)
	
			if self.model.hitBoxModeOn:
				if isinstance(sprite, MainCharacter):
					pygame.draw.rect(self.screen, "red", (sprite.x + sprite.hitboxLeft - camera.x, 
								sprite.y + sprite.hitboxTop - camera.y, sprite.w + sprite.hitboxW, sprite.h + sprite.hitboxH), 1)
				
				if isinstance(sprite, Slime):
					# Follows same pattern as drawMap method 	
					# Center Image
					pygame.draw.circle(self.screen, "red", (sprite.hitboxCenter[0] - camera.x, sprite.hitboxCenter[1] - camera.y), sprite.radius, 1)
					
					# Moving Right
					if camera.x + camera.width > self.currentMapSize[0]:
						pygame.draw.circle(self.screen, "red", (sprite.hitboxCenter[0] + self.currentMapSize[0] - camera.x, sprite.hitboxCenter[1] - camera.y), sprite.radius, 1)			
					# Moving Left
					if camera.x < 0 + sprite.w: # added width of sprite so it doesn't disappear from screen when moving left
						pygame.draw.circle(self.screen, "red", (sprite.hitboxCenter[0] - self.currentMapSize[0] + -camera.x, sprite.hitboxCenter[1] - camera.y), sprite.radius, 1)									
					# Moving Up
					if camera.y < 0 + sprite.h:
						pygame.draw.circle(self.screen, "red", (sprite.hitboxCenter[0] - camera.x, sprite.hitboxCenter[1] - self.currentMapSize[1] - camera.y), sprite.radius, 1)
					# Moving Down
					if camera.y + camera.height > self.currentMapSize[1]:
						pygame.draw.circle(self.screen, "red", (sprite.hitboxCenter[0] - camera.x, sprite.hitboxCenter[1] + self.currentMapSize[1] - camera.y), sprite.radius, 1)

					# Diagonals
					# Right-Up
					if camera.x + camera.width > self.currentMapSize[0] and camera.y < 0 + sprite.h:
						pygame.draw.circle(self.screen, "red", (sprite.hitboxCenter[0] + self.currentMapSize[0] - camera.x, sprite.hitboxCenter[1] - self.currentMapSize[1] - camera.y), sprite.radius, 1)	
					# Right-Down
					if camera.x + camera.width > self.currentMapSize[0] and camera.y + camera.height > self.currentMapSize[1]:
						pygame.draw.circle(self.screen, "red", (sprite.hitboxCenter[0] + self.currentMapSize[0] - camera.x, sprite.hitboxCenter[1] + self.currentMapSize[1] - camera.y), sprite.radius, 1)			
					# Left-Up
					if camera.x < 0 + sprite.w and camera.y < 0 + sprite.h:
						pygame.draw.circle(self.screen, "red", (sprite.hitboxCenter[0] - self.currentMapSize[0] + -camera.x, sprite.hitboxCenter[1] - self.currentMapSize[1] - camera.y), sprite.radius, 1)	
					# Left-Down
					if camera.x < 0 + sprite.w and camera.y + camera.height > self.currentMapSize[1]:
						pygame.draw.circle(self.screen, "red", (sprite.hitboxCenter[0] - self.currentMapSize[0] + -camera.x, sprite.hitboxCenter[1] + self.currentMapSize[1] - camera.y), sprite.radius, 1)
					
					#pygame.draw.line(self.screen, "black", (sprite.hitboxCenter[0] - camera.x, sprite.hitboxCenter[1] - camera.y) , 
					#				(self.model.mainCharacter.distVector.x - camera.x, self.model.mainCharacter.distVector.y - camera.y))
				
				pygame.draw.rect(self.screen, "black", (sprite.x - camera.x , sprite.y - camera.y, 
				sprite.w,sprite.h ), 1)

		for sprite in self.model.obstacles:
			if self.model.hitBoxModeOn:
				pygame.draw.rect(self.screen, "green", (sprite.x - camera.x , sprite.y - camera.y, 
				sprite.w,sprite.h ), 1)
				
	def drawHealthBar(self):
		playerHP = round(self.model.mainCharacter.hp/self.model.mainCharacter.maxHp * 100, 2)	
		playerHpSurface = self.base_font.render("Life: " + str(playerHP) + "%", True, (255,255,255))
		self.screen.blit(playerHpSurface,(self.screen_size[0] - 200, 0))

		pygame.draw.rect(self.screen, "white", (self.screen_size[0] - 200, self.screen_size[1] - 778, 200, 36), 2)				
		pygame.draw.rect(self.screen, "#CC0000", (self.screen_size[0] - 200 + 2, self.screen_size[1] - 778 + 2, 196 * (playerHP/100), 32))

	# Draw infinite scrolling map
	def drawMap(self):
		# Center image
		self.currentMap.drawWithOffset(-camera.x, -camera.y)

		# Moving Right
		if camera.x + camera.width > self.currentMapSize[0]:
			self.currentMap.drawWithOffset(self.currentMapSize[0] - camera.x, -camera.y)
		# Moving Left
		if camera.x < 0:
			self.currentMap.drawWithOffset(-self.currentMapSize[0] + -camera.x, -camera.y)
		# Moving Up
		if camera.y < 0:
			self.currentMap.drawWithOffset(-camera.x, -self.currentMapSize[1] + -camera.y)
		# Moving Down
		if camera.y + camera.height > self.currentMapSize[1]:
			self.currentMap.drawWithOffset(-camera.x, self.currentMapSize[1] -camera.y)

		# Diagonals				
		# Right-Up
		if camera.x + camera.width > self.currentMapSize[0] and camera.y < 0:
			self.currentMap.drawWithOffset(self.currentMapSize[0] - camera.x, -self.currentMapSize[1] + -camera.y)	
		# Right-Down
		if camera.x + camera.width > self.currentMapSize[0] and camera.y + camera.height > self.currentMapSize[1]:
			self.currentMap.drawWithOffset(self.currentMapSize[0] - camera.x, self.currentMapSize[1] -camera.y)
		# Left-Up
		if camera.x < 0 and camera.y < 0:
			self.currentMap.drawWithOffset(-self.currentMapSize[0] + -camera.x, -self.currentMapSize[1] + -camera.y)
		# Left-Down
		if camera.x < 0 and camera.y + camera.height > self.currentMapSize[1]:
			self.currentMap.drawWithOffset(-self.currentMapSize[0] + -camera.x, self.currentMapSize[1] -camera.y)