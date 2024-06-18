import pygame
import numpy as np

font_path = "./Fonts/seguiemj.ttf"
pygame.init()
font = pygame.font.Font(font_path, 20)


class Tree(pygame.sprite.Sprite):
    def __init__(self,pos, aim):
        super(Tree, self).__init__()
        self.size = 15
        self.speed = 5
        self.aim = aim
        self.font = pygame.font.Font(font_path, self.size)
        self.image = self.font.render("🌲" , True,(255,255,255))
        self.rect = self.image.get_rect(topright=(pos[0], pos[1]))

    def update(self,aliens,SCREEN_WIDTH,SCREEN_HEIGHT):
        #löschen wenn out of bounds!!  
        if self.rect.centerx < 0 or self.rect.centerx > SCREEN_WIDTH or self.rect.centery < 0 or self.rect.centery > SCREEN_HEIGHT:
            self.kill()

        #collision mit aliens
        for alien in aliens.sprites():
            distance_alien= np.linalg.norm((alien.rect.centerx-self.rect.centerx , alien.rect.centery-self.rect.centery))
            if distance_alien <= (alien.size+self.size)//2:
                alien.health -=1
        else:
            self.rect.move_ip(self.speed*self.aim[0], self.speed*self.aim[1])

class Forrest(pygame.sprite.Sprite):
    def __init__(self,pos):
        super(Forrest, self).__init__()
        self.size = 15
        self.font = pygame.font.Font(font_path, self.size)
        self.image = self.font.render("🎋" , True,(255,255,255))
        self.rect = self.image.get_rect(topright=(pos[0], pos[1]))
        
class Bambus(pygame.sprite.Sprite):
    def __init__(self,pos):
        super(Bambus, self).__init__()
        self.size = 15
        self.tick = 1
        self.font = pygame.font.Font(font_path, self.size)
        self.image = self.font.render("🎋" , True,(255,255,255))
        self.rect = self.image.get_rect(topright=(pos[0], pos[1]))

    def update(self,panda):
        distance_panda= np.linalg.norm((panda.rect.centerx-self.rect.centerx , panda.rect.centery-self.rect.centery))
        if distance_panda <= panda.size//2:
            self.tick -= 1
        if self.tick <= 0:
            panda.shooting_speed += 1
            self.kill()