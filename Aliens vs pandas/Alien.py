import pygame
import ammo
import numpy as np
import random

pygame.init()
#font_path = "seguiemj.ttf"
font_path = "./Fonts/seguiemj.ttf"


class Alien(pygame.sprite.Sprite):
    def __init__(self,SCREEN_WIDTH,SCREEN_HEIGHT, size = [25,25],  speed = 2, pos = (0,0), current_level = 1):
        super(Alien, self).__init__()
        self.size =random.randint(size[0], size[1]+1)
        self.font = pygame.font.Font(font_path, self.size)
        self.image = self.font.render("👽" , True,(255,255,255))
        if pos != (0,0):
            self.pos = pos
        elif  random.randint(0,1) == 1:
            self.pos = random.randint(SCREEN_WIDTH,SCREEN_WIDTH+1000),random.randint(SCREEN_HEIGHT,SCREEN_HEIGHT+1000)
        else:
            self.pos = -random.randint(0,1000),-random.randint(0,1000)

        self.rect = self.image.get_rect(topright=(self.pos[0], self.pos[1]))
        self.health = self.size//10 *current_level
        self.speed = speed
        
    def update(self,screen, panda,bambus, current_level): #<-> forrest
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

            powerup = random.randint(0,4+current_level^2)
            if powerup == 1:
                bambus.add(ammo.Bambus(self.rect.center))
            elif powerup == 2:
                bambus.add(ammo.Heart(self.rect.center))
            if powerup == 3:
                bambus.add(ammo.Apple(self.rect.center))
            
            panda.kills += 1
            self.kill()
        #else alien just follows panda:
        else:
            normalized_v = movement_v / np.linalg.norm(movement_v)
            self.rect.move_ip((self.speed)*normalized_v[0], (self.speed) * normalized_v[1])

class Goat(pygame.sprite.Sprite):
    def __init__(self,SCREEN_WIDTH,SCREEN_HEIGHT, size = 100,  speed = 10, pos = (0,0), current_level = 1):
        super(Goat, self).__init__()
        self.size =size
        self.font = pygame.font.Font(font_path, self.size)
        self.image = self.font.render("🐐" , True,(255,255,255))
        if pos != (0,0):
            self.pos = pos
        elif  random.randint(0,1) == 1:
            self.pos = random.randint(SCREEN_WIDTH,SCREEN_WIDTH+1000),random.randint(SCREEN_HEIGHT,SCREEN_HEIGHT+1000)
        else:
            self.pos = -random.randint(0,1000),-random.randint(0,1000)

        self.rect = self.image.get_rect(topright=(self.pos[0], self.pos[1]))
        self.health = 10000
        self.speed = speed
        
    def update(self,screen, panda,bambus, current_level): #<-> forrest
        #if alien hits panda:
        movement_v = [panda.rect.centerx-self.rect.centerx , panda.rect.centery-self.rect.centery]# collisions
        if np.linalg.norm(movement_v) <= 5:
            self.rect.move_ip(0,0)
            panda.health -=0.5

        elif self.health <= 1:
            #small explosion:
            text_render = self.font.render("💥" ,True, (255,255,255))
            text_rect = text_render.get_rect(center=self.rect.center)
            screen.blit(text_render, text_rect)
            powerup = random.randint(0,current_level^2)
            if powerup == 1:
                bambus.add(ammo.Bambus(self.rect.center))
            panda.kills += 1
            self.kill()
        #else alien just follows panda:
        else:
            normalized_v = movement_v / np.linalg.norm(movement_v)
            self.rect.move_ip((self.speed)*normalized_v[0], (self.speed) * normalized_v[1])

