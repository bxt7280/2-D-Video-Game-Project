# Ben Thiele - Battle Arena
import pygame
import time
from pygame.locals import*
from enum import Enum
import os
import random

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


class Sprite():
	def __init__(self, xPos, yPos, w, h, canCollideWithBorder, canCollideWithSprite, isActive):
		self.x = xPos 
		self.y = yPos 
		self.w = w
		self.h = h
		self.canCollideWithBorder = canCollideWithBorder
		self.canCollideWithSprite = canCollideWithSprite
		self.isActive = isActive 
		self.currentSpriteSheet = 0
		self.currentSpriteCellIndex = 0
		# Collision/Hitbox Offsets
		self.hitboxLeft = 0
		self.hitboxTop = 0
		self.hitboxW = 0
		self.hitboxH = 0

class Fireball(Sprite):
	def __init__(self, xPos, yPos, direction, model):
		super(Fireball, self).__init__(xPos, yPos, 47, 47, True, True, True)
		self.vert_vel = 5.0
		self.px = 0
		self.py = 0
		self.direction = direction
		self.model = model
		
		# Load SpriteSheet
		if "fireballSpriteSheets" not in self.model.dictOfSpriteSheets.keys():
			self.model.dictOfSpriteSheets["fireballSpriteSheets"] = []
			for fileName in os.listdir("./Images/fireball"):
				self.model.dictOfSpriteSheets["fireballSpriteSheets"].append(SpriteSheet("./Images/fireball/" + fileName, 1, 1))

		self.currentSpriteSheet = self.model.dictOfSpriteSheets["fireballSpriteSheets"][0]
		
	def update(self):
		self.moveFireball()
		
	# Changes direction. If invaild input defaults to "NEUTRAL" Currently Not Used. Might use to bounce off walls.
	def changeDirection(self, direction):
		match direction:
			case Direction.UP:
				self.direction = Direction.UP
			case Direction.DOWN:
				self.direction = Direction.DOWN
			case Direction.LEFT:
				self.direction = Direction.LEFT
			case Direction.RIGHT:
				self.direction = Direction.RIGHT
			case Direction.UP_LEFT:
				self.direction = Direction.UP_LEFT
			case Direction.DOWN_LEFT:
				self.direction = Direction.DOWN_LEFT
			case Direction.UP_RIGHT:
				self.direction = Direction.UP_RIGHT
			case Direction.DOWN_RIGHT:
				self.direction = Direction.DOWN_RIGHT
			case _:
				self.direction = Direction.NEUTRAL

	def moveFireball(self):
		self.vert_vel += 3.0
		match self.direction:
			case Direction.UP:
				self.y -= self.vert_vel
			case Direction.DOWN:
				self.y += self.vert_vel
			case Direction.LEFT:
				self.x -= self.vert_vel
			case Direction.RIGHT:
				self.x += self.vert_vel
			case Direction.UP_LEFT:
				self.y -= self.vert_vel
				self.x -= self.vert_vel
			case Direction.DOWN_LEFT:
				self.y += self.vert_vel
				self.x -= self.vert_vel
			case Direction.UP_RIGHT:
				self.y -= self.vert_vel
				self.x += self.vert_vel
			case Direction.DOWN_RIGHT:
				self.y += self.vert_vel
				self.x += self.vert_vel				
			case _:
				self.direction = Direction.UP

	def collideWithBorder(self, screenSize):
		# Past the border, but previously on left hand side of the border
		if self.x + self.hitboxLeft + (self.w + self.hitboxW) >= screenSize[0] and self.px + self.hitboxLeft + (self.w + self.hitboxW) <= screenSize[0]:
			self.isActive = False
			self.explode()		
		# Past the border, but previously on right hand side of the border
		if self.x + self.hitboxLeft <= 0 and self.px + self.hitboxLeft >= 0:
			self.isActive = False
			self.explode()				
		# Past the border, but previously above the border
		if self.y + self.hitboxTop + (self.h + self.hitboxH) >= screenSize[1] and self.py + self.hitboxTop + (self.h + self.hitboxH) <= screenSize[1]:
			self.isActive = False
			self.explode()	
		# Past the border, but previously below the border
		if self.y + self.hitboxTop <= 0 and self.py + self.hitboxTop >= 0:
			self.explode()	
			self.isActive = False

	def collideWithSprite(self, sprite):
			if not(isinstance(sprite, MainCharacter)) and isinstance(sprite, Slime):
				self.isActive = False
				self.explode()		

	def explode(self):
		self.model.spriteListBuffer.append(FireballExplosion(self.x - 27, self.y - 25, self.model))

	def savePreviousCoordinates(self):
		self.px = self.x
		self.py = self.y

class FireballExplosion(Sprite):
	def __init__(self, xPos, yPos, model):
		super(FireballExplosion, self).__init__(xPos, yPos, 96, 96, False, False, True)
		self.model = model
	
		# Load all SpriteSheets
		if "fireballExplosionSpriteSheets" not in self.model.dictOfSpriteSheets.keys():
			self.model.dictOfSpriteSheets["fireballExplosionSpriteSheets"] = []
			for fileName in os.listdir("./Images/stylized_explosion_001_small_yellow"):
				self.model.dictOfSpriteSheets["fireballExplosionSpriteSheets"].append(SpriteSheet("./Images/stylized_explosion_001_small_yellow/" + fileName, 9, 1))

		self.explodeSpriteSheets = self.model.dictOfSpriteSheets["fireballExplosionSpriteSheets"]

		self.currentSpriteSheet = self.explodeSpriteSheets[0]
		
	def update(self):
		self.animate()
		
	def animate(self):
		self.currentSpriteCellIndex += 1
			
		if self.currentSpriteCellIndex > 8:
			self.currentSpriteCellIndex = 0
			self.isActive = False

class LightningBolt(Sprite):
	def __init__(self, xPos, yPos, model):
		super(LightningBolt, self).__init__(xPos, yPos, 128, 256, False, False, True)
		self.model = model
		self.animateDuration = 4
	
		# Load all SpriteSheets
		if "lightningBoltSpriteSheets" not in self.model.dictOfSpriteSheets.keys():
			self.model.dictOfSpriteSheets["lightningBoltSpriteSheets"] = []
			for fileName in os.listdir("./Images/lightning"):
				self.model.dictOfSpriteSheets["lightningBoltSpriteSheets"].append(SpriteSheet("./Images/lightning/" + fileName, 5, 1))

		self.lightningBoltSpriteSheets = self.model.dictOfSpriteSheets["lightningBoltSpriteSheets"]

		self.currentSpriteSheet = self.lightningBoltSpriteSheets[0]
		
	def update(self):
		self.animate()
		
	def animate(self):
		self.currentSpriteCellIndex += 1
			
		if self.currentSpriteCellIndex > 4:
			self.currentSpriteCellIndex = 0
			self.animateDuration -= 1
			
		if self.animateDuration == 0:
			self.isActive = False


class BloodSplatter(Sprite):
	def __init__(self, xPos, yPos, model):
		super(BloodSplatter, self).__init__(xPos, yPos, 64, 64, False, False, True)
		self.model = model
	
		# Load all SpriteSheets
		if "bloodSplatterSpriteSheets" not in self.model.dictOfSpriteSheets.keys():
			self.model.dictOfSpriteSheets["bloodSplatterSpriteSheets"] = []
			for fileName in os.listdir("./Images/bloodSplatter"):
				self.model.dictOfSpriteSheets["bloodSplatterSpriteSheets"].append(SpriteSheet("./Images/bloodSplatter/" + fileName, 10, 1))

		self.bloodSplatterSpriteSheets = self.model.dictOfSpriteSheets["bloodSplatterSpriteSheets"]

		self.currentSpriteSheet = self.bloodSplatterSpriteSheets[0]
		
	def update(self):
		self.animate()
		
	def animate(self):
		self.currentSpriteCellIndex += 1
			
		if self.currentSpriteCellIndex > 9:
			self.currentSpriteCellIndex = 0
			self.isActive = False

class Slime(Sprite):
	def __init__(self, xPos, yPos, model):
		super(Slime, self).__init__(xPos, yPos, 64, 64, True, True, True)
		self.model = model
		self.px = 0
		self.py = 0
		self.provoked = False
		self.provokedCounter = 0
		self.isHurt = False
		self.isHurtCounter = 0
		self.isDying = False
		self.deathCounter = 0
		

		# Save original position as vector
		self.originalPos = pygame.math.Vector2(self.x, self.y)
	
		# Load all SpriteSheets
		if "slimeSpriteSheets" not in self.model.dictOfSpriteSheets.keys():
			self.model.dictOfSpriteSheets["slimeSpriteSheets"] = []
			for fileName in os.listdir("./Images/slime"):
				self.model.dictOfSpriteSheets["slimeSpriteSheets"].append(SpriteSheet("./Images/slime/" + fileName, 5, 3))

		self.slimeSpriteSheets = self.model.dictOfSpriteSheets["slimeSpriteSheets"]

		self.currentSpriteSheet = self.slimeSpriteSheets[0]
		
		self.frameDelayCounter = 2 # slow down rate of animation

		self.distVector = pygame.math.Vector2(self.x, self.y)


	def update(self):
		# Update distance vector
		self.distVector.x = self.x + self.hitboxLeft
		self.distVector.y = self.y + self.hitboxTop


		# Have slime follow mainCharacter based on conditions
		# if self.provoked == True and self.provokedCounter > 0:
		# 	if self.distVector.distance_to(self.model.mainCharacter.distVector) <= 150:
		# 		self.distVector.move_towards_ip(self.model.mainCharacter.distVector, 5)
		# 		self.x = self.distVector.x
		# 		self.y = self.distVector.y

		# 	if self.distVector.distance_to(self.model.mainCharacter.distVector) <= 1000:
		# 		self.distVector.move_towards_ip(self.model.mainCharacter.distVector, 3)
		# 		self.x = self.distVector.x
		# 		self.y = self.distVector.y
			
		# 	self.provokedCounter -= 1

		# if self.provokedCounter == 0:
		# 	self.provoked = False

		# if self.provoked == False:
		# 	self.distVector.distance_to(self.originalPos)
		# 	self.distVector.move_towards_ip(self.originalPos, 5)
		# 	self.x = self.distVector.x
		# 	self.y = self.distVector.y

		# Death if hit by lightning
		if self.isDying == True:
			if self.deathCounter == 0:
				self.bleed()
				self.isActive = False
			self.deathCounter -= 1

		self.animate()	
		
	def animate(self):
		if self.isHurt == True and self.isHurtCounter > 0:
			if self.currentSpriteSheet == self.slimeSpriteSheets[0]:
				self.currentSpriteSheet = self.slimeSpriteSheets[1]
			else:
				self.currentSpriteSheet = self.slimeSpriteSheets[0]
			
			self.isHurtCounter -= 1
		else:
			self.isHurt = False
			self.currentSpriteSheet = self.slimeSpriteSheets[0]

		if self.frameDelayCounter == 3:
			self.currentSpriteCellIndex += 1

		self.frameDelayCounter -= 1
		if self.frameDelayCounter == 0:
			self.frameDelayCounter = 3
			
		if self.currentSpriteCellIndex > 4:
			self.currentSpriteCellIndex = 0

	def collideWithBorder(self, screenSize):
		# Past the border, but previously on left hand side of the border
		if self.x + self.hitboxLeft + (self.w + self.hitboxW) >= screenSize[0] and self.px + self.hitboxLeft + (self.w + self.hitboxW) <= screenSize[0]:
			self.x = screenSize[0] - self.hitboxLeft - (self.w + self.hitboxW)	
		#Past the border, but previously on right hand side of the border
		if self.x + self.hitboxLeft <= 0 and self.px + self.hitboxLeft >= 0:
			self.x = 0 - self.hitboxLeft
		# Past the border, but previously above the border
		if self.y + self.hitboxTop + (self.h + self.hitboxH) >= screenSize[1] and self.py + self.hitboxTop + (self.h + self.hitboxH) <= screenSize[1]:
			self.y = screenSize[1] - self.hitboxTop - (self.h + self.hitboxH)
		# Past the border, but previously below the border
		if self.y + self.hitboxTop <= 0 and self.py + self.hitboxTop >= 0:
			self.y = 0 - self.hitboxTop

	def collideWithSprite(self, sprite):
		if isinstance(sprite, Fireball) and self.isDying == False: # Eventually change to sprite category rather than Fireballs specifically		
			self.isHurt = True
			self.isHurtCounter = 20
			self.provoked = True
			self.provokedCounter = 150
			self.isDying = True
			self.deathCounter = 20

		if isinstance(sprite, Slime):
			# In the sprite, but previously on left hand side of the sprite
			if self.x + self.hitboxLeft + (self.w + self.hitboxW) >= sprite.x + sprite.hitboxLeft and self.px + self.hitboxLeft + (self.w + self.hitboxW) <= sprite.x + sprite.hitboxLeft:
				self.x = sprite.x + sprite.hitboxLeft - self.hitboxLeft	- (self.w + self.hitboxW)	
			# In the sprite, but previously on right hand side of the sprite
			if self.x + self.hitboxLeft <= sprite.x + sprite.hitboxLeft + (sprite.w + sprite.hitboxW) and self.px + self.hitboxLeft >= sprite.x + sprite.hitboxLeft + (sprite.w + sprite.hitboxW):
				self.x = sprite.x + sprite.hitboxLeft + (sprite.w + sprite.hitboxW) - self.hitboxLeft
			# In the sprite, but previously above the sprite
			if self.y + self.hitboxTop +(self.h + self.hitboxH) >= sprite.y + sprite.hitboxTop and self.py + self.hitboxTop + (self.h + self.hitboxH) <= sprite.y + sprite.hitboxTop:
				self.y = sprite.y + sprite.hitboxTop - self.hitboxTop - (self.h + self.hitboxH)
			# In the sprite, but previously below the sprite
			if self.y + self.hitboxTop <= sprite.y + sprite.hitboxTop + (sprite.h + sprite.hitboxH) and self.py + self.hitboxTop >= sprite.y + sprite.hitboxTop + (sprite.h + sprite.hitboxH):
				self.y = sprite.y + sprite.hitboxTop + (sprite.h + sprite.hitboxH) - self.hitboxTop

	def hitByLightning(self):
		self.model.spriteListBuffer.append(LightningBolt(self.x - 34, self.y - 220 , self.model))
		self.isHurt = True
		self.isHurtCounter = 20
		self.isDying = True
		self.deathCounter = 20

	def bleed(self):
		self.model.spriteListBuffer.append(BloodSplatter(self.x, self.y, self.model))
	
	def savePreviousCoordinates(self):
		self.px = self.x
		self.py = self.y

# Imageless sprite used for invisible boundaries
class Border(Sprite):
	def __init__(self, xPos, yPos, model):
		super(Border, self).__init__(xPos, yPos, 50, 50, False, False, True)
		self.hitboxLeft = 0
		self.hitboxTop = 0
		self.hitboxW = 100
		self.hitboxH = 0
	def update(self):
		pass

			
class MainCharacter(Sprite):
	def __init__(self, xPos, yPos, model):
		super(MainCharacter, self).__init__(xPos - 256/2, yPos - 256/2, 256, 256, True, True, True)
		self.px = 0
		self.py = 0
		self.fireballChargeCounter = 0
		self.lightningAttackRecharge = 0
		self.lightningAttackOn = False
		
		# Collision/Hitbox parameters
		self.hitboxLeft = 105
		self.hitboxTop = 47
		self.hitboxW = -210
		self.hitboxH = -135

		self.direction = Direction.UP
		self.model = model
		
		# Load all SpriteSheets
		# Walk SpriteSheets
		self.model.dictOfSpriteSheets["girlWalkSpriteSheets"] = []
		for fileName in os.listdir("./Images/Girl/GirlSample_Walk_256Update"):
			self.model.dictOfSpriteSheets["girlWalkSpriteSheets"].append(SpriteSheet("./Images/Girl/GirlSample_Walk_256Update/" + fileName, 4, 3))

		self.walkSpriteSheets = self.model.dictOfSpriteSheets["girlWalkSpriteSheets"]
		
		# Idle SpriteSheets
		self.model.dictOfSpriteSheets["girlIdleSpriteSheets"] = []
		for fileName in os.listdir("./Images/Girl/GirlSampleReadyIdle"):
			self.model.dictOfSpriteSheets["girlIdleSpriteSheets"].append(SpriteSheet("./Images/Girl/GirlSampleReadyIdle/" + fileName, 4, 4))

		self.idleSpriteSheets = self.model.dictOfSpriteSheets["girlIdleSpriteSheets"]

		# Throw fireball SpriteSheets
		self.model.dictOfSpriteSheets["girlThrowFireSpriteSheets"] = []
		for fileName in os.listdir("./Images/Girl/GirlSampleFireball"):
			self.model.dictOfSpriteSheets["girlThrowFireSpriteSheets"].append(SpriteSheet("./Images/Girl/GirlSampleFireball/" + fileName, 4, 6))

		self.throwFireSpriteSheets = self.model.dictOfSpriteSheets["girlThrowFireSpriteSheets"]

		# Set initial SpriteSheet
		self.currentSpriteSheet = self.idleSpriteSheets[5]

		self.distVector = pygame.math.Vector2(self.x, self.y)
		

	def update(self):
		self.distVector.x = self.x + self.hitboxLeft
		self.distVector.y = self.y + self.hitboxTop

		if self.lightningAttackOn == True:
			self.lightningAttack()
			
			if self.lightningAttackRecharge > 0:
				self.lightningAttackRecharge -= 1

	def animateIdle(self):
		match(self.direction):
			case Direction.LEFT:
				self.currentSpriteSheet = self.idleSpriteSheets[3]

				self.currentSpriteCellIndex += 1
			
				if self.currentSpriteCellIndex > 8:
					self.currentSpriteCellIndex = 0
			case Direction.DOWN:
				self.currentSpriteSheet = self.idleSpriteSheets[0]

				self.currentSpriteCellIndex += 1
			
				if self.currentSpriteCellIndex > 8:
					self.currentSpriteCellIndex = 0
			case Direction.UP:
				self.currentSpriteSheet = self.idleSpriteSheets[5]

				self.currentSpriteCellIndex += 1
			
				if self.currentSpriteCellIndex > 8:
					self.currentSpriteCellIndex = 0
			case Direction.RIGHT:
				self.currentSpriteSheet = self.idleSpriteSheets[4]

				self.currentSpriteCellIndex += 1
			
				if self.currentSpriteCellIndex > 8:
					self.currentSpriteCellIndex = 0
			case Direction.UP_RIGHT:
				self.currentSpriteSheet = self.idleSpriteSheets[7]

				self.currentSpriteCellIndex += 1
			
				if self.currentSpriteCellIndex > 8:
					self.currentSpriteCellIndex = 0
			case Direction.UP_LEFT:
				self.currentSpriteSheet = self.idleSpriteSheets[6]

				self.currentSpriteCellIndex += 1
			
				if self.currentSpriteCellIndex > 8:
					self.currentSpriteCellIndex = 0
			case Direction.DOWN_RIGHT:
				self.currentSpriteSheet = self.idleSpriteSheets[2]

				self.currentSpriteCellIndex += 1
			
				if self.currentSpriteCellIndex > 8:
					self.currentSpriteCellIndex = 0
			case Direction.DOWN_LEFT:
				self.currentSpriteSheet = self.idleSpriteSheets[1]

				self.currentSpriteCellIndex += 1
			
				if self.currentSpriteCellIndex > 8:
					self.currentSpriteCellIndex = 0
			case _:
				self.currentSpriteCellIndex = 0

	def animateWalk(self):
		match(self.direction):
			case Direction.LEFT:
				self.currentSpriteSheet = self.walkSpriteSheets[3]

				self.currentSpriteCellIndex += 1
			
				if self.currentSpriteCellIndex > 8:
					self.currentSpriteCellIndex = 0
			case Direction.DOWN:
				self.currentSpriteSheet = self.walkSpriteSheets[0]

				self.currentSpriteCellIndex += 1
			
				if self.currentSpriteCellIndex > 8:
					self.currentSpriteCellIndex = 0
			case Direction.UP:
				self.currentSpriteSheet = self.walkSpriteSheets[5]

				self.currentSpriteCellIndex += 1
			
				if self.currentSpriteCellIndex > 8:
					self.currentSpriteCellIndex = 0
			case Direction.RIGHT:
				self.currentSpriteSheet = self.walkSpriteSheets[4]

				self.currentSpriteCellIndex += 1
			
				if self.currentSpriteCellIndex > 8:
					self.currentSpriteCellIndex = 0
			case Direction.UP_RIGHT:
				self.currentSpriteSheet = self.walkSpriteSheets[7]

				self.currentSpriteCellIndex += 1
			
				if self.currentSpriteCellIndex > 8:
					self.currentSpriteCellIndex = 0
			case Direction.UP_LEFT:
				self.currentSpriteSheet = self.walkSpriteSheets[6]

				self.currentSpriteCellIndex += 1
			
				if self.currentSpriteCellIndex > 8:
					self.currentSpriteCellIndex = 0
			case Direction.DOWN_RIGHT:
				self.currentSpriteSheet = self.walkSpriteSheets[2]

				self.currentSpriteCellIndex += 1
			
				if self.currentSpriteCellIndex > 8:
					self.currentSpriteCellIndex = 0
			case Direction.DOWN_LEFT:
				self.currentSpriteSheet = self.walkSpriteSheets[1]

				self.currentSpriteCellIndex += 1
			
				if self.currentSpriteCellIndex > 8:
					self.currentSpriteCellIndex = 0
			case _:
				self.currentSpriteCellIndex = 0
			

	def collideWithBorder(self, screenSize):
		# Past the border, but previously on left hand side of the border
		if self.x + self.hitboxLeft + (self.w + self.hitboxW) >= screenSize[0] and self.px + self.hitboxLeft + (self.w + self.hitboxW) <= screenSize[0]:
			self.x = screenSize[0] - self.hitboxLeft - (self.w + self.hitboxW)	
		#Past the border, but previously on right hand side of the border
		if self.x + self.hitboxLeft <= 0 and self.px + self.hitboxLeft >= 0:
			self.x = 0 - self.hitboxLeft
		# Past the border, but previously above the border
		if self.y + self.hitboxTop + (self.h + self.hitboxH) >= screenSize[1] and self.py + self.hitboxTop + (self.h + self.hitboxH) <= screenSize[1]:
			self.y = screenSize[1] - self.hitboxTop - (self.h + self.hitboxH)
		# Past the border, but previously below the border
		if self.y + self.hitboxTop <= 0 and self.py + self.hitboxTop >= 0:
			self.y = 0 - self.hitboxTop

	def collideWithSprite(self, sprite):
		# In the sprite, but previously on left hand side of the sprite
		if self.x + self.hitboxLeft + (self.w + self.hitboxW) >= sprite.x + sprite.hitboxLeft and self.px + self.hitboxLeft + (self.w + self.hitboxW) <= sprite.x + sprite.hitboxLeft:
			self.x = sprite.x + sprite.hitboxLeft - self.hitboxLeft	- (self.w + self.hitboxW)	
		# In the sprite, but previously on right hand side of the sprite
		if self.x + self.hitboxLeft <= sprite.x + sprite.hitboxLeft + (sprite.w + sprite.hitboxW) and self.px + self.hitboxLeft >= sprite.x + sprite.hitboxLeft + (sprite.w + sprite.hitboxW):
			self.x = sprite.x + sprite.hitboxLeft + (sprite.w + sprite.hitboxW) - self.hitboxLeft
		# In the sprite, but previously above the sprite
		if self.y + self.hitboxTop +(self.h + self.hitboxH) >= sprite.y + sprite.hitboxTop and self.py + self.hitboxTop + (self.h + self.hitboxH) <= sprite.y + sprite.hitboxTop:
			self.y = sprite.y + sprite.hitboxTop - self.hitboxTop - (self.h + self.hitboxH)
		# In the sprite, but previously below the sprite
		if self.y + self.hitboxTop <= sprite.y + sprite.hitboxTop + (sprite.h + sprite.hitboxH) and self.py + self.hitboxTop >= sprite.y + sprite.hitboxTop + (sprite.h + sprite.hitboxH):
			self.y = sprite.y + sprite.hitboxTop + (sprite.h + sprite.hitboxH) - self.hitboxTop
		
	def savePreviousCoordinates(self):
		self.px = self.x
		self.py = self.y
		
	# Changes direction. If invaild input defaults to "IDLE"
	def changeDirection(self, direction):
		match direction:
			case Direction.UP:
				self.direction = Direction.UP
			case Direction.DOWN:
				self.direction = Direction.DOWN
			case Direction.LEFT:
				self.direction = Direction.LEFT
			case Direction.RIGHT:
				self.direction = Direction.RIGHT
			case Direction.UP_LEFT:
				self.direction = Direction.UP_LEFT
			case Direction.DOWN_LEFT:
				self.direction = Direction.DOWN_LEFT
			case Direction.UP_RIGHT:
				self.direction = Direction.UP_RIGHT
			case Direction.DOWN_RIGHT:
				self.direction = Direction.DOWN_RIGHT
			case _:
				pass

	def animateThrowFireball(self):
		match(self.direction):
			case Direction.LEFT:
				self.currentSpriteSheet = self.throwFireSpriteSheets[3]

				self.currentSpriteCellIndex += 1

				if self.currentSpriteCellIndex == 18:
					self.throwFireball(65, 75)					
			
				if self.currentSpriteCellIndex > 22:					
					self.currentSpriteCellIndex = 0
				

			case Direction.DOWN:
				self.currentSpriteSheet = self.throwFireSpriteSheets[0]

				self.currentSpriteCellIndex += 1

				if self.currentSpriteCellIndex == 18:
					self.throwFireball(self.hitboxLeft, 100)				
				
				if self.currentSpriteCellIndex > 22:
					self.currentSpriteCellIndex = 0

			case Direction.UP:
				self.currentSpriteSheet = self.throwFireSpriteSheets[5]

				self.currentSpriteCellIndex += 1
				
				if self.currentSpriteCellIndex == 18:
					self.throwFireball(self.hitboxLeft, 10)				

				if self.currentSpriteCellIndex > 22:
					self.currentSpriteCellIndex = 0

			case Direction.RIGHT:
				self.currentSpriteSheet = self.throwFireSpriteSheets[4]

				self.currentSpriteCellIndex += 1
				
				if self.currentSpriteCellIndex == 18:
					self.throwFireball(150, 75)		
				
				if self.currentSpriteCellIndex > 22:
					self.currentSpriteCellIndex = 0

			case Direction.UP_RIGHT:
				self.currentSpriteSheet = self.throwFireSpriteSheets[7]

				self.currentSpriteCellIndex += 1
			
				if self.currentSpriteCellIndex == 18:
					self.throwFireball(150, 75)	
				
				if self.currentSpriteCellIndex > 22:
					self.currentSpriteCellIndex = 0

			case Direction.UP_LEFT:
				self.currentSpriteSheet = self.throwFireSpriteSheets[6]

				self.currentSpriteCellIndex += 1

				if self.currentSpriteCellIndex == 18:
					self.throwFireball(70, 50)	

				if self.currentSpriteCellIndex > 22:
					self.currentSpriteCellIndex = 0

			case Direction.DOWN_RIGHT:
				self.currentSpriteSheet = self.throwFireSpriteSheets[2]

				self.currentSpriteCellIndex += 1

				if self.currentSpriteCellIndex == 18:
					self.throwFireball(130, 85)	
			
				if self.currentSpriteCellIndex > 22:
					self.currentSpriteCellIndex = 0

			case Direction.DOWN_LEFT:
				self.currentSpriteSheet = self.throwFireSpriteSheets[1]

				self.currentSpriteCellIndex += 1
				if self.currentSpriteCellIndex == 18:
					self.throwFireball(65, 85)	

				if self.currentSpriteCellIndex > 22:
					self.currentSpriteCellIndex = 0
			case _:
				self.currentSpriteCellIndex = 0

	def throwFireball(self, offsetX, offsetY):
		self.model.sprites.append(Fireball(self.x + offsetX, self.y + offsetY, self.direction, self.model))

	def lightningAttack(self):
		# if self.lightningAttackRecharge == 0:
		# 	listOfSlimes = [sprite for sprite in self.model.sprites if isinstance(sprite, Slime)]
		# 	if len(listOfSlimes) > 0:
		# 		randomIndex = random.randrange(len(listOfSlimes))
		# 		listOfSlimes[randomIndex].hitByLightning()
		# 		self.lightningAttackRecharge = 30
		if self.lightningAttackRecharge == 0:
			listOfSlimes = [sprite for sprite in self.model.sprites if isinstance(sprite, Slime)]
			if len(listOfSlimes) > 0:
				for slime in listOfSlimes:
					if random.randrange(1, 60) == 5 and not(slime.isDying):
						slime.hitByLightning()
			self.lightningAttackRecharge = 20
	



class Model():
	def __init__(self):
		self.dest_x = 0
		self.dest_y = 0 
		self.dictOfSpriteSheets = {} 
		self.mainCharacter = MainCharacter(400, 700, self) 
		self.sprites = [] # Main list of sprites
		self.spriteListBuffer = [] # List of sprites that need to be added to main sprite list
		self.sprites.append(self.mainCharacter)   
		self.screenSize = 0

		# Toggle Hitbox mode on/off
		self.hitBoxModeOn = False

		# self.sprites.append(Slime(200, 350, self))
		# self.sprites.append(Slime(600, 100, self))

		for i in range(50):
			self.sprites.append(Slime(random.randrange(0,800), random.randrange(0, 800), self))

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

class Controller():
	def __init__(self, model):
		self.model = model
		self.keep_going = True
		self.editorToggle = True
		self.spriteToBeDrawn = 0
		self.ctrlKeyPressDelay = 0

		pygame.key.set_repeat(5000)

	def update(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				self.keep_going = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.keep_going = False
				# Hitbox Mode ON/OFF
				if event.key == K_h:
					self.model.hitBoxModeOn = not self.model.hitBoxModeOn
				if event.key == K_SPACE:
					self.model.mainCharacter.lightningAttackOn = not self.model.mainCharacter.lightningAttackOn

			# elif event.type == pygame.MOUSEBUTTONUP:
			# 	# get current x and y coordinates when mouse is clicked
			# 	x, y = pygame.mouse.get_pos()
				
			# 	# Check if in map editor mode
			# 	if self.editorToggle == True:
			# 		#Checks if tube is clicked. Adds new tube if not.
			# 		clicked = False
			# 		i = 0
			# 		if len(self.model.sprites) > 0:
			# 			while i < len(self.model.sprites) and clicked == False:
			# 				if (self.model.SpriteClicked(self.model.sprites[i],x + self.model.mainCharacter.x - self.model.mainCharacter.marioOffset, y)):
			# 					clicked = True
			# 					if not(isinstance(self.model.sprites[i], MainCharacter)):
			# 						self.model.sprites.remove(self.model.sprites[i])
			# 				i = i + 1
			# 		if clicked == False:
			# 			# Determine what sprite to draw
			# 			if self.spriteToBeDrawn == 0:
			# 				self.model.sprites.append(Tube(x + self.model.mainCharacter.x - self.model.mainCharacter.marioOffset,y))
			# 			if self.spriteToBeDrawn == 1:
			# 				self.model.sprites.append(Goomba(x + self.model.mainCharacter.x - self.model.mainCharacter.marioOffset,y))
		
		self.evaluateKeyPress()

	
	def evaluateKeyPress(self):
		keys = pygame.key.get_pressed()
		
		# Throw fireball. Delay added.
		# if keys[K_LCTRL] and self.ctrlKeyPressDelay == 0:
		# 	self.model.mainCharacter.throwFireball()
		# 	self.ctrlKeyPressDelay = 3
		# elif self.ctrlKeyPressDelay > 0:
		# 	self.ctrlKeyPressDelay -= 1

		if keys[K_LCTRL]:
			self.model.mainCharacter.animateThrowFireball()
		
		# Movement and direction
		if keys[K_UP] or keys[K_DOWN] or keys[K_LEFT] or keys[K_RIGHT]:
			if keys[K_UP] and keys[K_LEFT]:
				if not keys[K_LCTRL]:
					self.model.mainCharacter.x -= 6
					self.model.mainCharacter.y -= 6
					self.model.mainCharacter.animateWalk()	
				self.model.mainCharacter.changeDirection(Direction.UP_LEFT)
			elif keys[K_DOWN] and keys[K_LEFT]:
				if not keys[K_LCTRL]:
					self.model.mainCharacter.x -= 6
					self.model.mainCharacter.y += 6
					self.model.mainCharacter.animateWalk()	
				self.model.mainCharacter.changeDirection(Direction.DOWN_LEFT)
			elif keys[K_UP] and keys[K_RIGHT]:
				if not keys[K_LCTRL]:
					self.model.mainCharacter.x += 6
					self.model.mainCharacter.y -= 6
					self.model.mainCharacter.animateWalk()				
				self.model.mainCharacter.changeDirection(Direction.UP_RIGHT)
			elif keys[K_DOWN] and keys[K_RIGHT]:
				if not keys[K_LCTRL]:
					self.model.mainCharacter.x += 6
					self.model.mainCharacter.y += 6
					self.model.mainCharacter.animateWalk()	
				self.model.mainCharacter.changeDirection(Direction.DOWN_RIGHT)			
			
			
			elif keys[K_LEFT]:
				if not keys[K_LCTRL]:
					self.model.mainCharacter.x -= 6
					self.model.mainCharacter.animateWalk()
				self.model.mainCharacter.changeDirection(Direction.LEFT)				
			elif keys[K_RIGHT]:
				if not keys[K_LCTRL]:			
					self.model.mainCharacter.x += 6
					self.model.mainCharacter.animateWalk()
				self.model.mainCharacter.changeDirection(Direction.RIGHT)
				
			elif keys[K_UP]:
				if not keys[K_LCTRL]:			
					self.model.mainCharacter.y -= 6
					self.model.mainCharacter.animateWalk()
				self.model.mainCharacter.changeDirection(Direction.UP)
			elif keys[K_DOWN]:
				if not keys[K_LCTRL]:
					self.model.mainCharacter.y += 6
					self.model.mainCharacter.animateWalk()
				self.model.mainCharacter.changeDirection(Direction.DOWN)
				
		else:
			self.model.mainCharacter.animateIdle()

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


print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
pygame.display.set_caption("Battle Arena")

clock = pygame.time.Clock()

m = Model()
v = View(m)
c = Controller(m)

while c.keep_going:
	c.update()
	m.update()
	v.update()

	clock.tick(30)
	#print(clock.get_fps())

print("Goodbye")


