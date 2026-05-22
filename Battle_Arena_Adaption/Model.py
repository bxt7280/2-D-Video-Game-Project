import random
from Sprites import *
from Util import Direction

class Model():
	def __init__(self, screen, screenSize):
		self.screenSize = screenSize
		self.screen = screen
		self.dictOfSpriteSheets = {} 
		self.dictOfSingleImages = {}
		self.sprites = [] # Main list of sprites
		self.spriteListBuffer = [] # List of sprites that need to be added to main sprite list
		self.mainCharacter = MainCharacter(camera.width / 2 - 128 ,camera.width / 2, self) 	# value "128" is half the width of the mainCharacter image	
		self.sprites.append(self.mainCharacter) 
		self.currentMapSize = (0, 0)

		# Toggle Hitbox mode on/off
		self.hitBoxModeOn = False

		# slimeClass = Slime
		# testSlime = slimeClass(200, 350, self)
		# self.sprites.append(testSlime)
		# self.sprites.append(HomingFireball(700, 700, self, testSlime))


		# for i in range(30):
		# 	self.sprites.append(Slime(random.randrange(0,800), random.randrange(0, 500), self))

		# self.sprites.append(Border(50, 50)) # Use as an invisible border on top of tile maps. Experimental.
		# self.sprites.append(Border(100, 0))
	def update(self):
		# Update all sprites
		self.updateAllSprites()

		# Check for collisions with border
		#sself.checkBorderCollisions()

		# Check for collisions with other sprites
		self.checkSpriteCollisions()

		# Add sprites from spriteListBuffer
		# Used because one cannot add sprites to a list while iterating through it
		self.addBufferedSprites()

		# Clean up and remove all inactive or "dead" sprites
		self.sprites = [sprite for sprite in self.sprites if sprite.isActive]

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
						# Mask Collision for Slimes and FlyingSword
						if isinstance(sprite, Slime) and isinstance(sprite2, FlyingSword):
							if self.maskContactWithSprite(sprite, sprite2):
								sprite.maskCollideWithSprite(sprite2)
						# Circle Collision for Slime vs Slime
						elif isinstance(sprite,Slime,) and isinstance(sprite2, Slime):
							collisionResult = self.circleContactWithSprite(sprite, sprite2)
							if collisionResult[0]:	
								sprite.circleCollideWithSprite(sprite2, collisionResult[1], collisionResult[2])
						else:
							if self.contactWithSprite(sprite, sprite2): 
								sprite.collideWithSprite(sprite2)
						
		# mainCharacter will pulsate red if at least one collision
		if self.mainCharacter.collisionCount <= 0:
			self.mainCharacter.pulsateRed = False
		else:
			self.mainCharacter.pulsateRed = True
					
	def addBufferedSprites(self):
		self.sprites.extend(self.spriteListBuffer)
		self.spriteListBuffer.clear()

	def removeInactiveSprites(self):
		for sprite in self.sprites:
			if sprite.isActive == False:
				self.sprites.remove(sprite)
	
	# Returns true if sprite a is in contact with sprite b	
	def contactWithSprite(self, a, b):
		collisionOffsets = self.calculateCollisionOffsets(a, b)		
		collisionOffsetX = collisionOffsets[0]
		collisionOffsetY = collisionOffsets[1]
						
		if a.x + a.hitboxLeft + (a.w + a.hitboxW) < b.x + b.hitboxLeft + collisionOffsetX:
			return False
		if a.x + a.hitboxLeft > b.x + b.hitboxLeft + (b.w + b.hitboxW) + collisionOffsetX:
			return False
		if a.y + a.hitboxTop +(a.h + a.hitboxH) < b.y + b.hitboxTop + collisionOffsetY: 
			return False
		if a.y + a.hitboxTop > b.y + b.hitboxTop + (b.h + b.hitboxH) + collisionOffsetY: 
			return False
		
		return True
	
	# Determine if map size should be added to sprite b during rectangle collision detection
	def calculateCollisionOffsets(self, a, b):
		collisionOffsetY = 0
		collisionOffsetX = 0
		
		# Determine whether b.y is closer to 0 or screenSize y
		compareZeroX = abs(0 - b.x)
		compareScreenSizeX = abs(self.screenSize[0] - b.x)
		compareZeroY = abs(0 - b.y)
		compareScreenSizeY = abs(self.screenSize[1] - b.y)
			
		# Adjust collisionOffsetY based on conditions
		if compareZeroY < compareScreenSizeY and a.moduloEventUp == True:
			collisionOffsetY = self.currentMapSize[1]
		elif compareZeroY > compareScreenSizeY and a.moduloEventDown == True:
			collisionOffsetY = -self.currentMapSize[1]
		else:
			collisionOffsetY = 0
		
		# Adjust collisionOffsetX based on conditions
		if compareZeroX < compareScreenSizeX and a.moduloEventLeft == True:
			collisionOffsetX = self.currentMapSize[0]
		elif compareZeroX > compareScreenSizeX and a.moduloEventRight == True:
			collisionOffsetX = -self.currentMapSize[0]
		else:
			collisionOffsetX = 0

		return (collisionOffsetX, collisionOffsetY)
	
	# Determine if map size should be added to sprite b during distance based operations
	def calculateDistanceOffsets(self, a, b):
		possibleXOffsets = [0, self.currentMapSize[0], -self.currentMapSize[0]]
		possibleYOffsets = [0, self.currentMapSize[1], -self.currentMapSize[1]]

		listOfOffsets = []

		for xOffset in possibleXOffsets:
			for yOffset in possibleYOffsets:
				listOfOffsets.append((xOffset, yOffset))

		listOfPossibleDist = []

		for x, y in listOfOffsets:
			dist = a.distVector.distance_to((b.distVector.x + x, b.distVector.y + y))
			listOfPossibleDist.append([x, y, dist])

		listOfPossibleDist.sort(key=lambda x: x[2])
		shortestDist = listOfPossibleDist[0]

		return shortestDist

	def maskContactWithSprite(self, a, b):
		maskA = pygame.mask.from_surface(a.image)
		maskB = pygame.mask.from_surface(b.image)

		if maskA.overlap(maskB, (b.x - a.x, b.y - a.y)):
			return True
		else:
			return False
		
	def circleContactWithSprite(self, a, b):
		depth = 0
		normal = pygame.math.Vector2(0,0)

		distOffsets = self.calculateDistanceOffsets(a, b)
		bWithOffsets = pygame.math.Vector2(b.distVector.x + distOffsets[0], b.distVector.y + distOffsets[1])
		
		n = bWithOffsets - a.distVector
		distSq = n.length_squared()
		r2 = a.radius + b.radius
		radiusSq = r2 * r2

		if (distSq >= radiusSq):
			return [False]
		
		dist = math.sqrt(distSq)
		
		if dist != 0:
			depth = r2 - dist
			normal = n / dist
		else:
			depth = r2;
			normal = pygame.math.Vector2(1,0)
		
		return [True, depth, normal]
				
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
	
	# Saves coordinates of any sprite that has collision detection
	def universalSavePreviousCoordinates(self):	
		for sprite in self.sprites:
			if sprite.canCollideWithBorder or sprite.canCollideWithSprite:
				sprite.savePreviousCoordinates()
