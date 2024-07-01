import pygame
import numpy as np

#font_path = "seguiemj.ttf"
font_path = "seguiemj.ttf"

pygame.init()
font = pygame.font.Font(font_path, 20)


class Tree(pygame.sprite.Sprite):
    def __init__(self,pos, aim):
        super(Tree, self).__init__()
        self.size = 15
        self.speed = 5
        self.aim = aim
        self.posx = pos[0]
        self.posy = pos[1]
        self.font = pygame.font.Font(font_path, self.size)
        self.image = self.font.render("🌲" , True,(255,255,255))
        self.rect = self.image.get_rect(center=(pos[0], pos[1]))

    def new_pos(self):
        new_posx = self.speed
        new_posy = self.speed * self.slope + self.intercept
        return (new_posx, new_posy)
        
    def update(self,aliens,SCREEN_WIDTH,SCREEN_HEIGHT):
        #löschen wenn out of bounds!!  
        if self.rect.centerx < 0 or self.rect.centerx > SCREEN_WIDTH or self.rect.centery < 0 or self.rect.centery > SCREEN_HEIGHT:
            self.kill()

        #collision mit aliens
        for alien in aliens.sprites():
            distance_alien= np.linalg.norm((alien.rect.centerx-self.rect.centerx , alien.rect.centery-self.rect.centery))
            if distance_alien <= (alien.size+self.size)//2:
                alien.health -=1
                self.kill()
        else:
            self.posx += self.speed*self.aim[0]
            self.posy += self.speed*self.aim[1]
            self.rect = self.image.get_rect(center=(self.posx, self.posy))

class Rocket(pygame.sprite.Sprite):
    def __init__(self,pos, aim):
        super(Rocket,self).__init__() 
        self.size = 15
        self.speed = 7
        self.aim = aim
        self.posx = pos[0]
        self.posy = pos[1]
        self.font = pygame.font.Font(font_path, self.size)
        self.image = self.font.render("🚀" , True,(255,255,255))
        self.rect = self.image.get_rect(center=(pos[0], pos[1]))

    def new_pos(self):
        new_posx = self.speed
        new_posy = self.speed * self.slope + self.intercept
        return (new_posx, new_posy)
        
    def update(self,aliens,screen,SCREEN_WIDTH,SCREEN_HEIGHT):
        #löschen wenn out of bounds!!  
        if self.rect.centerx < 0 or self.rect.centerx > SCREEN_WIDTH or self.rect.centery < 0 or self.rect.centery > SCREEN_HEIGHT:
            self.kill()

        #collision mit aliens
        for alien in aliens.sprites():
            distance_alien= np.linalg.norm((alien.rect.centerx-self.rect.centerx , alien.rect.centery-self.rect.centery))
            if distance_alien <= (alien.size+self.size)//2 + 50:
                alien.health -=1+distance_alien
                self.font = pygame.font.Font(font_path, 100)
                text_render = self.font.render("💥" ,True, (255,255,255))
                text_rect = text_render.get_rect(center=self.rect.center)
                screen.blit(text_render, text_rect)
                self.kill()
        else:
            self.posx += self.speed*self.aim[0]
            self.posy += self.speed*self.aim[1]
            self.rect = self.image.get_rect(center=(self.posx, self.posy))

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
            panda.shooting_speed += .5
            self.kill()

class Heart(pygame.sprite.Sprite):
    def __init__(self,pos):
        super(Heart, self).__init__()
        self.size = 15
        self.tick = 1
        self.font = pygame.font.Font(font_path, self.size)
        self.image = self.font.render("❤️" , True,(255,255,255))
        self.rect = self.image.get_rect(topright=(pos[0], pos[1]))

    def update(self,panda):
        distance_panda= np.linalg.norm((panda.rect.centerx-self.rect.centerx , panda.rect.centery-self.rect.centery))
        if distance_panda <= panda.size//2:
            self.tick -= 1
        if self.tick <= 0:
            panda.health += 1
            self.kill()

class Apple(pygame.sprite.Sprite):
    def __init__(self,pos):
        super(Apple, self).__init__()
        self.size = 15
        self.tick = 1
        self.font = pygame.font.Font(font_path, self.size)
        self.image = self.font.render("🍎" , True,(255,255,255))
        self.rect = self.image.get_rect(topright=(pos[0], pos[1]))

    def update(self,panda):
        distance_panda= np.linalg.norm((panda.rect.centerx-self.rect.centerx , panda.rect.centery-self.rect.centery))
        if distance_panda <= panda.size//2:
            self.tick -= 1
        if self.tick <= 0:
            panda.speed += .2
            self.kill()

class rocket_pu(pygame.sprite.Sprite):
    def __init__(self,pos):
        super(rocket_pu, self).__init__()
        self.size = 15
        self.tick = 1
        self.font = pygame.font.Font(font_path, self.size)
        self.image = self.font.render("🚀" , True,(255,255,255))
        self.rect = self.image.get_rect(topright=(pos[0], pos[1]))

    def update(self,panda):
        distance_panda= np.linalg.norm((panda.rect.centerx-self.rect.centerx , panda.rect.centery-self.rect.centery))
        if distance_panda <= panda.size//2:
            self.tick -= 1
        if self.tick <= 0:
            panda.rocket_timer += 700
            self.kill()