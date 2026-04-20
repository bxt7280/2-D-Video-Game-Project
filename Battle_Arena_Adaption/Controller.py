import pygame, sys
from pygame.locals import *
from Util import Direction
from Sprites import *

class Controller():
	def __init__(self, model, view):
		self.model = model
		self.view = view
		self.keepGoing = True
		self.editorToggle = True
		self.spriteSelectorOn = False
		self.spriteToBeDrawn = dictOfSpriteClasses["Slime"]


	def update(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				self.keepGoing = False
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.keepGoing = False

				if self.spriteSelectorOn:
					if event.key == K_RETURN:
						self.spriteSelectorOn = False
						self.view.displayTextSpriteSelect = False
						print("Sprite Select Off")
						if self.view.user_text in dictOfSpriteClasses.keys():
							print("Sprite Changed")
							self.spriteToBeDrawn = dictOfSpriteClasses[self.view.user_text]
							self.view.user_text = ""
						else:
							print("Invalid Sprite")
							self.view.user_text = ""

					if event.key == K_BACKSPACE:
						self.view.user_text = self.view.user_text[0:-1]
					elif event.key != K_RETURN:
						self.view.user_text += event.unicode
				else:
					# Hitbox Mode ON/OFF
					if event.key == K_h:
						self.model.hitBoxModeOn = not self.model.hitBoxModeOn
					# Lightning Mode ON/OFF
					if event.key == K_SPACE:
						self.model.mainCharacter.lightningAttackOn = not self.model.mainCharacter.lightningAttackOn
					# Auto Fireball ON/OFF
					if event.key == K_f:
						self.model.mainCharacter.autoFireballAttackOn = not self.model.mainCharacter.autoFireballAttackOn 
					# Flying Swords ON/OFF
					if event.key == K_a:
						self.model.mainCharacter.flyingSwordsAttackOn = not self.model.mainCharacter.flyingSwordsAttackOn	
					if event.key == K_m:
						self.editorToggle = not(self.editorToggle)
					if event.key == K_s:
						self.spriteSelectorOn = True
						self.view.displayTextSpriteSelect = True
						print("Sprite Select On")

			# Map Editor Mode
			elif event.type == pygame.MOUSEBUTTONUP:
				self.addOrDeleteSprite()
					
		
		self.evaluateKeyPress()

	def addOrDeleteSprite(self):
		x, y = pygame.mouse.get_pos()
		if self.editorToggle == True and len(self.model.sprites) > 0:
			spriteClicked = None
			for sprite in self.model.sprites:
				if self.model.spriteClicked(sprite, x, y):
					spriteClicked = sprite
					pass

			if spriteClicked != None and not(isinstance(spriteClicked, MainCharacter)):
				self.model.sprites.remove(spriteClicked)
			else:
				self.model.sprites.append(self.spriteToBeDrawn(x, y, self.model))

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

# Dictionary of sprite classes to dynamically instantiate sprites during runtime
dictOfSpriteClasses = {
	"Slime": Slime,
	"FireballExplosion": FireballExplosion,
	"LightningBolt": LightningBolt
	}