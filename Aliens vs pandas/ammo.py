import pygame

pygame.init()
font = pygame.font.Font("C:\\Windows\\Fonts\\seguiemj.ttf", 20)


class Tree(pygame.sprite.Sprite):
    def __init__(self,speed,pos, size = 1):
        super(Tree, self).__init__()
        self.size = size
        self.speed = speed
        self.font = pygame.font.Font("C:\\Windows\\Fonts\\seguiemj.ttf", self.size)
        self.icon = self.font.render("🌲" , True,(255,255,255))
        self.rect = self.icon.get_rect(topright=(pos[0], pos[1]))

    #def update(self,pressed_keys):
        

