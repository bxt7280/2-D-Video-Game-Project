from Sprites import *
import random

class Model():
	def __init__(self):
		self.dest_x = 0
		self.dest_y = 0 
		self.dictOfSpriteSheets = {} 
		self.mainCharacter = MainCharacter(400, 800, self) 
		self.sprites = [] # Main list of sprites
		self.spriteListBuffer = [] # List of sprites that need to be added to main sprite list
		self.sprites.append(self.mainCharacter)   
		self.screenSize = 0

		# Toggle Hitbox mode on/off
		self.hitBoxModeOn = False

		# self.sprites.append(Slime(200, 350, self))
		# self.sprites.append(Slime(600, 100, self))

		for i in range(50):
			self.sprites.append(Slime(random.randrange(0,800), random.randrange(0, 650), self))

		#self.sprites.append(Border(50, 50, self))


	def update(self):
		# Update all sprites
		for sprite in self.sprites:
			sprite.update()

		# Check for collisions with border
		for sprite in self.sprites:
			if sprite.canCollideWithBorder:
				sprite.collideWithBorder(self.screenSize)

		# Check for collisions with other sprites
		#print(self.sprites)
		for sprite in self.sprites:
			if sprite.canCollideWithSprite:
				for sprite2 in self.sprites:
					if sprite2 != sprite:
						if self.contactWithSprite(sprite, sprite2): 
							sprite.collideWithSprite(sprite2)


		# Add sprites from spriteListBuffer
		self.sprites.extend(self.spriteListBuffer)
		self.spriteListBuffer.clear()
				
		# Clean up and remove all inactive or "dead" sprites
		for sprite in self.sprites:
			if sprite.isActive == False:
				self.sprites.remove(sprite)

		# Tell all applicable sprites to save their coordinates
		self.universalSavePreviousCoordinates()

	# Returns true if sprite a is in contact with sprite b. No collision hitbox considered
	# def contactWithSprite(self, a, b):
	# 	if a.x + a.w < b.x:
	# 		print("no contact")
	# 		return False
	# 	if a.x > b.x + b.w:
	# 		print("no contact")
	# 		return False
	# 	if a.y + a.h < b.y: # assumes bigger is downward
	# 		print("no contact")
	# 		return False
	# 	if a.y > b.y + b.h: # assumes bigger is downward
	# 		print("no contact")
	# 		return False
		
	# 	print("contact")
	# 	return True
	
	# Returns true if sprite a is in contact with sprite b	
	def contactWithSprite(self, a, b):
		if a.x + a.hitboxLeft + (a.w + a.hitboxW) < b.x + b.hitboxLeft:
			return False
		if a.x + a.hitboxLeft > b.x + b.hitboxLeft + (b.w + b.hitboxW):
			return False
		if a.y + a.hitboxTop +(a.h + a.hitboxH) < b.y + b.hitboxTop: # assumes bigger is downward
			return False
		if a.y + a.hitboxTop > b.y + b.hitboxTop +(b.h + b.hitboxH): # assumes bigger is downward
			return False
		
		return True
		
	def SpriteClicked(self,s, mouse_x, mouse_y):
		clicked = True
		if mouse_x < s.x:
			clicked = False	
		if mouse_x  > s.x + 55:
			clicked = False
		if mouse_y < s.y:
			clicked = False
		if mouse_y > s.y + 400:
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