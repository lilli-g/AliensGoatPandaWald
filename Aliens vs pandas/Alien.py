import pygame
import numpy as np

pygame.init()
font_path = "./Fonts/seguiemj.ttf"

class Alien(pygame.sprite.Sprite):
    def __init__(self, size = 15, pos=(200,200)):
        super(Alien, self).__init__()
        self.size = size
        self.font = pygame.font.Font(font_path, self.size)
        self.icon = self.font.render("👽" , True,(255,255,255))
        self.rect = self.icon.get_rect(topright=(pos[0], pos[1]))
        self.speed = 2
        
    def update(self, panda, SCREEN_WIDTH, SCREEN_HEIGHT):
        #if alien hits panda:
        movement_v = [panda.rect.centerx-self.rect.centerx , panda.rect.centery-self.rect.centery]# collisions
        if np.linalg.norm(movement_v) <= 5:
            self.rect.move_ip(0,0)
            panda.health -=0.1

        #else alien just follows panda:
        else:
            normalized_v = movement_v / np.linalg.norm(movement_v)
            self.rect.move_ip((self.speed)*normalized_v[0], (self.speed) * normalized_v[1])
