# -*- coding: utf-8 -*-

from config import *
from sprites import *
from dialogue import *
import sys
import pygame

pygame.font.init()

class Spritesheet:
    def __init__(self, path):
        self.spritesheet = pygame.image.load(path).convert()
        
    def get_image(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.spritesheet, (0,0), (x,y,width,height))
        sprite.set_colorkey(BLACK)
        return sprite
    
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(win_width / 2)
        y = -target.rect.centery + int(win_height / 2)

        # Limit scrolling to map size
        x = min(0, x)  # Left
        y = min(0, y)  # Top
        x = max(-(self.width - win_width), x)  # Right
        y = max(-(self.height - win_height), y)  # Bottom

        self.camera = pygame.Rect(x, y, self.width, self.height)
        


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode([win_width, win_height])
        self.clock = pygame.time.Clock()
        self.terrain_spritesheet = Spritesheet('assets/images/Overworld.png')
        self.player_spritesheet = Spritesheet('assets/sprites/Female 03-3.png')
        self.npc_spritesheet = Spritesheet('assets/sprites/Characters.png')
        self.running = True
        self.npc_collided =False
        self.scenery_collided = False
        self.dialogue = DialogueBox(self)
        
        
        
        
    def createTileMap(self):
        
        npc_positions = {
            (17, 7): "Alice",
            (36, 4): "Samuel"
            }
        
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column=='P':
                    Player(self, j, i)
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
                if column=='T':
                    Tree(self, j, i)
                if column == 'N':
                    name = npc_positions.get((j, i), "NPC")
                    NPC(self, j, i, name=name)

    
    def create(self):
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.scenery = pygame.sprite.LayeredUpdates()
        self.npcs = pygame.sprite.LayeredUpdates()
        self.createTileMap()
        
        for sprite in self.all_sprites:
            if isinstance(sprite, Player):
                self.player = sprite
    
        self.camera = Camera(len(tilemap[0]) * tileSize, len(tilemap) * tileSize)
    
    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.dialogue.visible:
                    self.dialogue.hide()
    
    def draw(self):
        self.screen.fill(BLACK)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.dialogue.draw()
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