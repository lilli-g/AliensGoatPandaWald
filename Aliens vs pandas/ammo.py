import pygame

font_path = "./Fonts/seguiemj.ttf"
pygame.init()
font = pygame.font.Font(font_path, 20)


class Tree(pygame.sprite.Sprite):
    def __init__(self,pos, aim):
        super(Tree, self).__init__()
        self.size = 20
        self.speed = 2
        self.aim = aim
        self.font = pygame.font.Font(font_path, self.size)
        self.immage = self.font.render("🌲" , True,(255,255,255))
        self.rect = self.immage.get_rect(topright=(pos[0], pos[1]))

    def update(self,aliens,SCREEN_WIDTH,SCREEN_HEIGHT):
        #löschen wenn out of bounds!!  
        #if self.rect.centerx < 0 or self.rect.centerx > SCREEN_WIDTH or self.rect.centery < 0 or self.rect.centery > SCREEN_HEIGHT:
            #self.kill()
        

        #collision mit aliens


        #else:
            self.rect.move_ip(self.speed*self.aim[0], self.speed*self.aim[1])
        
      

