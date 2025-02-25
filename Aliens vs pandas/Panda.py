import pygame
import numpy as np


#font_path = "seguiemj.ttf"
font_path = "./Fonts/seguiemj.ttf"

pygame.init()
font = pygame.font.Font(font_path, 20)
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_w,
    K_s,
    K_a,
    K_d
)

class Panda(pygame.sprite.Sprite):
    def __init__(self, size = 30, pos=(200,200)):
        super(Panda, self).__init__()
        self.size = size
        self.speed = 2
        self.font = pygame.font.Font(font_path, self.size)
        self.icon = self.font.render("🐼" , True,(255,255,255))
        self.rect = self.icon.get_rect(topright=(pos[0], pos[1]))
        self.shooting_speed = 1
        self.health =10
        self.score = 0
        self.kills = 0
        self.rocket_timer = 0

    def update(self,pressed_keys,bambus, SCREEN_WIDTH, SCREEN_HEIGHT): #<-> forrest
        #is panda out of border? --> teleport
        if self.rect.centerx < 0:
            self.rect.centerx = SCREEN_WIDTH-self.size
        elif self.rect.centerx > SCREEN_WIDTH:
            self.rect.centerx = 0+self.size

        if self.rect.centery < 0:
            self.rect.centery = SCREEN_HEIGHT-self.size
        elif self.rect.centery > SCREEN_HEIGHT:
            self.rect.centery = 0+self.size

        #panda near forrest?  
                
        
        #if not out of brder: move in direktion indicated by keys
        elif pressed_keys[K_w]:
                
            for tree in bambus: #<-> forrest
                distance_tree= np.linalg.norm((tree.rect.centerx-self.rect.centerx , tree.rect.centery-self.rect.centery-self.speed+self.size))
                if distance_tree <= tree.size//2:
                    self.rect.move_ip(0,0)
                    break
            self.rect.move_ip(0, -self.speed)
        elif pressed_keys[K_s]:
                self.rect.move_ip(0, self.speed)
        elif pressed_keys[K_a]:
                self.rect.move_ip(-self.speed, 0)
        elif pressed_keys[K_d]:
                self.rect.move_ip(self.speed, 0)
        else:
             self.rect.move_ip(0, 0)

