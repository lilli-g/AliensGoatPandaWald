import pygame
import ammo
import numpy as np

pygame.init()
font_path = "./Fonts/seguiemj.ttf"


class Alien(pygame.sprite.Sprite):
    def __init__(self, size = 25, pos=(200,200), health = 3):
        super(Alien, self).__init__()
        self.size = size
        self.font = pygame.font.Font(font_path, self.size)
        self.image = self.font.render("👽" , True,(255,255,255))
        self.rect = self.image.get_rect(topright=(pos[0], pos[1]))
        self.health = health
        self.speed = 2
        
    def update(self,screen, panda,forrest, SCREEN_WIDTH, SCREEN_HEIGHT):
        #if alien hits panda:
        movement_v = [panda.rect.centerx-self.rect.centerx , panda.rect.centery-self.rect.centery]# collisions
        if np.linalg.norm(movement_v) <= 5:
            self.rect.move_ip(0,0)
            panda.health -=0.1

        elif self.health <= 1:
            #small explosion:
            text_render = self.font.render("💥" ,True, (255,255,255))
            text_rect = text_render.get_rect(center=self.rect.center)
            screen.blit(text_render, text_rect)
            forrest.add(ammo.Forrest(self.rect.center))
            self.kill()
        #else alien just follows panda:
        else:
            normalized_v = movement_v / np.linalg.norm(movement_v)
            self.rect.move_ip((self.speed)*normalized_v[0], (self.speed) * normalized_v[1])
