'''
Created on May 7, 2014

@author: brewsterc
'''

# Conner Joseph Brewster, Devon S. Chao, Jonathan V. Nguyen
# Friday, May 23rd, 2014 @ 3:11:57 PM Central Standard Time (Daylight Savings Time)
# Pre-AP Computer Science
# Annette Walter - 7th Period

# Speed Snail
# Final Project

# Base code built off of the Dodger and Escape the Dragon programs.

#import needed modules
import pygame, random, sys, time
from pygame.locals import *

#initialize constant variables
window_width = 1000
window_height = 600
text_color = (0, 0, 0)
frames_per_second = 120
missile_minimum_size = 10
missile_maximum_size = 40
missile_minimum_speed = 1
missile_maximum_speed = 4
level = 1

#Name: terminate
#Description: Creates a way to exit the program
#Inputs: Escape and Quit Buttons    
#Output: Exits the program
def terminate(): 
    pygame.quit() 
    sys.exit() 

#Name: waitForPlayertoPressKey
#Description: Waits for the player to press a keyboard key to proceed in the game or quit it
#Input: Escape, Spacebar, Quit Buttons
#Output: Exits the program, proceeds to next screen, or to next level
def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: #pressing escape quits 
                    terminate()
                elif event.key == K_SPACE:
                     return 

#Name: playerHasHitMissile
#Description: Detects whether or not a missile has hit Speed Snail
#Input: snailRect, missiles
#Output: True for colliderect, False
def playerHasHitMissile(snailRect, missiles):
    for m in missiles:
        if snailRect.colliderect(m['rect']):
            return True
    return False

#Name: playerHasHitSpeedPowerUp
#Description: Detects whether or not Speed Snail collides with a speed power-up
#Input: snailRect, speed-power_ups
#Output: True for colliderect, False
def playerHasHitSpeedPowerUp(snailRect, speed_power_ups):
    if snailRect.colliderect(speed_power_upRect):
        return True
    return False

#Name: playerHasHitPointsPowerUP
#Description: Detects whether or not Speed Snail collides with a points power-up
#Input: snailRect, points_power_ups
#Output: True for colliderect, False
def playerHasHitPointsPowerUp(snailRect, points_power_ups):
    if snailRect.colliderect(points_power_upRect):
        return True
    return False

#Name: drawText
#Description: Renders all variants of text
#Input: text, font, surface, x, and y coordinates
#Output: blits(adds) a text on the screen
def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, text_color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

#format the in-game sprites.
snailImage = pygame.image.load('speed_snail.png')
snailRect = snailImage.get_rect()
missileImage = pygame.image.load('salt.png')
speed_power_upImage = pygame.image.load("speed_power_up_orb.png")
speed_power_upRect = speed_power_upImage.get_rect()
points_power_upImage = pygame.image.load("points_power_up_orb.png")
points_power_upRect = points_power_upImage.get_rect()

#setup the pygame basics.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Speed Snail')
pygame.mouse.set_visible(True)

# set up sounds
power_up_sound = pygame.mixer.Sound('orb_collect.wav')
collision_sound = pygame.mixer.Sound('missile_collision.wav')
pygame.mixer.music.load('background_music.mp3')

#allocate the font.
font = pygame.font.SysFont(None, 48)

#load the background image.
bg = pygame.image.load("background.png").convert_alpha()
begin_bg = pygame.image.load("beginning_screen.png").convert_alpha()
start_bg = pygame.image.load("starting_screen.png").convert_alpha()
instruct_bg = pygame.image.load("instructions_screen.png").convert_alpha()

#create the starting screen sequence.
windowSurface.blit(begin_bg, (0,0))
pygame.display.update()
waitForPlayerToPressKey()
windowSurface.blit(instruct_bg, (0,0))
pygame.display.update()
waitForPlayerToPressKey()
windowSurface.blit(start_bg, (0,0))
pygame.display.update()
waitForPlayerToPressKey()

#set high score to zero at game launch.
hi_score = 0
while True:
    #set up the start of the game.
    facing = "right"
    missiles = []
    if level == 1:
        windowSurface.blit(bg, (0,0))
    elif level == 2:
        windowSurface.blit(bg, (0,0))
    if level == 1:
        score = 0
    elif level == 2:
        score = 10000
    score_multiplyer = 1
    speed_snail_speed = 2
    points_power_up_value = 500
    missile_spawning_rate = 50
    death = False
    endless_mode = False
    snailRect.topleft = (400, 400)
    speed_power_upRect.topleft = (random.randint(200,950), random.randint(0,400))
    points_power_upRect.topleft = (random.randint(200,950), random.randint(0,400))
    moveLeft = moveRight = moveUp = moveDown = False
    missile_add_counter = 0
    pygame.mixer.music.play(-1, 0.0)
    while True: #the game loop runs while the game part is playing.
        score += score_multiplyer
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                #set parameters for when a keyboard key is pressed.
                if event.key == K_LEFT or event.key == ord('a'):
                    facing = "left"
                    snailImage = pygame.image.load('speed_snail_left.png')
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    facing = "right"
                    snailImage = pygame.image.load('speed_snail.png')
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    if facing == "right":
                        snailImage = pygame.image.load('speed_snail_up.png')
                    else:
                        snailImage = pygame.image.load('speed_snail_up_left.png')
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    if facing == "right":
                        snailImage = pygame.image.load('speed_snail_down.png')
                    else:
                        snailImage = pygame.image.load('speed_snail_down_left.png')
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                #set parameters for when a keyboard key is released.
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_LEFT or event.key == ord('a'):
                    snailImage = pygame.image.load('speed_snail_left.png')
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    snailImage = pygame.image.load('speed_snail.png')
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False
                if moveLeft == False and moveRight == False and moveUp == False and moveDown == False:
                    if facing == "right":
                        snailImage = pygame.image.load('speed_snail.png')
                    else:
                        snailImage = pygame.image.load('speed_snail_left.png')

        #add new missiles at the top of the screen, if needed.
        missile_add_counter += 1
        if missile_add_counter == missile_spawning_rate:
            missile_add_counter = 0
            missilesize = random.randint(missile_minimum_size, missile_maximum_size)
            newMissile = {'rect': pygame.Rect(0 - missilesize, random.randint(0, 500-missilesize), missilesize, missilesize),'speed': random.randint(missile_minimum_speed, missile_maximum_speed),'surface':pygame.transform.scale(missileImage, (missilesize, missilesize)),}
            missiles.append(newMissile)

        #move the player around.
        if moveLeft and snailRect.left > 0:
            snailRect.move_ip(-1 * speed_snail_speed, 0)
        if moveRight and snailRect.right < window_width:
            snailRect.move_ip(speed_snail_speed, 0)
        if moveUp and snailRect.top > 0:
            snailRect.move_ip(0, -1 * speed_snail_speed)
        if moveDown and snailRect.bottom < 490:
            snailRect.move_ip(0, speed_snail_speed)

        #move the missiles right.
        for m in missiles:
            m['rect'].move_ip(m['speed'], 0)

        #delete missiles that have gone past the screen.
        for m in missiles[:]:
            if m['rect'].left > window_width:
                missiles.remove(m)

        #draw the background.
        if level == 1:
            windowSurface.blit(bg, (0,0))
        elif level == 2:
            windowSurface.blit(bg, (0,0))

        #draw the score and top score.
        drawText('SCORE: %s' % (score), font, windowSurface, 10, 550)
        drawText('HI-SCORE: %s' % (hi_score), font, windowSurface, 290, 550)
        if endless_mode == True:
            drawText('Endless Mode: Unlocked', font, windowSurface, 600, 550)

        #draw the player's rectangle.
        windowSurface.blit(snailImage, snailRect)

        #draw the speed power-up's rectangle.
        windowSurface.blit(speed_power_upImage, speed_power_upRect)

        #draw the points power-up's rectangle.
        windowSurface.blit(points_power_upImage, points_power_upRect)
        
        #draw each missile.
        for m in missiles:
            windowSurface.blit(m['surface'], m['rect'])
        pygame.display.update()

        #check if any of the missiles have hit the player.
        if playerHasHitMissile(snailRect, missiles):
            if score > hi_score:
                hi_score = score # set new high score.
            collision_sound.play()
            death = True
            break

        #check if Speed Snail collects a speed power-up.
        if playerHasHitSpeedPowerUp(snailRect, speed_power_upRect):
            speed_power_up_status = True
            power_up_sound.play()
            speed_snail_speed += 1
            score_multiplyer += 1
            speed_power_upRect.topleft = (random.randint(200,1000), random.randint(0,400))
            
        #check if Speed Snail collects a points power-up.
        if playerHasHitPointsPowerUp(snailRect, points_power_upRect):
            power_up_sound.play()
            score += points_power_up_value
            points_power_up_value += 500
            points_power_upRect.topleft = (random.randint(200,1000), random.randint(0,400))

        #check for score necessary to move on to level two.
        if level == 1:
            if score > 9999:
                break
        else:
            if score > 24999:
                endless_mode = True

        #setup frames per second.
        mainClock.tick(frames_per_second)

    #finalize game over screen.
    if death == True:
        drawText('You died!', font, windowSurface, (window_width / 3), (window_height / 3))
        drawText('Press SPACEBAR to try again.', font, windowSurface, (window_width / 3) - 80, (window_height / 3) + 50)
        if level == 2:
            score = 10000
        pygame.display.update()
        waitForPlayerToPressKey()
    elif level == 1:
        drawText('Entering level two...', font, windowSurface, (window_width / 3), (window_height / 3))
        drawText('Press SPACEBAR to continue.', font, windowSurface, (window_width / 3) - 80, (window_height / 3) + 50)
        bg = pygame.image.load("background2.png").convert_alpha()
        missileImage = pygame.image.load('flame.png')
        level = 2
        pygame.display.update()
        waitForPlayerToPressKey()