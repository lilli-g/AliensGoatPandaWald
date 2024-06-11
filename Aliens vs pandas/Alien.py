import pygame

pygame.init()


class Alien(pygame.sprite.Sprite):
    def __init__(self, size = 10, pos=(200,200)):
        super(Alien, self).__init__()
        self.size = size
        self.font = pygame.font.Font("C:\\Windows\\Fonts\\seguiemj.ttf", self.size)
        self.icon = self.font.render("👽" , True,(255,255,255))
        self.rect = self.icon.get_rect(topright=(pos[0], pos[1]))
