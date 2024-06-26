import Panda
import Alien
import ammo
import pygame
import math
import sys
import random
import numpy as np
import time
from scipy import linalg

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
weaponImg = pygame.image.load('Aliens vs pandas\Raketenwerfer.png')
width = weaponImg.get_rect().width
height = weaponImg.get_rect().height
weaponImg = pygame.transform.scale(weaponImg, (width/20, height/20))

#colors
red = (255, 0, 0)
white = (255, 255, 255)
purple =(234, 144, 255)
orange =(255, 204, 153)
font = pygame.font.Font(font_path, 20)

levels = { # (alien:  size, speed, killsto move on, spawn_time )
    1 : ([25,25],2,30,2),
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
def get_aim(panda):
    vector = (pygame.mouse.get_pos()[0] -  panda.rect.centerx, pygame.mouse.get_pos()[1] -  panda.rect.centery)
    vector= vector/ linalg.norm(vector)
    return vector

def calc_roation_angle(aim):
    v1 = (0,10)
    v0 = aim
    angle = np.math.atan2(np.linalg.det([v0,v1]),np.dot(v0,v1))
    angle=  np.degrees(angle)
    while 0 > angle or angle >= 360:
        if angle < 0:
            angle = 360 + angle
        if angle > 360 :
            angle -= 360
        if angle == 360:
            angle = 0
    return angle

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

def explanation_screen():
    screen.fill((0,0,0))
    show_text_on_screen("How to Play:", 50,y_position = SCREEN_HEIGHT // 4)
    show_text_on_screen("Press w,a,s,d to move", 30, y_position =SCREEN_HEIGHT // 3)
    show_text_on_screen("aim by moving your mouse", 30, y_position =SCREEN_HEIGHT // 3+50)
    show_text_on_screen("pause the game by pressing p anytime during the game", 30, y_position =SCREEN_HEIGHT // 3+100)
    show_text_on_screen("Press any key to start...", 30, y_position =SCREEN_HEIGHT // 3+150)
    pygame.display.flip()
    wait_for_key()

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
    explanation_screen()


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

def paused():
    pause = True
    
    while pause:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit() 
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.type == pygame.QUIT:
                    running = False
                if event.key == pygame.K_c:
                    pause = False

        score_text = font.render("PAUSED", True, orange)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, 200))
        screen.blit(score_text, score_rect)
                
        score_text = font.render("To Continue press c", True, orange)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, 400))
        screen.blit(score_text, score_rect)

        pygame.display.update()
        clock.tick(15)  


def Raketenwerfer(aim):
    angle = calc_roation_angle(aim)
    rota_image = pygame.transform.rotate(weaponImg, angle+180)
    return rota_image



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
rockets = pygame.sprite.Group()

current_level = 1
end_level  = 10
alien_size = levels[current_level][0]
alien_speed = levels[current_level][1]
spawn_time = levels[current_level][3]
kills = levels[current_level][2]
alien_count = 0
img = 0 

#run until user quitsd
running = True 





start_screen()

while running:

    timer = time.time()
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == pygame.K_p:
                paused()

        if event.type == pygame.QUIT:
                running = False
        

    screen.fill((0, 0, 0))    

    pressed_keys = pygame.key.get_pressed()

    panda.update(pressed_keys,forrest,SCREEN_WIDTH, SCREEN_HEIGHT)

    aim = get_aim(panda)
    end_of_weapon = (panda.rect.centerx + aim[0]*25, panda.rect.centery + aim[1]*25)

    if panda.rocket_timer > 0:
        img = Raketenwerfer(aim)
        screen.blit(panda.icon,panda.rect) 
        screen.blit(img, (panda.rect.centerx-15,panda.rect.centery-15))
        
    else:
        pygame.draw.line(screen,white,panda.rect.center,end_of_weapon, 10)
        screen.blit(panda.icon,panda.rect) 

    #trees
    if time.time()- tree_timer >= 1/panda.shooting_speed and panda.rocket_timer > 0:
        rockets.add( ammo.Rocket((panda.rect.centerx+15,panda.rect.centery+15), aim))
        panda.rocket_timer -= 100    
        tree_timer = time.time()
    elif  time.time()- tree_timer >= 1/panda.shooting_speed:
        trees.add(ammo.Tree(panda.rect.center, aim))
        tree_timer = time.time()
    
    trees.update(aliens,SCREEN_WIDTH,SCREEN_HEIGHT)
    trees.draw(screen)
    rockets.update(aliens,screen,SCREEN_WIDTH,SCREEN_HEIGHT)
    rockets.draw(screen)


    
    if  time.time() - alien_timer >= spawn_time and alien_count < kills :
        if current_level == end_level:
            aliens.add(Alien.Goat(SCREEN_WIDTH, SCREEN_HEIGHT))
            alien_count += 1
        else:   
            aliens.add(Alien.Alien(SCREEN_WIDTH, SCREEN_HEIGHT,current_level= current_level, size = alien_size, speed = alien_speed, ))
            alien_timer = time.time()
            alien_count += 1

    #aliens
    aliens.update(screen,panda,bambus,current_level)
    aliens.draw(screen)

    #bambus
    bambus.update(panda)
    bambus.draw(screen)

    #forrest
    forrest.draw(screen)
    
    

    score_text = font.render(f"Heath: {int(panda.health)}   speed: {int((panda.shooting_speed))}    kills: {panda.kills}    level:  {current_level} " , True, purple)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, info_line_y))
    screen.blit(score_text, score_rect)

    if panda.health <= 0 :
        game_over_screen(current_level)
        start_screen()
        panda = Panda.Panda(pos = (0 +50, SCREEN_HEIGHT//2 +5))
        aliens =pygame.sprite.Group()
        alien_count = 0
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
        alien_count = 0
        trees = pygame.sprite.Group()
        bambus = pygame.sprite.Group()
        forrest = pygame.sprite.Group()

    # Control the frame rate
    clock.tick(FPS)

# Done! Time to quit.
pygame.quit()