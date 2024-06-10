import pygame 

pygame.init()
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_w,
    K_s
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Player1(pygame.sprite.Sprite):
    def __init__(self):
        super(Player1, self).__init__()
        self.surf = pygame.Surface((10, 50))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH-5,25))

    def update(self, pressed_keys):
            if pressed_keys[K_UP] and self.rect.y >0 :
                self.rect.move_ip(0, -1)
            if pressed_keys[K_DOWN] and self.rect.y+50 <SCREEN_HEIGHT:
                self.rect.move_ip(0, 1)


class Player2(pygame.sprite.Sprite):
    def __init__(self):
        super(Player2, self).__init__()
        self.surf = pygame.Surface((10, 50))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(5,25))

    def update(self, pressed_keys):
        if pressed_keys[K_w] and self.rect.y >0 :
            self.rect.move_ip(0, -1)
        if pressed_keys[K_s] and self.rect.y+50 <SCREEN_HEIGHT:
            self.rect.move_ip(0, 1)
        else:
             self.rect.move_ip(0, 0)



#set up window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#initialize player
player1 = Player1()
player2 = Player2()

#run until user quits
running = True 
while running:

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        if event.type == pygame.QUIT:
                running = False

    screen.fill((0, 0, 0))    

    pressed_keys = pygame.key.get_pressed()

    player1.update(pressed_keys)
    player2.update(pressed_keys)

    screen.blit(player1.surf,player1.rect)
    screen.blit(player2.surf,player2.rect)
    
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()