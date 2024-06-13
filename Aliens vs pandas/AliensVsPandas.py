import Panda
import Alien
import ammo
import pygame
import sys
import random
import numpy as np
import time


font_path = "./Fonts/seguiemj.ttf"
pygame.init()


from pygame.locals import (
    K_UP,
    K_DOWN,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_w,
    K_s
)


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
FPS = 100
info_line_y = 10 
info_spacing = 75

#colors
red = (255, 0, 0)
white = (255, 255, 255)
purple =(234, 144, 255)
orange =(255, 204, 153)
font = pygame.font.Font(font_path, 20)


#FUnktions:
def get_aim(panda,mouse):
    vector = (mouse[0] -  panda.rect.centerx, mouse[1] -  panda.rect.centery)
    vector= vector/ np.linalg.norm(vector)
    return vector

def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

def show_text_on_screen(text, font_size, x_position = SCREEN_WIDTH // 2 ,y_position = SCREEN_HEIGHT // 2 ):
    font = pygame.font.Font(None, font_size)
    text_render = font.render(text, True, (255,255,255))
    text_rect = text_render.get_rect(center=(x_position, y_position))
    screen.blit(text_render, text_rect)

def start_screen():
    screen.fill((0,0,0))
    panda = Panda.Panda(size =150, pos= (SCREEN_WIDTH//3, SCREEN_HEIGHT//2-100))
    alien = Alien.Alien(size= 150, pos= ((SCREEN_WIDTH//3) *3-150, SCREEN_HEIGHT//2-110))
    screen.blit(panda.icon,panda.rect)
    screen.blit(alien.image,alien.rect)
    show_text_on_screen("Pandas vs. Aliens", 50,y_position = SCREEN_HEIGHT // 4)
    show_text_on_screen("Press any key to start...", 30, y_position =SCREEN_HEIGHT // 3)
    pygame.display.flip()
    wait_for_key()

def game_over_screen():
    screen.fill((0,0,0))
    show_text_on_screen("Game Over", 50, SCREEN_WIDTH //2, SCREEN_HEIGHT // 4)
    show_text_on_screen(f"Your final score: {panda.score}", 30, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    show_text_on_screen("Press any key to restart...", 30, y_position= SCREEN_HEIGHT*2 // 3) 
    pygame.display.flip()
    wait_for_key()






clock = pygame.time.Clock()
tree_timer = time.time()
alien_timer = time.time()
#set up window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#initialize player and aliens
panda = Panda.Panda(pos = (0 +50, SCREEN_HEIGHT//2 +5))
aliens =pygame.sprite.Group()
trees = pygame.sprite.Group()

#run until user quits
running = True 

start_screen()

while running:

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        if event.type == pygame.QUIT:
                running = False

    screen.fill((0, 0, 0))    

    pressed_keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pos()

    panda.update(pressed_keys,SCREEN_WIDTH, SCREEN_HEIGHT)

    aim = get_aim(panda,mouse)
    end_of_weapon = (panda.rect.centerx + aim[0]*25, panda.rect.centery + aim[1]*25)
    
    #trees
    if  time.time()- tree_timer >= 1:
        trees.add(ammo.Tree(panda.rect.center, aim))
        tree_timer = time.time()
    
    trees.update(aliens,SCREEN_WIDTH,SCREEN_HEIGHT)
    trees.draw(screen)

    
    if  time.time()- alien_timer >= 3:
        aliens.add(Alien.Alien(pos = (random.uniform(SCREEN_WIDTH,SCREEN_WIDTH+1000),random.uniform(SCREEN_HEIGHT,SCREEN_HEIGHT))))
        alien_timer = time.time()
        print(aliens)

    #aliens
    aliens.update(screen,panda,SCREEN_WIDTH, SCREEN_HEIGHT)
    aliens.draw(screen)

    pygame.draw.line(screen,white,panda.rect.center,end_of_weapon, 10)

    screen.blit(panda.icon,panda.rect) 

    score_text = font.render(f"Heath: {int(panda.health)}" , True, purple)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, info_line_y))
    screen.blit(score_text, score_rect)

    if panda.health <=0 :
        game_over_screen()
        start_screen()
        panda = Panda.Panda(pos = (0 +50, SCREEN_HEIGHT//2 +5))
        aliens = [Alien.Alien(pos = (random.uniform(SCREEN_WIDTH,SCREEN_WIDTH+1000),random.uniform(SCREEN_HEIGHT,SCREEN_HEIGHT))) for  i in range(0,1)]


    pygame.display.flip()

    # Control the frame rate
    clock.tick(FPS)

# Done! Time to quit.
pygame.quit()