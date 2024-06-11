import pygame

pygame.init()
font = pygame.font.Font("C:\\Windows\\Fonts\\seguiemj.ttf", 20)
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
    def __init__(self, size = 20, pos=(200,200)):
        super(Panda, self).__init__()
        self.size = size
        self.speed = 2
        self.font = pygame.font.Font("C:\\Windows\\Fonts\\seguiemj.ttf", self.size)
        self.icon = self.font.render("🐼" , True,(255,255,255))
        self.rect = self.icon.get_rect(topright=(pos[0], pos[1]))

    def update(self,pressed_keys, SCREEN_WIDTH, SCREEN_HEIGHT):

        #is panda out of border? --> teleport
        if self.rect.x <= 0:
            self.rect = self.icon.get_rect(bottomleft=(SCREEN_WIDTH, self.rect.y))
        elif self.rect.x >= SCREEN_WIDTH:
            self.rect = self.icon.get_rect(bottomleft=(0, self.rect.y))
        elif self.rect.y <= 0:
            self.rect = self.icon.get_rect(topright=(self.rect.x, SCREEN_HEIGHT))
        elif self.rect.y >= SCREEN_HEIGHT:
            self.rect = self.icon.get_rect(topright=(self.rect.x, 0))
        elif pressed_keys[K_w]:
                self.rect.move_ip(0, -self.speed)
        elif pressed_keys[K_s]:
                self.rect.move_ip(0, self.speed)
        elif pressed_keys[K_a]:
                self.rect.move_ip(-self.speed, 0)
        elif pressed_keys[K_d]:
                self.rect.move_ip(self.speed, 0)
        else:
             self.rect.move_ip(0, 0)

