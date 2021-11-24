import pygame

pygame.init()  # initializes the Pygame
from pygame.locals import *  # import all modules from Pygame
import random

screen = pygame.display.set_mode((798, 600))

# changing title of the game window
pygame.display.set_caption('Car Racing')

# changing the logo
logo = pygame.image.load('car_assets_game/Logo_1.jfif')
pygame.display.set_icon(logo)


# defining our gameloop function

def gameloop():
    # setting background image
    bg = pygame.image.load('car_assets_game/bg.png')

    # setting our player
    maincar = pygame.image.load('car_assets_game\car.png')
    maincarX = 350
    maincarY = 495
    maincarX_change = 0
    maincarY_change = 0

    # other cars
    car1 = pygame.image.load('car_assets_game\car1.jpeg')
    car1X = random.randint(178, 490)
    car1Y = 100

    car2 = pygame.image.load('car_assets_game\car2.png')
    car2X = random.randint(178, 490)
    car2Y = 100

    car3 = pygame.image.load('car_assets_game\car3.png')
    car3X = random.randint(178, 490)
    car3Y = 100

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

                # checking if any key has been pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    maincarX_change += 5

                if event.key == pygame.K_LEFT:
                    maincarX_change -= 5

                if event.key == pygame.K_UP:
                    maincarY_change -= 5

                if event.key == pygame.K_DOWN:
                    maincarY_change += 5

                # checking if key has been lifted up
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    maincarX_change = 0

                if event.key == pygame.K_LEFT:
                    maincarX_change = 0

                if event.key == pygame.K_UP:
                    maincarY_change = 0

                if event.key == pygame.K_DOWN:
                    maincarY_change = 0

                    # setting boundary for our main car
        if maincarX < 178:
            maincarX = 178
        if maincarX > 490:
            maincarX = 490

        if maincarY < 0:
            maincarY = 0
        if maincarY > 495:
            maincarY = 495

        # CHANGING COLOR WITH RGB VALUE, RGB = RED, GREEN, BLUE
        screen.fill((0, 0, 0))

        # displaying the background image
        screen.blit(bg, (0, 0))

        # displaying our main car
        screen.blit(maincar, (maincarX, maincarY))

        # displaing other cars
        screen.blit(car1, (car1X, car1Y))
        screen.blit(car2, (car2X, car2Y))
        screen.blit(car3, (car3X, car3Y))

        # updating the values
        maincarX += maincarX_change
        maincarY += maincarY_change

        # movement of the enemies
        car1Y += 10
        car2Y += 10
        car3Y += 10

        # moving enemies infinitely
        if car1Y > 670:
            car1Y = -100
        if car2Y > 670:
            car2Y = -150
        if car3Y > 670:
            car3Y = -200

        pygame.display.update()


gameloop()