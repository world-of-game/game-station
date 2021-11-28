import pygame
from pygame.locals import *
from pygame import mixer
import pickle
import math
from os import path

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 700
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('adventure')

# font
font = pygame.font.SysFont('Bauhaus 93', 50)
font_score = pygame.font.SysFont('Bauhaus 93', 20)
white_color = (255, 255, 255)
green_color = (0, 255, 0)
red_color = (255, 0, 0)

tile_size = 35
game_over = 0
main_menu = True
level = 1
score = 0


sun_img = pygame.image.load('adventure/img/sun.png')
sun = pygame.transform.scale(sun_img, (tile_size, tile_size))
bg_img = pygame.image.load('adventure/img/sky.jpg')
bg = pygame.transform.scale(bg_img, (700, 700))
restart_img = pygame.image.load('adventure/img/restart_btn.png')
start_img = pygame.image.load('adventure/img/start_btn.png')
start_img = pygame.transform.scale(start_img, (120, 42))
exit_img = pygame.image.load('adventure/img/exit_btn.png')
exit_img = pygame.transform.scale(exit_img, (120, 42))


# sounds
pygame.mixer.music.load('adventure/img/music.wav')
pygame.mixer.music.play(-1, 0.0, 5000)
coin_sound = pygame.mixer.Sound('adventure/img/coin.wav')
coin_sound.set_volume(0.5)
jump_sound = pygame.mixer.Sound('adventure/img/jump.wav')
jump_sound.set_volume(0.5)
game_over_sound = pygame.mixer.Sound('adventure/img/game_over.wav')
game_over_sound.set_volume(0.5)


def draw_text(text, font, text_col, x, y):
	font_img = font.render(text, True, text_col)
	screen.blit(font_img, (x, y))

def reset_level(level):
	player.reset(70, screen_height - 90)
	blob_group.empty()
	lava_group.empty()
	exit_group.empty()
	coin_group.empty()
	platform_group.empty()
	score_coin = Coin(tile_size // 2, tile_size // 2)
	coin_group.add(score_coin)

	if path.exists(f'adventure/level{level}_data'):
		pickle_in = open(f'adventure/level{level}_data', 'rb')
		world_data = pickle.load(pickle_in)
	world = World(world_data)

	return world


class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clicked = False

	def draw(self):
		action = False
		# mouse position
		mus_pos = pygame.mouse.get_pos()

		# check for mouse collision
		if self.rect.collidepoint(mus_pos):
			if pygame.mouse.get_pressed()[0] and not self.clicked:
				action = True
				self.clicked = True

		if not pygame.mouse.get_pressed()[0]:
			self.clicked = False

		screen.blit(self.image, self.rect)

		return action


# Jump has to be edited to be reduced to one
class Player():
	def __init__(self, x, y):
		self.reset(x, y)

	def update(self, game_over):
		dx = 0
		dy = 0
		walk_handle = 7
		col_thresh = 14
		if game_over == 0:
			key = pygame.key.get_pressed()
			if key[pygame.K_SPACE] and not self.jumped and not self.jump_handle:
				jump_sound.play()
				self.vel_y = -9
				self.jumped = True
			if not key[pygame.K_SPACE]:
				self.jumped = False
			if key[pygame.K_LEFT]:
				dx -= 3
				self.counter += 1
				self.direction = -1
			if key[pygame.K_RIGHT]:
				dx += 3
				self.counter += 1
				self.direction = 1
			if not key[pygame.K_RIGHT] and not key[pygame.K_LEFT]:
				self.counter = 0
				self.index = 0
				if self.direction == 1:
					self.image = self.images_movement_right[self.index]
				if self.direction == -1:
					self.image = self.images_movement_left[self.index]

			# animation
			if self.counter > walk_handle:
				self.counter = 0
				self.index += 1
				if self.index >= len(self.images_movement_right):
					self.index = 1
				if self.direction == 1:
					self.image = self.images_movement_right[self.index]
				if self.direction == -1:
					self.image = self.images_movement_left[self.index]

			# gravity
			self.vel_y += .5
			if self.vel_y > 10:
				self.vel_y = 10
			dy += self.vel_y

			# Collision
			self.collide_with_plat = False
			self.collide_with_tile = False
			self.jump_handle = True
			for tile in world.tile_list:
				# x Collision
				if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				# y Collision
				if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					if self.vel_y < 0:
						dy = tile[1].bottom - self.rect.top
						self.vel_y = 0
						self.collide_with_tile = True
					elif self.vel_y >= 0:
						dy = tile[1].top - self.rect.bottom
						self.vel_y = 0
						self.jump_handle = False
						self.collide_with_tile = True

				# platfrom collision
				for platform in platform_group:
					if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
						dx = 0
					if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
						if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
							dy = platform.rect.bottom - self.rect.top + 1
							self.vel_y = 0
							self.collide_with_plat = True

						elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
							self.rect.bottom = platform.rect.top - 1
							self.jump_handle = False
							dy = 0
							self.collide_with_plat = True

						# move with the platform
						if platform.move_x != 0:
							self.rect.x += platform.move_direction

			# Collision with Enemies
			if pygame.sprite.spritecollide(self, blob_group, False):
				game_over_sound.play()
				game_over = -1

			# Collision with lava
			if pygame.sprite.spritecollide(self, lava_group, False):
				game_over_sound.play()
				game_over = -1

			# Collision with exit
			if pygame.sprite.spritecollide(self, exit_group, False):
				game_over = 1




			self.rect.x += dx
			self.rect.y += dy

			if self.rect.bottom > screen_height:
				self.rect.bottom = screen_height
				dy = 0
		elif game_over == -1:
			self.image = self.death_image
			if self.rect.y > 140:
				self.rect.y -= 3
		screen.blit(self.image, self.rect)
		return game_over

	def reset(self, x, y):
		self.images_movement_right = []
		self.images_movement_left = []
		self.index = 0
		self.counter = 0
		for i in range(1, 7):
			img_right = pygame.image.load(f'adventure/img/pose_{i}.png')
			if i == 3 or i == 6:
				img_right = pygame.transform.scale(img_right, (45, 56))
			else:
				img_right = pygame.transform.scale(img_right, (28, 56))
			img_left = pygame.transform.flip(img_right, True, False)
			self.images_movement_right.append(img_right)
			self.images_movement_left.append(img_left)
		# print(len(self.images_movement_right))
		self.death_image = pygame.image.load(f'adventure/img/death_image.png')
		self.death_image = pygame.transform.scale(self.death_image, (45, 56))
		self.image = self.images_movement_right[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.vel_y = 0
		self.jumped = False
		self.direction = 0
		self.jump_handle = True
		self.collide_with_plat = False
		self.collide_with_tile = False


class World():
	def __init__(self, data):
		self.tile_list = []

		# load images
		dirt_img = pygame.image.load('adventure/img/dirt.png')
		grass_img = pygame.image.load('adventure/img/grass.png')

		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 2:
					img = pygame.transform.scale(grass_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 3:
					blob = Enemy(col_count * tile_size, row_count * tile_size + 5)
					blob_group.add(blob)
				if tile == 4:
					platform = Platform(col_count * tile_size, row_count * tile_size, 1, 0)
					platform_group.add(platform)
				if tile == 5:
					platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1)
					platform_group.add(platform)
				if tile == 6:
					lava = Lava(col_count * tile_size, row_count * tile_size + math.ceil(tile_size / 2))
					lava_group.add(lava)
				if tile == 7:
					coin = Coin(col_count * tile_size  + (tile_size // 2), row_count * tile_size + (tile_size // 2))
					coin_group.add(coin)
				if tile == 8:
					exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
					exit_group.add(exit)

				col_count += 1
			row_count += 1

	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])


class Enemy(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('adventure/img/blob.png')
		self.image = pygame.transform.scale(self.image, (tile_size, 30))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.movement = 1
		self.movement_counter = 0

	def update(self):
		self.rect.x += self.movement
		self.movement_counter += 1
		if abs(self.movement_counter) > 35:
			self.movement *= -1
			self.movement_counter *= -1


class Platform(pygame.sprite.Sprite):
	def __init__(self, x, y, move_x, move_y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('adventure/img/platform.png')
		self.image = pygame.transform.scale(self.image, (tile_size, tile_size //2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move_direction = 1
		self.move_counter = 0
		self.move_x = move_x
		self.move_y = move_y

	def update(self):
		self.rect.x += self.move_direction * self.move_x
		self.rect.y += self.move_direction * self.move_y
		self.move_counter += 1
		if abs(self.move_counter) > 35:
			self.move_direction *= -1
			self.move_counter *= -1

class Lava(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('adventure/img/lava.png')
		self.image = pygame.transform.scale(self.image, (tile_size, tile_size//2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.movement = 1
		self.movement_counter = 0


class Coin(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('adventure/img/coin.png')
		self.image = pygame.transform.scale(self.image, (tile_size//2, tile_size//2))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.movement = 1
		self.movement_counter = 0


class Exit(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('adventure/img/exit.png')
		self.image = pygame.transform.scale(self.image, (tile_size, int(tile_size * 1.5)))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.movement = 1
		self.movement_counter = 0


player = Player(70, screen_height - 90)
blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

# dummy coin
score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)

# load world_data
if path.exists(f'adventure/level{level}_data'):
	pickle_in = open(f'adventure/level{level}_data', 'rb')
	world_data = pickle.load(pickle_in)
world = World(world_data)

restart_button = Button(screen_width // 2 - 50, screen_height // 2 - 50, restart_img)
start_button = Button(screen_width // 2 - 200, screen_height // 2, start_img)
exit_button = Button(screen_width // 2 + 90, screen_height // 2, exit_img)


run = True
while run:
	clock.tick(fps)
	screen.blit(bg, (0, 0))
	screen.blit(sun, (80, 90))

	if main_menu:
		if start_button.draw():
			main_menu = False
		if exit_button.draw():
			run = False

	else:

		world.draw()
		# the normal situation
		if game_over == 0:
			blob_group.update()
			platform_group.update()

			# Update score
			if pygame.sprite.spritecollide(player, coin_group, True):
				coin_sound.play()
				score += 1
			draw_text('X ' + str(score), font_score, white_color, tile_size - 7, 7)



		blob_group.draw(screen)
		platform_group.draw(screen)
		lava_group.draw(screen)
		coin_group.draw(screen)
		exit_group.draw(screen)
		game_over = player.update(game_over)

		# collide from both top and bottom
		if player.collide_with_plat and player.collide_with_tile:
			game_over = -1

		# if the player has died
		if game_over == -1:
			draw_text('YOU DIED', font, red_color, screen_width // 2 - 100, screen_height // 2)

			if restart_button.draw():
				world_data = []
				world = reset_level(level)
				game_over = 0

		# if the player has won the level
		if game_over == 1:
			level += 1
			max_level = 7
			if level <= max_level:
				world_data = []
				world = reset_level(level)
				game_over = 0
			else:
				draw_text('YOU WON!', font, green_color, screen_width // 2 - 100, screen_height // 2)

				# restart the whole game
				if restart_button.draw():
					level = 1
					world_data = []
					world = reset_level(level)
					game_over = 0
					score = 0


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()
