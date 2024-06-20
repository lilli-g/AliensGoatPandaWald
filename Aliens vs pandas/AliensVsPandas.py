import Panda
import Alien
import ammo
import pygame
import sys
import random
import numpy as np
import time

#to DO:
#raketen
#anzahl aliens begrenzen
#aliens laufen nicht übereinander
#erklärungsscreen


#font_path = "seguiemj.ttf"
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
info_line_y = 20 
info_spacing = 75

#colors
red = (255, 0, 0)
white = (255, 255, 255)
purple =(234, 144, 255)
orange =(255, 204, 153)
font = pygame.font.Font(font_path, 20)

levels = { # (alien:  size, speed, killsto move on, spawn_time )
    1 : ([25,25],2,30,3),
    2 : ([25,30],2,40,2),
    3 : ([25,40],2,50,1),
    4 : ([25,50],3,60,.5),
    5 : ([30,50],3,70,0.4),
    6 : ([40,60],4,80,.3),
    7 : ([50,70],4,90,.2),
    8 : ([50,80],4,100,.2),
    9 : ([70,80],4,130,.1),
    10 : (100,4,1,0)
}


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

def level_screen(current_level):
    screen.fill((0,0,0))
    show_text_on_screen("Congratulations!", 50, SCREEN_WIDTH //2, SCREEN_HEIGHT // 4)
    show_text_on_screen(f"You beat level {current_level}", 40, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.display.flip()
    pygame.time.wait(3000)

def start_screen():
    screen.fill((0,0,0))
    panda = Panda.Panda(size =150, pos= (SCREEN_WIDTH//3, SCREEN_HEIGHT//2-100))
    alien = Alien.Alien(SCREEN_WIDTH, SCREEN_HEIGHT,size= (150,150), pos= ((SCREEN_WIDTH//3) *3-150, SCREEN_HEIGHT//2-110))
    screen.blit(panda.icon,panda.rect)
    screen.blit(alien.image,alien.rect)
    show_text_on_screen("Pandas vs. Aliens", 50,y_position = SCREEN_HEIGHT // 4)
    show_text_on_screen("Press any key to start...", 30, y_position =SCREEN_HEIGHT // 3)
    pygame.display.flip()
    wait_for_key()

def end_screen():
    screen.fill((0,0,0))
    show_text_on_screen("Congrats!", 50, SCREEN_WIDTH //2, SCREEN_HEIGHT // 4)
    show_text_on_screen(f"You defeated the GOAT ", 30, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    show_text_on_screen("Press any key to restart...", 30, y_position =SCREEN_HEIGHT // 3)
    pygame.display.flip()
    wait_for_key()

def game_over_screen(current_level):
    screen.fill((0,0,0))
    show_text_on_screen("Game Over!", 50, SCREEN_WIDTH //2, SCREEN_HEIGHT // 4)
    show_text_on_screen(f"Your final level: {current_level}", 30, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    show_text_on_screen("Press any key to restart...", 30, y_position =SCREEN_HEIGHT // 3)
    pygame.display.flip()
    wait_for_key()






clock = pygame.time.Clock()
tree_timer = time.time()
alien_timer = time.time()
#set up window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#initialize player and aliens,...
panda = Panda.Panda(pos = (0 +50, SCREEN_HEIGHT//2 +5))
aliens =pygame.sprite.Group()
trees = pygame.sprite.Group()
bambus = pygame.sprite.Group()
forrest = pygame.sprite.Group()

current_level = 1
end_level  = 10
alien_size = levels[current_level][0]
alien_speed = levels[current_level][1]
spawn_time = levels[current_level][3]
kills = levels[current_level][2]
 

#run until user quits
running = True 





start_screen()

while running:

    timer = time.time()
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        if event.type == pygame.QUIT:
                running = False

    screen.fill((0, 0, 0))    

    pressed_keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pos()

    panda.update(pressed_keys,forrest,SCREEN_WIDTH, SCREEN_HEIGHT)

    aim = get_aim(panda,mouse)
    end_of_weapon = (panda.rect.centerx + aim[0]*25, panda.rect.centery + aim[1]*25)
    
    #trees
    if  time.time()- tree_timer >= 1/panda.shooting_speed:
        trees.add(ammo.Tree(panda.rect.center, aim))
        tree_timer = time.time()
    
    trees.update(aliens,SCREEN_WIDTH,SCREEN_HEIGHT)
    trees.draw(screen)

    
    if  time.time()- alien_timer >= spawn_time and len(aliens.sprites()) < kills :
        if current_level == end_level:
            aliens.add(Alien.Goat(SCREEN_WIDTH, SCREEN_HEIGHT))
        else:   
            aliens.add(Alien.Alien(SCREEN_WIDTH, SCREEN_HEIGHT,current_level= current_level, size = alien_size, speed = alien_speed, ))
            alien_timer = time.time()

    #aliens
    aliens.update(screen,panda,bambus,current_level)
    aliens.draw(screen)

    #bambus
    bambus.update(panda)
    bambus.draw(screen)

    #forrest
    forrest.draw(screen)

    pygame.draw.line(screen,white,panda.rect.center,end_of_weapon, 10)

    screen.blit(panda.icon,panda.rect) 

    score_text = font.render(f"Heath: {int(panda.health)}   speed: {int((panda.shooting_speed))}    score: {panda.kills}    level:  {current_level} " , True, purple)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, info_line_y))
    screen.blit(score_text, score_rect)

    if panda.health <=0 :
        game_over_screen(current_level)
        start_screen()
        panda = Panda.Panda(pos = (0 +50, SCREEN_HEIGHT//2 +5))
        aliens =pygame.sprite.Group()
        trees = pygame.sprite.Group()
        bambus = pygame.sprite.Group()
        forrest = pygame.sprite.Group()


        current_level = 1
        alien_size = levels[current_level][0]
        alien_speed = levels[current_level][1]
        spawn_time = levels[current_level][3]

    pygame.display.flip()

    if panda.kills >= kills:
        

        level_screen(current_level)
        if current_level == end_level:
            end_screen()
            start_screen()
            current_level = 0
            panda = Panda.Panda(pos = (0 +50, SCREEN_HEIGHT//2 +5))

        current_level += 1
        alien_size = levels[current_level][0]
        alien_speed = levels[current_level][1]
        spawn_time = levels[current_level][3]
        panda.kills = 0
        aliens =pygame.sprite.Group()
        trees = pygame.sprite.Group()
        bambus = pygame.sprite.Group()
        forrest = pygame.sprite.Group()


   
    # Control the frame rate
    clock.tick(FPS)

# Done! Time to quit.
pygame.quit()