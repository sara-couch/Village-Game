
from config import *
from dialogue import *
import pygame
import random
import math
import json


with open("dialogue.json") as f:
    npc_dialogue = json.load(f)

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        
        self.game=game
        self._layer=player_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x*tileSize
        self.y = y*tileSize
        
        
        self.width  = tileSize
        self.height = tileSize
        
        self.x_change=0
        self.y_change=0
        
        self.animationCounter = 0
        
        self.image = self.game.player_spritesheet.get_image(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.direction = "down"
        
    def move(self):
        pressed = pygame.key.get_pressed()
            
        if pressed[pygame.K_LEFT]:
            self.x_change = self.x_change - player_steps
            self.direction = "left"
                
        elif pressed[pygame.K_RIGHT]:
            self.x_change = self.x_change + player_steps
            self.direction = "right"
                
        elif pressed[pygame.K_UP]:
            self.y_change = self.y_change - player_steps
            self.direction = "up"
                
        elif pressed[pygame.K_DOWN]:
            self.y_change = self.y_change + player_steps
            self.direction = "down"
                
    def update(self):
        self.move()
        self.animation()
        self.rect.x = self.rect.x + self.x_change
        self.rect.y = self.rect.y + self.y_change
        self.collide_scenery()
        self.collide_npcs()        

        self.x_change=0
        self.y_change=0
        
        
    def animation(self):
        
        self.downAnimation = [self.game.player_spritesheet.get_image(0,0, self.width, self.height),
                         self.game.player_spritesheet.get_image(32,0, self.width, self.height),
                         self.game.player_spritesheet.get_image(64,0, self.width, self.height),]
        
        self.leftAnimation = [self.game.player_spritesheet.get_image(0,32, self.width, self.height),
                         self.game.player_spritesheet.get_image(32,32, self.width, self.height),
                         self.game.player_spritesheet.get_image(64,32, self.width, self.height),]
        
        self.rightAnimation = [self.game.player_spritesheet.get_image(0,64, self.width, self.height),
                         self.game.player_spritesheet.get_image(32,64, self.width, self.height),
                         self.game.player_spritesheet.get_image(64,64, self.width, self.height),]
        
        self.upAnimation = [self.game.player_spritesheet.get_image(0,96, self.width, self.height),
                         self.game.player_spritesheet.get_image(32,96, self.width, self.height),
                         self.game.player_spritesheet.get_image(64,96, self.width, self.height),]
        
        
        
        if self.direction == "down":
            if self.y_change==0:
                self.image = self.game.player_spritesheet.get_image(0,0, self.width, self.height)
            else:
                self.image = self.downAnimation[math.floor(self.animationCounter)]
                self.animationCounter += 0.2
                if self.animationCounter >= 3:
                    self.animationCounter=0
                    
        if self.direction == "left":
            if self.x_change==0:
                self.image = self.game.player_spritesheet.get_image(0,32, self.width, self.height)
            else:
                self.image = self.leftAnimation[math.floor(self.animationCounter)]
                self.animationCounter += 0.2
                if self.animationCounter >= 3:
                    self.animationCounter=0
                    
                    
        if self.direction == "right":
            if self.x_change==0:
                self.image = self.game.player_spritesheet.get_image(0,64, self.width, self.height)
            else:
                self.image = self.rightAnimation[math.floor(self.animationCounter)]
                self.animationCounter += 0.2
                if self.animationCounter >= 3:
                    self.animationCounter=0

        if self.direction == "up":
            if self.y_change==0:
                self.image = self.game.player_spritesheet.get_image(0,96, self.width, self.height)
            else:
                self.image = self.upAnimation[math.floor(self.animationCounter)]
                self.animationCounter += 0.2
                if self.animationCounter >= 3:
                    self.animationCounter=0 
                    
    def collide_scenery(self):
        pressed= pygame.key.get_pressed()
        collide=pygame.sprite.spritecollide(self, self.game.scenery, False, pygame.sprite.collide_rect_ratio(0.85))
        if collide:
            self.game.scenery_collided=True
            if pressed[pygame.K_LEFT]:
                self.rect.x += player_steps
            elif pressed[pygame.K_RIGHT]:
                self.rect.x -= player_steps
            elif pressed[pygame.K_UP]:
                self.rect.y += player_steps
            elif pressed[pygame.K_DOWN]:
                self.rect.y -= player_steps
        else:
            self.game.scenery_collided=False
                
    def collide_npcs(self):
        pressed= pygame.key.get_pressed()
        collide=pygame.sprite.spritecollide(self, self.game.npcs, False, pygame.sprite.collide_rect_ratio(0.85))
        if collide:
            
            #self.game.dialogue.show("Hello there! I'm an NPC.")
            self.game.npc_collided=True
            if pressed[pygame.K_LEFT]:
                self.rect.x += player_steps
            elif pressed[pygame.K_RIGHT]:
                self.rect.x -= player_steps
            elif pressed[pygame.K_UP]:
                self.rect.y += player_steps
            elif pressed[pygame.K_DOWN]:
                self.rect.y -= player_steps
        else:
            self.game.npc_collided=False
        for npc in collide:
           if npc.name in npc_dialogue:
            self.game.dialogue.show(npc_dialogue[npc.name][0])             

            
class NPC(pygame.sprite.Sprite):
    def __init__(self, game, x, y, name="NPC"):
        
        self.game=game
        self.name = name
        self._layer=player_layer
        self.groups = self.game.all_sprites, self.game.npcs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x*tileSize
        self.y = y*tileSize
        

        self.width  = tileSize
        self.height = tileSize
        
        self.x_change=0
        self.y_change=0
        
        self.animationCounter = 0
        
        
        self.character_index=0
        if name == "Alice":
            self.character_index=0
        elif name == "Samuel":
            self.character_index=96
            
            
            
        self.image = self.game.npc_spritesheet.get_image(self.character_index, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y 
        
        self.direction = random.choice(['left', 'right', 'up', 'down'])
        self.numberSteps = random.choice([30,40,50,60,70,120])
        self.stallSteps = random.choice([120,140,150,60,70,80])
        self.currentSteps = 0
        
        self.state="moving"
        
        
        
        
    def move(self):
        if self.state=="moving":
            if self.direction == "left":
                self.x_change = self.x_change - npc_steps
                self.currentSteps += 1
                
            elif self.direction == "right":
                self.x_change = self.x_change + npc_steps
                self.currentSteps += 1        
            
            elif self.direction == "up":
                self.y_change = self.y_change - npc_steps
                self.currentSteps += 1
            
            elif self.direction == "down":
                self.y_change = self.y_change + npc_steps  
                self.currentSteps += 1
        elif self.state == "stalling":
            self.currentSteps +=1
            if self.currentSteps == self.stallSteps:
                self.state="moving"
                self.currentSteps=0
                self.direction = random.choice(['left', 'right', 'up', 'down'])
                
        
    def update(self):
        self.move()
        self.animation()
        self.rect.x = self.rect.x + self.x_change
        self.rect.y = self.rect.y + self.y_change
        self.collide_scenery()
        self.x_change=0
        self.y_change=0  
        if self.currentSteps == self.numberSteps:
            if self.state !="stalling":
                self.currentSteps=0
            self.state="stalling"
        
    def animation(self):
        
        self.downAnimation = [self.game.npc_spritesheet.get_image(self.character_index,0, self.width, self.height),
                         self.game.npc_spritesheet.get_image((self.character_index+32),0, self.width, self.height),
                         self.game.npc_spritesheet.get_image((self.character_index+64),0, self.width, self.height),]
        
        self.leftAnimation = [self.game.npc_spritesheet.get_image(self.character_index,32, self.width, self.height),
                         self.game.npc_spritesheet.get_image((self.character_index+32),32, self.width, self.height),
                         self.game.npc_spritesheet.get_image((self.character_index+64),32, self.width, self.height),]
        
        self.rightAnimation = [self.game.npc_spritesheet.get_image(self.character_index,64, self.width, self.height),
                         self.game.npc_spritesheet.get_image((self.character_index+32),64, self.width, self.height),
                         self.game.npc_spritesheet.get_image((self.character_index+64),64, self.width, self.height),]
        
        self.upAnimation = [self.game.npc_spritesheet.get_image(self.character_index,96, self.width, self.height),
                         self.game.npc_spritesheet.get_image((self.character_index+32),96, self.width, self.height),
                         self.game.npc_spritesheet.get_image((self.character_index+64),96, self.width, self.height),]
        
        
        
        if self.direction == "down":
            if self.y_change==0:
                self.image = self.game.npc_spritesheet.get_image(self.character_index,0, self.width, self.height)
            else:
                self.image = self.downAnimation[math.floor(self.animationCounter)]
                self.animationCounter += 0.2
                if self.animationCounter >= 3:
                    self.animationCounter=0
                    
        if self.direction == "left":
            if self.x_change==0:
                self.image = self.game.npc_spritesheet.get_image(self.character_index,32, self.width, self.height)
            else:
                self.image = self.leftAnimation[math.floor(self.animationCounter)]
                self.animationCounter += 0.2
                if self.animationCounter >= 3:
                    self.animationCounter=0
                    
                    
        if self.direction == "right":
            if self.x_change==0:
                self.image = self.game.npc_spritesheet.get_image(self.character_index,64, self.width, self.height)
            else:
                self.image = self.rightAnimation[math.floor(self.animationCounter)]
                self.animationCounter += 0.2
                if self.animationCounter >= 3:
                    self.animationCounter=0

        if self.direction == "up":
            if self.y_change==0:
                self.image = self.game.npc_spritesheet.get_image(self.character_index,96, self.width, self.height)
            else:
                self.image = self.upAnimation[math.floor(self.animationCounter)]
                self.animationCounter += 0.2
                if self.animationCounter >= 3:
                    self.animationCounter=0        
        
    def collide_scenery(self):
        pressed= pygame.key.get_pressed()
        collide=pygame.sprite.spritecollide(self, self.game.scenery, False, pygame.sprite.collide_rect_ratio(0.85))
        if collide:
            if self.direction == "left":
                self.rect.x += npc_steps
            elif self.direction == "right":
                self.rect.x -= npc_steps
            elif self.direction == "up":
                self.rect.y += npc_steps
            elif self.direction == "down":
                self.rect.y -= npc_steps        
        
class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        
        self.game=game
        self._layer=blocks_layer
        self.groups = self.game.all_sprites, self.game.scenery
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x*tileSize
        self.y = y*tileSize
        
        
        self.width  = tileSize
        self.height = tileSize
        
        self.image = self.game.terrain_spritesheet.get_image(64,16, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        
        self.game=game
        self._layer=ground_layer
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x*tileSize
        self.y = y*tileSize
        
        
        self.width  = tileSize
        self.height = tileSize
        
        self.image = self.game.terrain_spritesheet.get_image(112,144, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        
class Water(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        
        self.game=game
        self._layer=water_layer
        self.groups = self.game.all_sprites, self.game.scenery
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x*tileSize
        self.y = y*tileSize
        
        
        self.width  = tileSize
        self.height = tileSize
        
        self.image = self.game.terrain_spritesheet.get_image(490,333, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        
class Cliff(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        
        self.game=game
        self._layer=cliff_layer
        self.groups = self.game.all_sprites, self.game.scenery
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x*tileSize
        self.y = y*tileSize
        
        
        self.width  = tileSize
        self.height = tileSize
        
        self.image = self.game.terrain_spritesheet.get_image(69,144, 44, 96)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
class WaterEdgeRight(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        
        self.game=game
        self._layer=ground_layer
        self.groups = self.game.all_sprites, self.game.scenery
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x*tileSize
        self.y = y*tileSize
        
        
        self.width  = tileSize
        self.height = tileSize
        
        self.image = self.game.terrain_spritesheet.get_image(527,333, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
class WaterEdgeDown(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        
        self.game=game
        self._layer=ground_layer
        self.groups = self.game.all_sprites, self.game.scenery
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x*tileSize
        self.y = y*tileSize
        
        
        self.width  = tileSize
        self.height = tileSize
        
        self.image = self.game.terrain_spritesheet.get_image(563,333, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
class WaterSECorner(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        
        self.game=game
        self._layer=ground_layer
        self.groups = self.game.all_sprites, self.game.scenery
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x*tileSize
        self.y = y*tileSize
        
        
        self.width  = tileSize
        self.height = tileSize
        
        self.image = self.game.terrain_spritesheet.get_image(527,368, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        
class Waterfall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        
        self.game=game
        self._layer=cliff_layer
        self.groups = self.game.all_sprites, self.game.scenery
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x*tileSize
        self.y = y*tileSize
        
        
        self.width  = tileSize
        self.height = tileSize
        
        self.image = self.game.terrain_spritesheet.get_image(288,96, 47, 47)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
class Vertical_Fence(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        
        self.game=game
        self._layer=blocks_layer
        self.groups = self.game.all_sprites, self.game.scenery
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x*tileSize
        self.y = y*tileSize
        
        
        self.width  = tileSize
        self.height = tileSize
        
        self.image = self.game.terrain_spritesheet.get_image(3,274, 10, 30)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
class Tree(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        
        self.game=game
        self._layer=blocks_layer
        self.groups = self.game.all_sprites, self.game.scenery
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x*tileSize
        self.y = y*tileSize
        
        
        self.width  = tileSize
        self.height = tileSize
        
        self.image = self.game.terrain_spritesheet.get_image(80,256, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y