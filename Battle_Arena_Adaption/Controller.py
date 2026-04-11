import pygame
from pygame.locals import *
from Util import Direction

class Controller():
	def __init__(self, model):
		self.model = model
		self.keepGoing = True
		self.editorToggle = True
		self.spriteToBeDrawn = 0

	def update(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				self.keepGoing = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.keepGoing = False
				# Hitbox Mode ON/OFF
				if event.key == K_h:
					self.model.hitBoxModeOn = not self.model.hitBoxModeOn
				# Lightning Mode ON/OFF
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
		# Get list of all keys being pressed
		keys = pygame.key.get_pressed()
		
		# Throw Fireball 
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