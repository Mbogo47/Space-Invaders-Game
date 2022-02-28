import pygame
import random
import math
from pygame import mixer
# Initialize the pygame
pygame.init() #will always be in every game

# Create a screen
screen = pygame.display.set_mode((800,600)) 

# Background a 800 x 600
background = pygame.image.load("c:/Users/USER/PycharmProjects/exper/spaceinvaders/background_1.png")

# Background music
mixer.music.load("c:/Users/USER/PycharmProjects/exper/spaceinvaders/background.wav")
mixer.music.play(-1) # Makes the music play in a loop

# Title and icon
# Title 
pygame.display.set_caption("Space Invaders")

# Icon
icon = pygame.image.load("c:/Users/USER/PycharmProjects/exper/spaceinvaders/ufo.png")
pygame.display.set_icon(icon)
# icon = pygame.image.load("ufo.png")
# pygame.display.set_icon(icon)

# Player
playerimg = pygame.image.load("c:/Users/USER/PycharmProjects/exper/spaceinvaders/player.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 7

for i in range(num_of_enemies):
    enemyimg .append(pygame.image.load("c:/Users/USER/PycharmProjects/exper/spaceinvaders/enemy_1.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4) 
    enemyY_change.append(40)
    
# Bullet
bulletimg = pygame.image.load("c:/Users/USER/PycharmProjects/exper/spaceinvaders/bullet_1.png")
bulletX = 0
bulletY = 480
bulletX_change = 0 
bulletY_change = 10
# Ready - You can't see the bullet
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

text_X = 10
text_Y = 10

# Game over text
game_over_font = pygame.font.Font('freesansbold.ttf', 64)



def show_score(x, y):
    score = font.render(f"Score: {score_value}", True, (234,89,97))
    screen.blit(score, (x, y))

def game_over_text():
    game_over_font = font.render(f"GAME OVER!! ", True, (234,89,97))
    screen.blit(game_over_font, (200, 250))

def player(x,y):
    # drawing use blit
    screen.blit(playerimg, (x, y))

def enemy(x,  y, i):
    # drawing use blit
    screen.blit(enemyimg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    # Fire - The bullet is currently moving
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))

def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Game Loop
running = True

while running:
    # Changing background color
    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(background, (0, 0))

    # Enables the user to quit the screen 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keystrokes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -.3
            if event.key == pygame.K_RIGHT:
                playerX_change = .3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    # bullet sound
                    bullet_sound = mixer.Sound("c:/Users/USER/PycharmProjects/exper/spaceinvaders/laser.wav")
                    bullet_sound.play()

                    # Get the xcor of spaceship 
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)


        if event.type == pygame.KEYUP:
            if  event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Creating boundaries
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        # Enemy movement
        enemyX[i] +=enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = .7
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -.7
            enemyY[i] += enemyY_change[i]
        
        
        # Collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            # Collision Sound
            explosion_sound = mixer.Sound("c:/Users/USER/PycharmProjects/exper/spaceinvaders/explosion.wav")
            explosion_sound.play()
            bulletY = 480
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        
        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    # Firing multiple bullets
    if bulletY <=0:
        bulletY =   480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    
    player(playerX, playerY)
    
    show_score(text_X, text_Y)
    pygame.display.update() # Will always be in every game updates screen