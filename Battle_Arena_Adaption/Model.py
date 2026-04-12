import random
from Sprites import *

class Model():
	def __init__(self):
		self.dictOfSpriteSheets = {} 
		self.sprites = [] # Main list of sprites
		self.spriteListBuffer = [] # List of sprites that need to be added to main sprite list
		self.mainCharacter = MainCharacter(400, 800, self) 		
		self.sprites.append(self.mainCharacter)   
		self.screenSize = 0

		# Toggle Hitbox mode on/off
		self.hitBoxModeOn = False

		slimeClass = Slime
		testSlime = slimeClass(200, 350, self)
		self.sprites.append(testSlime)
		# self.sprites.append(HomingFireball(700, 700, self, testSlime))
		# self.sprites.append(Slime(600, 100, self))

		# for i in range(30):
		# 	self.sprites.append(Slime(random.randrange(0,800), random.randrange(0, 500), self))

		# self.sprites.append(Border(50, 50)) # Use as an invisible border on top of tile maps. Experimental.

	def update(self):
		# Update all sprites
		self.updateAllSprites()

		# Check for collisions with border
		self.checkBorderCollisions()

		# Check for collisions with other sprites
		self.checkSpriteCollisions()

		# Add sprites from spriteListBuffer
		# Used because one cannot add sprites to a list while iterating through it
		self.addBufferedSprites()

		# Clean up and remove all inactive or "dead" sprites
		for sprite in self.sprites:
			if sprite.isActive == False:
				self.sprites.remove(sprite)

		# Tell all applicable sprites to save their coordinates
		self.universalSavePreviousCoordinates()

	def updateAllSprites(self):
		for sprite in self.sprites:
			sprite.update()

	def checkBorderCollisions(self):
		for sprite in self.sprites:
			if sprite.canCollideWithBorder:
				sprite.collideWithBorder(self.screenSize)

	def checkSpriteCollisions(self):
		for sprite in self.sprites:
			if sprite.canCollideWithSprite:
				for sprite2 in self.sprites:
					if sprite2 != sprite:
						if self.contactWithSprite(sprite, sprite2): 
							sprite.collideWithSprite(sprite2)

	def addBufferedSprites(self):
		self.sprites.extend(self.spriteListBuffer)
		self.spriteListBuffer.clear()

	def removeInactiveSprites(self):
		for sprite in self.sprites:
			if sprite.isActive == False:
				self.sprites.remove(sprite)

	# Returns true if sprite a is in contact with sprite b	
	def contactWithSprite(self, a, b):
		if a.x + a.hitboxLeft + (a.w + a.hitboxW) < b.x + b.hitboxLeft:
			return False
		if a.x + a.hitboxLeft > b.x + b.hitboxLeft + (b.w + b.hitboxW):
			return False
		if a.y + a.hitboxTop +(a.h + a.hitboxH) < b.y + b.hitboxTop: # assumes bigger is downward
			return False
		if a.y + a.hitboxTop > b.y + b.hitboxTop + (b.h + b.hitboxH): # assumes bigger is downward
			return False
		
		return True
		
	def spriteClicked(self,s, mouse_x, mouse_y):
		clicked = True
		if mouse_x < s.x + s.hitboxLeft:
			clicked = False	
		if mouse_x  > s.x + s.hitboxLeft + (s.w + s.hitboxW):
			clicked = False
		if mouse_y < s.y + s.hitboxTop:
			clicked = False
		if mouse_y > s.y + s.hitboxTop + (s.h + s.hitboxH):
			clicked = False
		return clicked
	
	# Saves coordinates of any sprite with collide capability
	def universalSavePreviousCoordinates(self):	
		for sprite in self.sprites:
			if sprite.canCollideWithBorder or sprite.canCollideWithSprite:
				sprite.savePreviousCoordinates()

	# Set Screen Size. Set when view is initialized.
	def setScreenSize(self, size):
		self.screenSize = size