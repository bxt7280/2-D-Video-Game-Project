import pygame
import os
import random
import math
from Util import Direction, SpriteSheet, camera

class Sprite():
	def __init__(self, xPos, yPos, w, h, canCollideWithBorder, canCollideWithSprite):
		self.x = xPos 
		self.y = yPos
		self.px = 0
		self.py = 0 
		self.w = w
		self.h = h
		self.canCollideWithBorder = canCollideWithBorder
		self.canCollideWithSprite = canCollideWithSprite
		self.isActive = True 
		self.currentSpriteSheet = 0
		self.currentSpriteCellIndex = 0
		
		# Collision/Hitbox Offsets
		self.hitboxLeft = 0
		self.hitboxTop = 0
		self.hitboxW = 0
		self.hitboxH = 0
		
		# Booleans to determine direction sprite was moving when modulo calculation occurs
		self.moduloEventUp = False
		self.moduloEventDown = False		
		self.moduloEventLeft = False
		self.moduloEventRight = False

	def savePreviousCoordinates(self):
		self.px = self.x
		self.py = self.y	

	def calculateModuloEvents(self):
		# Determine what direction sprite was moving when crossing the border of the map
		if self.x < 0:			
			self.moduloEventLeft = True

		if self.x > self.model.currentMapSize[0]:
			self.moduloEventRight = True 

		self.x = self.x % self.model.currentMapSize[0] # Perform modulo operation due to map scrolling 

		if self.y < 0:
			self.moduloEventUp = True	

		if self.y > self.model.currentMapSize[1]:
			self.moduloEventDown = True	
		
		self.y = self.y % self.model.currentMapSize[1]

		# Reset modulo events if sprite crosses a certain point
		if self.x + self.w < self.model.currentMapSize[0] - self.model.currentMapSize[0] / 8:
			self.moduloEventLeft = False
		if self.x + self.w >= self.model.currentMapSize[0] - self.model.currentMapSize[0] / 8:
			self.moduloEventLeft = True

		if self.x > self.model.currentMapSize[0] / 8:
			self.moduloEventRight = False
		if self.x <= self.model.currentMapSize[0] / 8:
			self.moduloEventRight = True

		if self.y + self.h < self.model.currentMapSize[1] - self.model.currentMapSize[1] / 8:
			self.moduloEventUp = False
		if self.y + self.h >= self.model.currentMapSize[1] - self.model.currentMapSize[1] / 8:
			self.moduloEventUp = True

		if self.y > self.model.currentMapSize[1] / 8:
			self.moduloEventDown = False
		if self.y <= self.model.currentMapSize[1] / 8:
			self.moduloEventDown = True

class MainCharacter(Sprite):
	def __init__(self, xPos, yPos, model):
		super(MainCharacter, self).__init__(xPos, yPos, 256, 256, True, True)
		self.lightningAttackRecharge = 0
		self.lightningAttackOn = False
		self.autoFireballCooldown = 0
		self.autoFireballAttackOn = False 
		self.flyingSwordsAttackOn = False
		self.listOfActiveSwords = []
		self.direction = Direction.UP
		self.model = model
		self.collisionCount = 0
		self.pulsateRed = False
		self.hp = 300
		self.maxHp = self.hp
		
		# Collision/Hitbox parameters
		self.hitboxLeft = 105
		self.hitboxTop = 47
		self.hitboxW = -210
		self.hitboxH = -135
		
		# Load all SpriteSheets
		# Walk SpriteSheets
		self.model.dictOfSpriteSheets["girlWalkSpriteSheets"] = []
		for fileName in os.listdir("./Images/Girl/GirlSample_Walk_256Update"):
			self.model.dictOfSpriteSheets["girlWalkSpriteSheets"].append(SpriteSheet("./Images/Girl/GirlSample_Walk_256Update/" + fileName, 4, 3, self.model.screen))

		self.walkSpriteSheets = self.model.dictOfSpriteSheets["girlWalkSpriteSheets"]
		
		# Idle SpriteSheets
		self.model.dictOfSpriteSheets["girlIdleSpriteSheets"] = []
		for fileName in os.listdir("./Images/Girl/GirlSampleReadyIdle"):
			self.model.dictOfSpriteSheets["girlIdleSpriteSheets"].append(SpriteSheet("./Images/Girl/GirlSampleReadyIdle/" + fileName, 4, 4, self.model.screen))

		self.idleSpriteSheets = self.model.dictOfSpriteSheets["girlIdleSpriteSheets"]

		# Throw fireball SpriteSheets
		self.model.dictOfSpriteSheets["girlThrowFireSpriteSheets"] = []
		for fileName in os.listdir("./Images/Girl/GirlSampleFireball"):
			self.model.dictOfSpriteSheets["girlThrowFireSpriteSheets"].append(SpriteSheet("./Images/Girl/GirlSampleFireball/" + fileName, 4, 6, self.model.screen))

		self.throwFireSpriteSheets = self.model.dictOfSpriteSheets["girlThrowFireSpriteSheets"]

		# Set initial SpriteSheet
		self.currentSpriteSheet = self.idleSpriteSheets[5]

		# Create a vector to determine distance between sprites
		self.distVector = pygame.math.Vector2(self.x, self.y)

		# For red pulsating effect on mainCharacter
		self.currentAlpha = 255
		self.alphaDirectionSwitch = True

		# Center of hitbox
		self.hitboxRect =  pygame.Rect(self.x + self.hitboxLeft, self.y + self.hitboxTop, 
								self.w + self.hitboxW, self.h + self.hitboxH)

		self.hitboxCenter = self.hitboxRect.center
	
	def update(self):
		# Reset number of collisions
		self.collisionCount = 0

		# Update distVector to save current coordinates
		self.distVector.x = self.x + self.hitboxLeft
		self.distVector.y = self.y + self.hitboxTop

		# Update hitboxRect and hitboxCenter
		self.hitboxRect = pygame.Rect(self.x + self.hitboxLeft, self.y + self.hitboxTop, 
							self.w + self.hitboxW, self.h + self.hitboxH)
		
		self.hitboxCenter = self.hitboxRect.center

		# Lighting attack update
		if self.lightningAttackOn == True:
			self.lightningAttack()
			
			if self.lightningAttackRecharge > 0:
				self.lightningAttackRecharge -= 1

		# Auto fireball update
		if self.autoFireballAttackOn == True:
			if self.autoFireballCooldown > 0:
				self.autoFireballCooldown -= 1			
			self.autoFireball()

		# Flying swords update
		if self.flyingSwordsAttackOn == True and len(self.listOfActiveSwords) == 0:
			self.flyingSwordsAttack()
		elif self.flyingSwordsAttackOn == False:
			for sword in self.listOfActiveSwords:
				sword.isActive = False
			self.listOfActiveSwords.clear()

	def draw(self, screen):
		if self.pulsateRed == True:
			self.assignCurrentAlpha()
			self.currentSpriteSheet.drawWithAlpha(screen, self.currentSpriteCellIndex, self.x - camera.x, self.y - camera.y, 0, self.currentAlpha)
		else:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x - camera.x, self.y - camera.y)

		if self.model.mainCharacter.pulsateRed == False:
			self.currentAlpha = 255

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
		# Past the border, but previously on right hand side of the border
		if self.x + self.hitboxLeft <= 0 and self.px + self.hitboxLeft >= 0:
			self.x = 0 - self.hitboxLeft
		# Past the border, but previously above the border
		if self.y + self.hitboxTop + (self.h + self.hitboxH) >= screenSize[1] and self.py + self.hitboxTop + (self.h + self.hitboxH) <= screenSize[1]:
			self.y = screenSize[1] - self.hitboxTop - (self.h + self.hitboxH)
		# Past the border, but previously below the border
		if self.y + self.hitboxTop <= 0 and self.py + self.hitboxTop >= 0:
			self.y = 0 - self.hitboxTop

	def moveCharacter(self, dx, dy):
		if dx != 0:
			self.moveSingleAxis(dx, 0)
		if dy != 0:
			self.moveSingleAxis(0, dy)

	def moveSingleAxis(self, dx, dy):
		self.x += dx
		self.y += dy

		for sprite in self.model.obstacles:
			collisionOffsets = self.model.calculateCollisionOffsets(self, sprite)		
			collisionOffsetX = collisionOffsets[0]
			collisionOffsetY = collisionOffsets[1]
			spriteRect = pygame.Rect(sprite.x + sprite.hitboxLeft + collisionOffsetX, sprite.y + sprite.hitboxTop + collisionOffsetY, sprite.w + sprite.hitboxW, sprite.h + sprite.hitboxH)
			mainCharRect = pygame.Rect(self.x + self.hitboxLeft, self.y + self.hitboxTop, self.w + self.hitboxW, self.h + self.hitboxH)
			if mainCharRect.colliderect(spriteRect):
				if dx > 0: # Moving right; Hit the left side of the wall
					mainCharRect.right = spriteRect.left
					self.x = mainCharRect.x - self.hitboxLeft
				if dx < 0: # Moving left; Hit the right side of the wall
					mainCharRect.left = spriteRect.right
					self.x = mainCharRect.x - self.hitboxLeft
				if dy > 0: # Moving down; Hit the top side of the wall
					mainCharRect.bottom = spriteRect.top
					self.y = mainCharRect.y - self.hitboxTop
				if dy < 0: # Moving up; Hit the bottom side of the wall
					mainCharRect.top = spriteRect.bottom
					self.y = mainCharRect.y - self.hitboxTop

	def rectCollideWithSprite(self, sprite):
		if isinstance(sprite, Slime):
			self.collisionCount += 1
			if self.hp > 0:
				self.hp -= 1

		# # ORIGINAL SPRITE COLLISION
		# #In the sprite, but previously on left hand side of the sprite
		# if self.x + self.hitboxLeft + (self.w + self.hitboxW) >= sprite.x + sprite.hitboxLeft and self.px + self.hitboxLeft + (self.w + self.hitboxW) <= sprite.x + sprite.hitboxLeft:
		# 	self.x = sprite.x + sprite.hitboxLeft - self.hitboxLeft	- (self.w + self.hitboxW)	
		# # In the sprite, but previously on right hand side of the sprite
		# if self.x + self.hitboxLeft <= sprite.x + sprite.hitboxLeft + (sprite.w + sprite.hitboxW) and self.px + self.hitboxLeft >= sprite.x + sprite.hitboxLeft + (sprite.w + sprite.hitboxW):
		# 	self.x = sprite.x + sprite.hitboxLeft + (sprite.w + sprite.hitboxW) - self.hitboxLeft
		# # In the sprite, but previously above the sprite
		# if self.y + self.hitboxTop +(self.h + self.hitboxH) >= sprite.y + sprite.hitboxTop and self.py + self.hitboxTop + (self.h + self.hitboxH) <= sprite.y + sprite.hitboxTop:
		# 	self.y = sprite.y + sprite.hitboxTop - self.hitboxTop - (self.h + self.hitboxH)
		# # In the sprite, but previously below the sprite
		# if self.y + self.hitboxTop <= sprite.y + sprite.hitboxTop + (sprite.h + sprite.hitboxH) and self.py + self.hitboxTop >= sprite.y + sprite.hitboxTop + (sprite.h + sprite.hitboxH):
		# 	self.y = sprite.y + sprite.hitboxTop + (sprite.h + sprite.hitboxH) - self.hitboxTop
	
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
					if random.randrange(1, 15) == 5 and not(slime.isDying):
						slime.hitByLightning()
			self.lightningAttackRecharge = 30

	def autoFireball(self):
		if self.autoFireballCooldown == 0:
			self.autoFireballCooldown = 50
			listOfSlimes = [sprite for sprite in self.model.sprites if isinstance(sprite, Slime)]
			if len(listOfSlimes) > 0: 
				closestDistanceFromChar = 1000
				closestSlimeIndex = 0
				for i in range(len(listOfSlimes)):
					shortestDist = self.model.calculateDistanceOffsets(self, listOfSlimes[i])
					if self.distVector.distance_to((listOfSlimes[i].distVector.x + shortestDist[0], listOfSlimes[i].distVector.y + shortestDist[1])) < closestDistanceFromChar:
						closestDistanceFromChar = self.distVector.distance_to(listOfSlimes[i].distVector)
						closestSlimeIndex = i

				self.model.sprites.append(HomingFireball(self.x + self.hitboxLeft, self.y + self.hitboxTop, self.model, listOfSlimes[closestSlimeIndex]))

	def flyingSwordsAttack(self):
		self.listOfActiveSwords.append(FlyingSword(self.x + self.hitboxLeft + ((self.w + self.hitboxW) / 2),
											       self.y + self.hitboxTop + ((self.h + self.hitboxH) / 2), 0, 130, self.model))
		self.listOfActiveSwords.append(FlyingSword(self.x + self.hitboxLeft + ((self.w + self.hitboxW) / 2),
											       self.y + self.hitboxTop + ((self.h + self.hitboxH) / 2), 90, 130, self.model))
		self.listOfActiveSwords.append(FlyingSword(self.x + self.hitboxLeft + ((self.w + self.hitboxW) / 2), 
											       self.y + self.hitboxTop + ((self.h + self.hitboxH) / 2), 180, 130, self.model))
		self.listOfActiveSwords.append(FlyingSword(self.x + self.hitboxLeft + ((self.w + self.hitboxW) / 2), 
											       self.y + self.hitboxTop + ((self.h + self.hitboxH) / 2), 270, 130, self.model))
		self.model.spriteListBuffer.extend(self.listOfActiveSwords)

class Fireball(Sprite):
	def __init__(self, xPos, yPos, direction, model):
		super(Fireball, self).__init__(xPos, yPos, 47, 47, True, True)
		self.vert_vel = 5.0
		self.direction = direction
		self.model = model
		
		# Load SpriteSheet
		if "fireballSpriteSheets" not in self.model.dictOfSpriteSheets.keys():
			self.model.dictOfSpriteSheets["fireballSpriteSheets"] = []
			for fileName in os.listdir("./Images/fireball"):
				self.model.dictOfSpriteSheets["fireballSpriteSheets"].append(SpriteSheet("./Images/fireball/" + fileName, 1, 1, self.model.screen))

		self.currentSpriteSheet = self.model.dictOfSpriteSheets["fireballSpriteSheets"][0]
		
	def update(self):
		self.moveFireball()
		self.calculateModuloEvents()
		
	def draw(self, screen):
		# Follows same pattern as drawMap method in View Class
		# Center Image
		self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x - camera.x, self.y - camera.y)
	
		# Moving Right
		if camera.x + camera.width > self.model.currentMapSize[0]:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x + self.model.currentMapSize[0] - camera.x, self.y - camera.y)
		# Moving Left
		if camera.x < 0 + self.w: # added width of sprite so it doesn't disappear from screen when moving left
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x - self.model.currentMapSize[0] + -camera.x, self.y - camera.y)
		# Moving Up
		if camera.y < 0 + self.h:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x -camera.x, self.y - self.model.currentMapSize[1] - camera.y)
		# Moving Down
		if camera.y + camera.height > self.model.currentMapSize[1]:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x -camera.x, self.y + self.model.currentMapSize[1] - camera.y)

		# Diagonals
		# Right-Up
		if camera.x + camera.width > self.model.currentMapSize[0] and camera.y < 0 + self.h:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x + self.model.currentMapSize[0] - camera.x, self.y - self.model.currentMapSize[1] - camera.y)		
		# Right-Down
		if camera.x + camera.width > self.model.currentMapSize[0] and camera.y + camera.height > self.model.currentMapSize[1]:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x + self.model.currentMapSize[0] - camera.x, self.y + self.model.currentMapSize[1] - camera.y)			
		# Left-Up
		if camera.x < 0 + self.w and camera.y < 0 + self.h:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x - self.model.currentMapSize[0] + -camera.x, self.y - self.model.currentMapSize[1] - camera.y)		
		# Left-Down
		if camera.x < 0 + self.w and camera.y + camera.height > self.model.currentMapSize[1]:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x - self.model.currentMapSize[0] + -camera.x, self.y + self.model.currentMapSize[1] - camera.y)	
	
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

	def rectCollideWithSprite(self, sprite):
			if not(isinstance(sprite, MainCharacter)) and isinstance(sprite, Slime):
				self.isActive = False
				self.explode()		

	def explode(self):
		self.model.spriteListBuffer.append(FireballExplosion(self.x - 27, self.y - 25, self.model))

class HomingFireball(Sprite):
	def __init__(self, xPos, yPos, model, targetSprite):
		super(HomingFireball, self).__init__(xPos, yPos, 47, 47, True, True)
		self.vert_vel = 5.0
		self.model = model
		self.targetSprite = targetSprite
		self.distVector = pygame.math.Vector2(self.x, self.y)
		
		# Load SpriteSheet
		if "fireballSpriteSheets" not in self.model.dictOfSpriteSheets.keys():
			self.model.dictOfSpriteSheets["fireballSpriteSheets"] = []
			for fileName in os.listdir("./Images/fireball"):
				self.model.dictOfSpriteSheets["fireballSpriteSheets"].append(SpriteSheet("./Images/fireball/" + fileName, 1, 1, self.model.screen))

		self.currentSpriteSheet = self.model.dictOfSpriteSheets["fireballSpriteSheets"][0]
		
	def update(self):
		self.vert_vel += 1.0
		
		self.distVector.x = self.x + self.hitboxLeft
		self.distVector.y = self.y + self.hitboxTop
		
		if self.targetSprite.isActive == True:
			self.trackTarget()
		else:
			self.explode()
			self.isActive = False

	def draw(self, screen):
		# Follows same pattern as drawMap method in View Class
		# Center Image
		self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x - camera.x, self.y - camera.y)
	
		# Moving Right
		if camera.x + camera.width > self.model.currentMapSize[0]:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x + self.model.currentMapSize[0] - camera.x, self.y - camera.y)
		# Moving Left
		if camera.x < 0 + self.w: # added width of sprite so it doesn't disappear from screen when moving left
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x - self.model.currentMapSize[0] + -camera.x, self.y - camera.y)
		# Moving Up
		if camera.y < 0 + self.h:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x -camera.x, self.y - self.model.currentMapSize[1] - camera.y)
		# Moving Down
		if camera.y + camera.height > self.model.currentMapSize[1]:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x -camera.x, self.y + self.model.currentMapSize[1] - camera.y)

		# Diagonals
		# Right-Up
		if camera.x + camera.width > self.model.currentMapSize[0] and camera.y < 0 + self.h:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x + self.model.currentMapSize[0] - camera.x, self.y - self.model.currentMapSize[1] - camera.y)		
		# Right-Down
		if camera.x + camera.width > self.model.currentMapSize[0] and camera.y + camera.height > self.model.currentMapSize[1]:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x + self.model.currentMapSize[0] - camera.x, self.y + self.model.currentMapSize[1] - camera.y)			
		# Left-Up
		if camera.x < 0 + self.w and camera.y < 0 + self.h:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x - self.model.currentMapSize[0] + -camera.x, self.y - self.model.currentMapSize[1] - camera.y)		
		# Left-Down
		if camera.x < 0 + self.w and camera.y + camera.height > self.model.currentMapSize[1]:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x - self.model.currentMapSize[0] + -camera.x, self.y + self.model.currentMapSize[1] - camera.y)	
		
	def trackTarget(self):
		shortestDist = self.model.calculateDistanceOffsets(self, self.targetSprite)		
		targetDest = pygame.math.Vector2(self.targetSprite.distVector.x + shortestDist[0], self.targetSprite.distVector.y + shortestDist[1])
		
		self.distVector.move_towards_ip(targetDest, 5 + self.vert_vel)
		self.x = self.distVector.x
		self.y = self.distVector.y
		
		self.calculateModuloEvents()
	
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

	def rectCollideWithSprite(self, sprite):
			if not(isinstance(sprite, MainCharacter)) and isinstance(sprite, Slime):
				self.isActive = False
				self.explode()		

	def explode(self):
		self.model.spriteListBuffer.append(FireballExplosion(self.x - 27, self.y - 25, self.model))

class FireballExplosion(Sprite):
	def __init__(self, xPos, yPos, model):
		super(FireballExplosion, self).__init__(xPos, yPos, 96, 96, False, False)
		self.model = model
	
		# Load all SpriteSheets
		if "fireballExplosionSpriteSheets" not in self.model.dictOfSpriteSheets.keys():
			self.model.dictOfSpriteSheets["fireballExplosionSpriteSheets"] = []
			for fileName in os.listdir("./Images/stylized_explosion_001_small_yellow"):
				self.model.dictOfSpriteSheets["fireballExplosionSpriteSheets"].append(SpriteSheet("./Images/stylized_explosion_001_small_yellow/" + fileName, 9, 1, self.model.screen))

		self.explodeSpriteSheets = self.model.dictOfSpriteSheets["fireballExplosionSpriteSheets"]

		self.currentSpriteSheet = self.explodeSpriteSheets[0]
		
	def update(self):
		self.animate()

	def draw(self, screen):
		# Follows same pattern as drawMap method in View Class
		# Center Image
		self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x - camera.x, self.y - camera.y)
	
		# Moving Right
		if camera.x + camera.width > self.model.currentMapSize[0]:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x + self.model.currentMapSize[0] - camera.x, self.y - camera.y)
		# Moving Left
		if camera.x < 0 + self.w: # added width of sprite so it doesn't disappear from screen when moving left
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x - self.model.currentMapSize[0] + -camera.x, self.y - camera.y)
		# Moving Up
		if camera.y < 0 + self.h:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x -camera.x, self.y - self.model.currentMapSize[1] - camera.y)
		# Moving Down
		if camera.y + camera.height > self.model.currentMapSize[1]:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x -camera.x, self.y + self.model.currentMapSize[1] - camera.y)

		# Diagonals
		# Right-Up
		if camera.x + camera.width > self.model.currentMapSize[0] and camera.y < 0 + self.h:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x + self.model.currentMapSize[0] - camera.x, self.y - self.model.currentMapSize[1] - camera.y)		
		# Right-Down
		if camera.x + camera.width > self.model.currentMapSize[0] and camera.y + camera.height > self.model.currentMapSize[1]:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x + self.model.currentMapSize[0] - camera.x, self.y + self.model.currentMapSize[1] - camera.y)			
		# Left-Up
		if camera.x < 0 + self.w and camera.y < 0 + self.h:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x - self.model.currentMapSize[0] + -camera.x, self.y - self.model.currentMapSize[1] - camera.y)		
		# Left-Down
		if camera.x < 0 + self.w and camera.y + camera.height > self.model.currentMapSize[1]:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x - self.model.currentMapSize[0] + -camera.x, self.y + self.model.currentMapSize[1] - camera.y)	
		
	def animate(self):
		self.currentSpriteCellIndex += 1
			
		if self.currentSpriteCellIndex > 8:
			self.currentSpriteCellIndex = 0
			self.isActive = False

class LightningBolt(Sprite):
	def __init__(self, xPos, yPos, model, target):
		super(LightningBolt, self).__init__(xPos, yPos, 128, 256, False, False)
		self.model = model
		self.animateDuration = 4
		self.target = target
	
		# Load all SpriteSheets
		if "lightningBoltSpriteSheets" not in self.model.dictOfSpriteSheets.keys():
			self.model.dictOfSpriteSheets["lightningBoltSpriteSheets"] = []
			for fileName in os.listdir("./Images/lightning"):
				self.model.dictOfSpriteSheets["lightningBoltSpriteSheets"].append(SpriteSheet("./Images/lightning/" + fileName, 5, 1, self.model.screen))

		self.lightningBoltSpriteSheets = self.model.dictOfSpriteSheets["lightningBoltSpriteSheets"]

		self.currentSpriteSheet = self.lightningBoltSpriteSheets[0]
		
	def update(self):
		self.x = self.target.x - 34
		self.y = self.target.y - 220
		self.animate()

	def draw(self, screen):
		# Follows same pattern as drawMap method in View Class
		# Center Image
		self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x - camera.x, self.y - camera.y)
	
		# Moving Right
		if camera.x + camera.width > self.model.currentMapSize[0]:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x + self.model.currentMapSize[0] - camera.x, self.y - camera.y)
		# Moving Left
		if camera.x < 0 + self.w: # added width of sprite so it doesn't disappear from screen when moving left
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x - self.model.currentMapSize[0] + -camera.x, self.y - camera.y)
		# Moving Up
		if camera.y < 0 + self.h:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x -camera.x, self.y - self.model.currentMapSize[1] - camera.y)
		# Moving Down
		if camera.y + camera.height > self.model.currentMapSize[1]:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x -camera.x, self.y + self.model.currentMapSize[1] - camera.y)

		# Diagonals
		# Right-Up
		if camera.x + camera.width > self.model.currentMapSize[0] and camera.y < 0 + self.h:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x + self.model.currentMapSize[0] - camera.x, self.y - self.model.currentMapSize[1] - camera.y)		
		# Right-Down
		if camera.x + camera.width > self.model.currentMapSize[0] and camera.y + camera.height > self.model.currentMapSize[1]:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x + self.model.currentMapSize[0] - camera.x, self.y + self.model.currentMapSize[1] - camera.y)			
		# Left-Up
		if camera.x < 0 + self.w and camera.y < 0 + self.h:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x - self.model.currentMapSize[0] + -camera.x, self.y - self.model.currentMapSize[1] - camera.y)		
		# Left-Down
		if camera.x < 0 + self.w and camera.y + camera.height > self.model.currentMapSize[1]:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x - self.model.currentMapSize[0] + -camera.x, self.y + self.model.currentMapSize[1] - camera.y)	
		
	def animate(self):
		self.currentSpriteCellIndex += 1
			
		if self.currentSpriteCellIndex > 4:
			self.currentSpriteCellIndex = 0
			self.animateDuration -= 1
			
		if self.animateDuration == 0:
			self.isActive = False

class BloodSplatter(Sprite):
	def __init__(self, xPos, yPos, model):
		super(BloodSplatter, self).__init__(xPos, yPos, 64, 64, False, False)
		self.model = model
	
		# Load all SpriteSheets
		if "bloodSplatterSpriteSheets" not in self.model.dictOfSpriteSheets.keys():
			self.model.dictOfSpriteSheets["bloodSplatterSpriteSheets"] = []
			for fileName in os.listdir("./Images/bloodSplatter"):
				self.model.dictOfSpriteSheets["bloodSplatterSpriteSheets"].append(SpriteSheet("./Images/bloodSplatter/" + fileName, 10, 1, self.model.screen))

		self.bloodSplatterSpriteSheets = self.model.dictOfSpriteSheets["bloodSplatterSpriteSheets"]

		self.currentSpriteSheet = self.bloodSplatterSpriteSheets[0]
		
	def update(self):
		self.animate()

	def draw(self, screen):
		# Follows same pattern as drawMap method in View Class
		# Center Image
		self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x - camera.x, self.y - camera.y)
	
		# Moving Right
		if camera.x + camera.width > self.model.currentMapSize[0]:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x + self.model.currentMapSize[0] - camera.x, self.y - camera.y)
		# Moving Left
		if camera.x < 0 + self.w: # added width of sprite so it doesn't disappear from screen when moving left
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x - self.model.currentMapSize[0] + -camera.x, self.y - camera.y)
		# Moving Up
		if camera.y < 0 + self.h:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x -camera.x, self.y - self.model.currentMapSize[1] - camera.y)
		# Moving Down
		if camera.y + camera.height > self.model.currentMapSize[1]:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x -camera.x, self.y + self.model.currentMapSize[1] - camera.y)

		# Diagonals
		# Right-Up
		if camera.x + camera.width > self.model.currentMapSize[0] and camera.y < 0 + self.h:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x + self.model.currentMapSize[0] - camera.x, self.y - self.model.currentMapSize[1] - camera.y)		
		# Right-Down
		if camera.x + camera.width > self.model.currentMapSize[0] and camera.y + camera.height > self.model.currentMapSize[1]:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x + self.model.currentMapSize[0] - camera.x, self.y + self.model.currentMapSize[1] - camera.y)			
		# Left-Up
		if camera.x < 0 + self.w and camera.y < 0 + self.h:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x - self.model.currentMapSize[0] + -camera.x, self.y - self.model.currentMapSize[1] - camera.y)		
		# Left-Down
		if camera.x < 0 + self.w and camera.y + camera.height > self.model.currentMapSize[1]:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x - self.model.currentMapSize[0] + -camera.x, self.y + self.model.currentMapSize[1] - camera.y)	
		
	def animate(self):
		self.currentSpriteCellIndex += 1
			
		if self.currentSpriteCellIndex > 9:
			self.currentSpriteCellIndex = 0
			self.isActive = False

class Slime(Sprite):
	def __init__(self, xPos, yPos, model):
		super(Slime, self).__init__(xPos, yPos, 64, 64, True, True)
		self.model = model
		self.provoked = False
		self.provokedCounter = 0
		self.isHurt = False
		self.isHurtCounter = 0
		self.isDying = False
		self.deathCounter = 0

		# Single image used for mask collision
		if "slimeSingleImage" not in self.model.dictOfSingleImages.keys():
			self.model.dictOfSingleImages["slimeSingleImage"] = pygame.image.load("./Images/slimeSingleImage.png").convert_alpha()
			
		self.image = self.model.dictOfSingleImages["slimeSingleImage"]
		
		# Save original position as vector
		self.originalPos = pygame.math.Vector2(self.x, self.y)
	
		# Load all SpriteSheets
		if "slimeSpriteSheets" not in self.model.dictOfSpriteSheets.keys():
			self.model.dictOfSpriteSheets["slimeSpriteSheets"] = []
			for fileName in os.listdir("./Images/slime"):
				self.model.dictOfSpriteSheets["slimeSpriteSheets"].append(SpriteSheet("./Images/slime/" + fileName, 5, 3, self.model.screen))

		self.slimeSpriteSheets = self.model.dictOfSpriteSheets["slimeSpriteSheets"]

		self.currentSpriteSheet = self.slimeSpriteSheets[0]
		
		self.frameDelayCounter = 2 # slow down rate of animation

		self.distVector = pygame.math.Vector2(self.x, self.y) # Vector used to follow mainCharacter

		# Properties for circle based collision
		# Determine center of hitbox
		self.hitboxRect = pygame.Rect(self.x + self.hitboxLeft, self.y + self.hitboxTop, 
										self.w + self.hitboxW, self.h + self.hitboxH)
		
		self.hitboxCenter = self.hitboxRect.center
		self.radius = 30

	def update(self):
		# Update distance vector
		self.distVector.x = self.x + self.hitboxLeft
		self.distVector.y = self.y + self.hitboxTop
	
		self.trackMainCharacter()

		# Update hitboxRect and hitboxCenter
		self.hitboxRect = pygame.Rect(self.x + self.hitboxLeft, self.y + self.hitboxTop, 
							self.w + self.hitboxW, self.h + self.hitboxH)
		
		self.hitboxCenter = self.hitboxRect.center
		
		# Death if hit by lightning
		if self.isDying == True:
			if self.deathCounter == 0:
				self.bleed()
				self.isActive = False
			self.deathCounter -= 1

		self.animate()

	def draw(self, screen):
		# Follows same pattern as drawMap method in View Class
		# Center Image
		self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x - camera.x, self.y - camera.y)
	
		# Moving Right
		if camera.x + camera.width > self.model.currentMapSize[0]:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x + self.model.currentMapSize[0] - camera.x, self.y - camera.y)
		# Moving Left
		if camera.x < 0 + self.w: # added width of sprite so it doesn't disappear from screen when moving left
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x - self.model.currentMapSize[0] + -camera.x, self.y - camera.y)
		# Moving Up
		if camera.y < 0 + self.h:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x -camera.x, self.y - self.model.currentMapSize[1] - camera.y)
		# Moving Down
		if camera.y + camera.height > self.model.currentMapSize[1]:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x -camera.x, self.y + self.model.currentMapSize[1] - camera.y)

		# Diagonals
		# Right-Up
		if camera.x + camera.width > self.model.currentMapSize[0] and camera.y < 0 + self.h:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x + self.model.currentMapSize[0] - camera.x, self.y - self.model.currentMapSize[1] - camera.y)		
		# Right-Down
		if camera.x + camera.width > self.model.currentMapSize[0] and camera.y + camera.height > self.model.currentMapSize[1]:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x + self.model.currentMapSize[0] - camera.x, self.y + self.model.currentMapSize[1] - camera.y)			
		# Left-Up
		if camera.x < 0 + self.w and camera.y < 0 + self.h:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x - self.model.currentMapSize[0] + -camera.x, self.y - self.model.currentMapSize[1] - camera.y)		
		# Left-Down
		if camera.x < 0 + self.w and camera.y + camera.height > self.model.currentMapSize[1]:
			self.currentSpriteSheet.draw(screen, self.currentSpriteCellIndex, self.x - self.model.currentMapSize[0] + -camera.x, self.y + self.model.currentMapSize[1] - camera.y)	

	def trackMainCharacter(self):
		shortestDist = self.model.calculateDistanceOffsets(self, self.model.mainCharacter)
				
		targetDest = pygame.math.Vector2(self.model.mainCharacter.distVector.x + shortestDist[0], self.model.mainCharacter.distVector.y + shortestDist[1])
		
		self.distVector.move_towards_ip(targetDest, 3)
		self.x = self.distVector.x
		self.y = self.distVector.y

		self.calculateModuloEvents()
		
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

	def rectCollideWithSprite(self, sprite):
		if isinstance(sprite, Fireball) or isinstance(sprite, HomingFireball) and self.isDying == False: 		
			self.isHurt = True
			self.isHurtCounter = 20
			self.provoked = True
			self.provokedCounter = 150
			self.isDying = True
			self.deathCounter = 20

	def circleCollideWithSprite(self, sprite, depth = None, normal = None):
		if isinstance(sprite, Slime):
			# Minimum translation vector. Distance and direction to separate sprites
			mtv = depth * normal
			# Move both sprites apart by half the distance they intersect
			self.move(-mtv / 2.0)
			sprite.move(mtv / 2.0)

	def move(self, amount):
		self.distVector += amount
		self.x = self.distVector.x
		self.y = self.distVector.y
		self.calculateModuloEvents()

	def maskCollideWithSprite(self, sprite):
		if isinstance(sprite, FlyingSword) and self.isDying == False: 	
			self.isHurt = True
			self.isHurtCounter = 20
			self.provoked = True
			self.provokedCounter = 150
			self.isDying = True
			self.deathCounter = 20

	def hitByLightning(self):
		self.model.spriteListBuffer.append(LightningBolt(self.x - 34, self.y - 220 , self.model, self))
		self.isHurt = True
		self.isHurtCounter = 20
		self.isDying = True
		self.deathCounter = 20

	def bleed(self):
		self.model.spriteListBuffer.append(BloodSplatter(self.x, self.y, self.model))
	
class FlyingSword(Sprite):
	def __init__(self, xPos, yPos, startingAngle, lengthFromPivot, model):
		super(FlyingSword, self).__init__(xPos, yPos, 124, 23, False, True)
		self.distVector = pygame.math.Vector2(self.x, self.y)
		self.borderRect = pygame.Rect(xPos, yPos, 124, 23)
		self.currentAlpha = 255
		self.alphaDirectionSwitch = True
		self.model = model

		self.lengthFromPivot = lengthFromPivot
		self.startingAngle = startingAngle

		self.pivot = pygame.Vector2(xPos, yPos)
		self.angle = 0

		self.offset = pygame.Vector2()
		self.offset.from_polar((lengthFromPivot, -self.startingAngle))

		self.pos = self.pivot + self.offset

		if "flyingSword" not in self.model.dictOfSingleImages.keys():
			self.model.dictOfSingleImages["flyingSword"] = pygame.image.load("./Images/flyingSword/flyingSword.png").convert_alpha()
		
		self.imageOrig = self.model.dictOfSingleImages["flyingSword"] 
		self.image = self.imageOrig

		self.modifiedImage = pygame.transform.rotate(self.image, startingAngle)

		self.image, self.rect = self.rotate_on_pivot(self.modifiedImage, self.angle, self.pivot, self.pos)
		
	def update(self):
		self.angle += 4
		self.pivot = pygame.Vector2(self.model.mainCharacter.x + self.model.mainCharacter.hitboxLeft + ((self.model.mainCharacter.w + self.model.mainCharacter.hitboxW) / 2), self.model.mainCharacter.y + self.model.mainCharacter.hitboxTop + ((self.model.mainCharacter.h + self.model.mainCharacter.hitboxH) / 2))
		self.offset = pygame.Vector2()
		self.offset.from_polar((self.lengthFromPivot, -self.startingAngle))
		self.pos = self.pivot + self.offset

		self.image, self.rect = self.rotate_on_pivot(self.modifiedImage, self.angle, self.pivot, self.pos)
		
		self.x = self.rect.x
		self.y = self.rect.y
		self.w = self.rect.w
		self.h = self.rect.h
		self.distVector.x = self.x
		self.distVector.y = self.y

	def draw(self, screen):
		mask = pygame.mask.from_surface(self.image)
		greenSilhouette = mask.to_surface(setcolor="green", unsetcolor=None)
		screen.blit(greenSilhouette, (self.rect.x - camera.x, self.rect.y - camera.y, self.rect.width, self.rect.height))
		
		self.assignCurrentAlpha()
		self.image.set_alpha(self.currentAlpha)
		screen.blit(self.image, (self.rect.x - camera.x, self.rect.y - camera.y, self.rect.width, self.rect.height))

	def rectCollideWithSprite(self, sprite):
		pass	

	def assignCurrentAlpha(self):
		if self.alphaDirectionSwitch == True:
			if self.currentAlpha <= 100:
				self.alphaDirectionSwitch = False
			else:
				self.currentAlpha -= 5
		else:
			if self.currentAlpha >= 255:
				self.alphaDirectionSwitch = True
			else:
				self.currentAlpha += 5

	def rotate_on_pivot(self, image, angle, pivot, origin):	
		surf = pygame.transform.rotate(image, angle)
		
		offset = pivot + (origin - pivot).rotate(-angle)
		rect = surf.get_rect(center = offset)
		
		return surf, rect

# Imageless sprite used for invisible boundaries
class Obstacle(Sprite):
	def __init__(self, xPos, yPos, width, height):
		super(Obstacle, self).__init__(xPos, yPos, width, height, False, True)
		self.hitboxLeft = 0
		self.hitboxTop = 0
		self.hitboxW = 0
		self.hitboxH = 0

		self.hitboxRect = pygame.Rect(self.x + self.hitboxLeft, self.y + self.hitboxTop, 
								self.w + self.hitboxW, self.h + self.hitboxH)
	def update(self):
		pass

