import os
import pygame
import random
from Util import Direction, SpriteSheet

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

class MainCharacter(Sprite):
	def __init__(self, xPos, yPos, model):
		super(MainCharacter, self).__init__(xPos - 256/2, yPos - 256/2, 256, 256, True, True, True)
		self.px = 0
		self.py = 0
		self.fireballChargeCounter = 0
		self.lightningAttackRecharge = 0
		self.lightningAttackOn = False
		self.autoFireballCooldown = 0
		
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

		if self.autoFireballCooldown > 0:
			self.autoFireballCooldown -= 1
			
		self.autoFireball()

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

	def autoFireball(self):
		if self.autoFireballCooldown == 0:
			self.autoFireballCooldown = 50
			listOfSlimes = [sprite for sprite in self.model.sprites if isinstance(sprite, Slime)]
			if len(listOfSlimes) > 0: 
				closestDistanceFromChar = 1000
				closestSlimeIndex = 0
				for i in range(len(listOfSlimes)):
					if self.distVector.distance_to(listOfSlimes[i].distVector) < closestDistanceFromChar:
						closestDistanceFromChar = self.distVector.distance_to(listOfSlimes[i].distVector)
						print(closestDistanceFromChar)
						closestSlimeIndex = i

				self.model.sprites.append(HomingFireball(self.x + self.hitboxLeft, self.y + self.hitboxTop, self.model, listOfSlimes[closestSlimeIndex]))


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

class HomingFireball(Sprite):
	def __init__(self, xPos, yPos, model, targetSprite):
		super(HomingFireball, self).__init__(xPos, yPos, 47, 47, True, True, True)
		self.vert_vel = 5.0
		self.px = 0
		self.py = 0
		self.model = model
		self.targetSprite = targetSprite
		self.distVector = pygame.math.Vector2(self.x, self.y)
		
		# Load SpriteSheet
		if "fireballSpriteSheets" not in self.model.dictOfSpriteSheets.keys():
			self.model.dictOfSpriteSheets["fireballSpriteSheets"] = []
			for fileName in os.listdir("./Images/fireball"):
				self.model.dictOfSpriteSheets["fireballSpriteSheets"].append(SpriteSheet("./Images/fireball/" + fileName, 1, 1))

		self.currentSpriteSheet = self.model.dictOfSpriteSheets["fireballSpriteSheets"][0]
		
	def update(self):
		self.vert_vel += 1.0
		
		self.distVector.x = self.x + self.hitboxLeft
		self.distVector.y = self.y + self.hitboxTop
		
		if self.targetSprite.isActive == True:
			self.distVector.move_towards_ip(self.targetSprite.distVector, 5 + self.vert_vel)
			self.x = self.distVector.x
			self.y = self.distVector.y
		else:
			self.explode()
			self.isActive = False
		
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
		if isinstance(sprite, Fireball) or isinstance(sprite, HomingFireball) and self.isDying == False: # Eventually change to sprite category rather than Fireballs specifically		
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

