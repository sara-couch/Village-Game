# -*- coding: utf-8 -*-

from config import *
from sprites import *
import sys
import pygame

class Spritesheet:
    def __init__(self, path):
        self.spritesheet = pygame.image.load(path).convert()
        
    def get_image(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.spritesheet, (0,0), (x,y,width,height))
        sprite.set_colorkey(BLACK)
        return sprite


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode([win_width, win_height])
        self.clock = pygame.time.Clock()
        self.terrain_spritesheet = Spritesheet('assets/images/Overworld.png')
        self.player_spritesheet = Spritesheet('assets/sprites/Female 03-3.png')
        self.npc_spritesheet = Spritesheet('assets/sprites/Female 09-2.png')
        self.running = True
        
        
        
    def createTileMap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column=='P':
                    Player(self, j, i)
                if column=='N':
                    NPC(self, j, i)
                if column=='B':
                    Block(self, j, i)
                if column=='W':
                    Water(self, j, i)
                if column=='C':
                    Cliff(self, j, i)
                if column=='R':
                    WaterEdgeRight(self, j, i)
                if column=='D':
                    WaterEdgeDown(self, j, i)
                if column=='X':
                    WaterSECorner(self, j, i)
                if column=='Z':
                    Waterfall(self, j, i)
                if column=='V':
                    Vertical_Fence(self, j, i)
    
    def create(self):
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.scenery = pygame.sprite.LayeredUpdates()
        self.createTileMap()
    
    def update(self):
        self.all_sprites.update()
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running=False
    
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()
    
    def main(self):
        while self.running:
            self.events()
            self.update()
            self.draw()
    
    
game=Game()
game.create()

while game.running:
    game.main()
    
pygame.quit()
sys.exit()