import pygame
from pygame.locals import *

pygame.init()

# Game Window width and height.
screen_width = 800
screen_height = 600

# The Gaming Board.
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong Game')


# define font.
font = pygame.font.SysFont('georgia', 30)


# Determine the game variables.
margin = 50  # this margin is to make a header area at top window.
cpu_score = 0  # to start counts the points for the computer each time scored.
player_score = 0  # # to start counts the points for the player each time scored.
fps = 60  # frame per second, to control the speed of the moving paddles
live_ball = False  # make the ball into action.
winner = 0  # to start scoring from
speed_increase = 0  # to make the ball speed increases.


# determine the background colours
rgb = (0,125,0)
white = (255, 255, 255)

# Function for drawing the board.
def draw_board():
	screen.fill(rgb)
	pygame.draw.line(screen, white, (0, margin), (screen_width, margin), 2)


# Function to print out the text in header, what font type and color.
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

# To use the build in method Rect(coordinates, width, height), to create rectangle.
class paddle():
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.rect = Rect(x, y, 20, 100)
		self.speed = 5
		self.ai_speed = 5

	# This function will make the rectangles move by up & down arrows on keyboard by built in key method.
	def move(self):
		key = pygame.key.get_pressed()
		if key[pygame.K_UP] and self.rect.top > margin:
			self.rect.move_ip(0, -1 * self.speed)
		if key[pygame.K_DOWN] and self.rect.bottom < screen_height:
			self.rect.move_ip(0, self.speed)

	#  to draw the rectangles on the game board.
	def draw(self):
		pygame.draw.rect(screen, white, self.rect)

	# AI function to control the computer paddle.
	def ai(self):
		# ai to move the paddle automatically
		# move down
		if self.rect.centery < pong.rect.top and self.rect.bottom < screen_height:
			self.rect.move_ip(0, self.ai_speed)
		# move up
		if self.rect.centery > pong.rect.bottom and self.rect.top > margin:
			self.rect.move_ip(0, -1 * self.ai_speed)



class ball():
	def __init__(self, x, y):
		self.reset(x, y)


	def move(self):

		# check collision with top margin
		if self.rect.top < margin:
			self.speed_y *= -1  # flip the speed to get inverted
		# check collision with bottom of the screen
		if self.rect.bottom > screen_height:
			self.speed_y *= -1
		if self.rect.colliderect(player_paddle) or self.rect.colliderect(cpu_paddle):
			self.speed_x *= -1

		# check for out of bounds: if ball goes beyond the paddle that is a score
		if self.rect.left < 0:
			self.winner = 1
		if self.rect.left > screen_width:
			self.winner = -1

		# update ball position
		self.rect.x += self.speed_x
		self.rect.y += self.speed_y

		return self.winner


	def draw(self):
		pygame.draw.circle(screen, white, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)


	def reset(self, x, y):
		self.x = x
		self.y = y
		self.ball_rad = 8
		self.rect = Rect(x, y, self.ball_rad * 2, self.ball_rad * 2)
		self.speed_x = -4
		self.speed_y = 4
		self.winner = 0  # 1 is the player and -1 is the Computer


#create paddles
player_paddle = paddle(screen_width - 40, screen_height // 2)
cpu_paddle = paddle(20, screen_height // 2)

#create pong ball
pong = ball(screen_width - 60, screen_height // 2 + 50)


#create game loop
run = True
while run:

	# frame speed of the player paddle.
	fpsClock.tick(fps)

	draw_board()
	draw_text('Computer: ' + str(cpu_score), font, white, 20, 15)
	draw_text('Player: ' + str(player_score), font, white, screen_width - 100, 15)
	draw_text('BALL SPEED: ' + str(abs(pong.speed_x)), font, white, screen_width // 2 - 100 , 15)


	# render paddles.
	player_paddle.draw()
	cpu_paddle.draw()

	if live_ball == True:
		speed_increase += 1
		winner = pong.move()
		if winner == 0:
			# draw ball
			pong.draw()
			# move paddles
			player_paddle.move()
			cpu_paddle.ai()
		else:
			live_ball = False
			if winner == 1:
				player_score += 1
			elif winner == -1:
				cpu_score += 1


	# print player instructions
	if live_ball == False:
		if winner == 0:
			draw_text('CLICK ANYWHERE TO START', font, white, 200, screen_height // 2 -100)
		if winner == 1:
			draw_text('YOU SCORED!', font, white, 270, screen_height // 2 -100)
			draw_text('CLICK ANYWHERE TO START', font, white, 200, screen_height // 2 -50)
		if winner == -1:
			draw_text('Computer SCORED!', font, white, 270, screen_height // 2 -100)
			draw_text('CLICK ANYWHERE TO START', font, white, 200, screen_height // 2 -50)



	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
			live_ball = True
			pong.reset(screen_width - 60, screen_height // 2 + 50)



	if speed_increase > 500:
		speed_increase = 0
		if pong.speed_x < 0:
			pong.speed_x -= 1
		if pong.speed_x > 0:
			pong.speed_x += 1
		if pong.speed_y < 0:
			pong.speed_y -= 1
		if pong.speed_y > 0:
			pong.speed_y += 1


	pygame.display.update()

pygame.quit()