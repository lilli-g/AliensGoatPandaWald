import pygame 
import random
import sys


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
# constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
PLATFORM_WIDTH= 10
PLATFORM_HEIGHT =100
player1_color =(234, 144, 255)
player2_color =(255, 204, 153)
FPS = 100
info_line_y = 10 
info_spacing = 75

#set ball speed to be faster after every lost live but be reatartetd when game ends




class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        self.speed = [-1,1]
        self.radius = 10

    def update(self, player1 , player2):
        platform1_pos = player1.rect
        platform2_pos = player2.rect

        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]

        #check if ball hits wall:
        if self.pos[1] <= 0+self.radius:
            self.speed[1] = -self.speed[1]
            self.pos[1] = 0+self.radius

        elif self.pos[1] >= SCREEN_HEIGHT-self.radius:
            self.speed[1] = -self.speed[1]
            self.pos[1] = SCREEN_HEIGHT-self.radius
        
        #check if ball hits platform1:
        if (platform1_pos[0] <= self.pos[0] - self.radius <= platform1_pos[0] + PLATFORM_WIDTH
        and platform1_pos[1] <= self.pos[1] - self.radius <= platform1_pos[1] + PLATFORM_HEIGHT):
            self.speed[0] = -self.speed[0]
            player1.score += 1
            self.speed[0] += 0.1 
            self.speed[1] += 0.1 

        #check if ball hits platform2:
        if (platform2_pos[0] <= self.pos[0] + self.radius <= platform2_pos[0] + PLATFORM_WIDTH
        and platform2_pos[1] <= self.pos[1] + self.radius <= platform2_pos[1] + PLATFORM_HEIGHT):
            self.speed[0] = -self.speed[0]
            player2.score += 1
            self.speed[0] += 0.2 
            self.speed[1] += 0.2 
        
        #check if ball is out of bounds:
        if (self.pos[0] <= 0):
            player1.lives-=1
            self.pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        if (self.pos[0] >= SCREEN_WIDTH):
            player2.lives-=1
            self.pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]

        pygame.draw.circle(screen, (255,255,255), (int(self.pos[0]), int(self.pos[1])), self.radius)

class Player1(pygame.sprite.Sprite):
    def __init__(self):
        super(Player1, self).__init__()
        self.surf = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.surf.fill(player2_color)
        self.rect = self.surf.get_rect(center=(PLATFORM_WIDTH/2, PLATFORM_HEIGHT/2))
        self.lives = 3
        self.score = 0
        self.speed = 2

    def update(self, pressed_keys):
        if pressed_keys[K_w] and self.rect.y >0 :
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[K_s] and self.rect.y+PLATFORM_HEIGHT <SCREEN_HEIGHT:
            self.rect.move_ip(0, self.speed)
        else:
             self.rect.move_ip(0, 0)

class Player2(pygame.sprite.Sprite):
    def __init__(self):
        super(Player2, self).__init__()
        self.surf = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.surf.fill(player1_color)
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH-PLATFORM_WIDTH/2, PLATFORM_HEIGHT/2))
        self.lives = 3
        self.score = 0
        self.speed = 2

    def update(self, pressed_keys):
            if pressed_keys[K_UP] and self.rect.y >0 :
                self.rect.move_ip(0, -self.speed)
            if pressed_keys[K_DOWN] and self.rect.y+PLATFORM_HEIGHT <SCREEN_HEIGHT:
                self.rect.move_ip(0, self.speed)
            else:
             self.rect.move_ip(0, 0)



#funktions:
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
    show_text_on_screen("Pong", 50,y_position = SCREEN_HEIGHT // 4)
    show_text_on_screen("Press any key to start...", 30, y_position =SCREEN_HEIGHT // 3)
    show_text_on_screen("Move the platforms with arrow keys and W, S", 30,y_position = SCREEN_HEIGHT // 2)
    pygame.display.flip()
    wait_for_key()

def speed_up_screen():
    screen.fill((0,0,0))
    show_text_on_screen("To Easy", 50,y_position = SCREEN_HEIGHT // 4)
    show_text_on_screen("Let's speed this up...", 30, y_position =SCREEN_HEIGHT // 3)
    show_text_on_screen("Press any key to continue...", 20, y_position= SCREEN_HEIGHT*2 // 3)
    pygame.display.flip()
    wait_for_key()
    
def game_over_player1_screen(player1, player2):
    screen.fill((0,0,0))
    show_text_on_screen("Game Over", 50, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3)
    show_text_on_screen(f"Your final score: {player1.score}", 30,SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
    show_text_on_screen("Congratulations!", 50, (SCREEN_WIDTH // 4) *3, SCREEN_HEIGHT // 3)
    show_text_on_screen(f"Your final score: {player2.lives}", 30, (SCREEN_WIDTH // 4) *3, SCREEN_HEIGHT // 2)
    show_text_on_screen("Press any key to restart...", 20, y_position= SCREEN_HEIGHT *2 // 3) 
    pygame.display.flip()
    wait_for_key()

def game_over_player2_screen(player1, player2):
    screen.fill((0,0,0))
    show_text_on_screen("Congratulations!", 50, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3)
    show_text_on_screen(f"Your final score: {player1.lives}", 30,SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
    show_text_on_screen("Game Over", 50, (SCREEN_WIDTH // 4) *3, SCREEN_HEIGHT // 3)
    show_text_on_screen(f"Your final score: {player2.score}", 30, (SCREEN_WIDTH // 4) *3, SCREEN_HEIGHT // 2)
    show_text_on_screen("Press any key to restart...", 20, y_position= SCREEN_HEIGHT*2 // 3) 
    pygame.display.flip()
    wait_for_key()


clock = pygame.time.Clock()
#set up window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.Font(None, 20)
#initialize player
player1 = Player1()
player2 = Player2()
ball = Ball()

start_screen()
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
    ball.update(player1, player2)

    screen.blit(player1.surf,player1.rect)
    screen.blit(player2.surf,player2.rect)
    
    if player1.lives <=0 :
        game_over_player1_screen(player1,player2)
        start_screen()
        player1 = Player1()
        player2 = Player2()
        ball = Ball()
    if player2.lives <=0 :
        game_over_player2_screen(player1,player2)
        start_screen()
        player1 = Player1()
        player2 = Player2()
        ball = Ball()

    score_text = font.render(f"Score: {player1.score}   Lives: {player1.lives}", True, player1_color)
    score_rect = score_text.get_rect(topleft=(10, info_line_y))
    screen.blit(score_text, score_rect)

    score_text = font.render(f"Score: {player2.score}   Lives: {player2.lives}", True, player2_color)
    score_rect = score_text.get_rect(topright=(SCREEN_WIDTH-10, info_line_y))
    screen.blit(score_text, score_rect)

    pygame.display.flip()

    # Control the frame rate
    clock.tick(FPS)

# Done! Time to quit.
pygame.quit()