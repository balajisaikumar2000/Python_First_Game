import pygame               
import random                         #for generating random numbers
import sys                              #for system info

pygame.init()                               #intialize all pygame modules

width = 800
height =600

RED = (255,0,0)
BLUE  = (0,0,255)
YELLOW = (255,255,0)
BACK_GROUND_COLOR = (0,0,0)

player_size = 50
player_pos = [width/2,height-2*player_size]

enemy_size =50
enemy_pos = [random.randint(0,width-enemy_size),0]
enemy_lst = [enemy_pos]
print(enemy_lst)

screen = pygame.display.set_mode((width,height))           #This function will create a display Surface

SPEED = 10

game_over = False

score = 0 

clock = pygame.time.Clock()                              #create an object to help track time

myFont = pygame.font.SysFont("monospace",35)            #create a Font object from the system fonts;SysFont(name, size, bold=False, italic=False)

def set_level(score,SPEED):
	if score < 20:
		SPEED = 8
	elif score< 40:
		SPEED = 12
	elif score < 60:
		SPEED = 18
	else:
		SPEED = 20

	return SPEED

def drop_enemies(enemy_lst):
	delay = random.random()                        #will generete a random number between 0-1
 
	if len(enemy_lst) < 10 and delay < 0.1:
		x_pos = random.randint(0,width-enemy_size)
		y_pos = 0
		enemy_lst.append([x_pos,y_pos])

def draw_enemies(enemy_lst):
	for enemy_pos in enemy_lst:
		pygame.draw.rect(screen,BLUE,(enemy_pos[0],enemy_pos[1],enemy_size,enemy_size))

def update_enemy_positions(enemy_lst,score):
	for idx,enemy_pos in enumerate(enemy_lst):
		 if enemy_pos[1] >= 0 and enemy_pos[1] < height:
		 	enemy_pos[1] += SPEED
		 else:
		 	enemy_lst.pop(idx)
		 	score += 1
	return score

def collision_check(enemy_lst,player_pos):
	for enemy_pos in enemy_lst:
		if detect_collisions(enemy_pos,player_pos):
			return True
	return False



def detect_collisions(player_pos,enemy_pos):
	p_x = player_pos[0]
	p_y =  player_pos[1]

	e_x = enemy_pos[0]
	e_y = enemy_pos[1]

	if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
		if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y+enemy_size)):
			return True
	return False

while not game_over:
	for event in pygame.event.get():                 #get events from the queue
		# print(event)

		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.KEYDOWN:

			x = player_pos[0]
			y = player_pos[1]

			if event.key == pygame.K_LEFT:
				x -= player_size
			elif event.key == pygame.K_RIGHT:
				x += player_size
			player_pos = [x,y]

	screen.fill(BACK_GROUND_COLOR)

	# if enemy_pos[1] >= 0 and enemy_pos[1] < height:
	# 	enemy_pos[1] += SPEED
	# else:
	# 	enemy_pos[0] = random.randint(0,width-enemy_size)
	# 	enemy_pos[1] = 0

	if detect_collisions(player_pos,enemy_pos):
		game_over = True
		break

	drop_enemies(enemy_lst)
	score = update_enemy_positions(enemy_lst,score)
	SPEED = set_level(score,SPEED)

	text = "Score: " + str(score)
	label = myFont.render(text,1,YELLOW)
	screen.blit(label,(width-200,height-40))

	if collision_check(enemy_lst,player_pos):
		game_over = True
		break

	draw_enemies(enemy_lst)
	pygame.draw.rect(screen,RED,(player_pos[0],player_pos[1],player_size,player_size))        #rect(left, top, width, height)

	clock.tick(30)                              #this will play 30 frames per second
 
	pygame.display.update()                    #Update portions of the screen for software displays


