import pygame
from snake import *
from food import Food

pygame.init()
bounds = (600, 600)
window = pygame.display.set_mode(bounds)
pygame.display.set_caption("Snake Game")

block_size = 10
snake = Snake(block_size, bounds)
food = Food(block_size, bounds)
font = pygame.font.SysFont('Times New Roman', 60, True)

run = True
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        snake.steer(Direction.LEFT)
    elif keys[pygame.K_RIGHT]:
        snake.steer(Direction.RIGHT)
    elif keys[pygame.K_UP]:
        snake.steer(Direction.UP)
    elif keys[pygame.K_DOWN]:
        snake.steer(Direction.DOWN)

    snake.move()
    snake.check_for_food(food)

    if snake.check_bounds() == True or snake.check_tail_collision() == True:
        text = font.render('Game Over', True, (255, 0, 127))
        window.blit(text, (150, 200))
        pygame.display.update()
        pygame.time.delay(2000)
        snake.respawn()
        food.respawn()

    window.fill((0, 0, 0))
    snake.draw(pygame, window)
    food.draw(pygame, window)
    pygame.display.update()
