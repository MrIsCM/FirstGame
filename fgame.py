#==================================
#	Ismael Charpentier Martín
#
#			02/03/2021
#
# 	  --Primer juego con Pygame--
#==================================


import pygame

pygame.init()
pygame.font.init()
pygame.mixer.init()

# Declaro ciertas constantes utiles

WIDTH, HEIGHT = 900, 500 						# Ancho y alto de la ventana
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) 	# Creacion per se de la ventana

MAX_BULLETS = 5
BULLET_WIDTH, BULLET_HEIGHT = 6, 4

pygame.display.set_caption("First Game") 		# Caption de la ventana

# Definicion de colores como tuples
# Formato RBG. ([0, 255], x3)

WHITE = (255, 255, 255) 		 				# Defino el color blanco en RGB (fondo)
BLACK = (0, 0, 0) 								# Defino el color negro en RBG
RED = (255, 0, 0)
PURPLISH = (171, 74, 233)


FPS = 60										# Defino el ratio de FPS
VEL = 5  										# Velocidad movimiento

SHIP_WIDTH, SHIP_HEIGHT = 60, 40 				# Ancho y alto de los rectangulos de las naves
BORDER_WIDTH = 2 								# Ancho del borde


#====================================================
# Creo mis eventos para los 'hit'
LEFT_HIT = pygame.USEREVENT + 1
RIGHT_HIT = pygame.USEREVENT + 2
#====================================================

#================================
# Creo las imagenes de las naves
#================================

LEFT_SHIP = pygame.image.load('Assets/ship2x2.png') 	# Cargo la imagen de la nave (Iz)
																# Escalo y roto la imagen (Iz)
LEFT_SHIP.set_colorkey((0, 0, 0))
LEFT_SHIP.convert()  

RIGHT_SHIP = pygame.image.load('Assets/spaceship_red.png') 		# Cargo la imagen de la nave (De)
																# Escalo y roto la imagen (De)
RIGHT_SHIP = pygame.transform.rotate(pygame.transform.scale(RIGHT_SHIP, (SHIP_WIDTH, SHIP_HEIGHT)), 270)


#======================================================================
# Separacion del medio

BORDER = pygame.Rect((WIDTH - BORDER_WIDTH)/2, 0, BORDER_WIDTH, HEIGHT)

#======================================================================

BACKGROUND = pygame.transform.scale(pygame.image.load('Assets/BG4.png'), (WIDTH, HEIGHT))

#======================================================
# TEXTO DE VIDAS
HEALTH_FONT = pygame.font.SysFont('TimesNewRoman', 40)
WINNER_FONT = pygame.font.SysFont('TimesNewRoman', 80)
 # font = pygame.font.SysFont(None, 40) 	# Desuso
#======================================================



#===============================================
# Funcion draw que voy a llamar para representar 
# los objetos por pantalla
#===============================================
def draw_window(left, right, left_bullets, right_bullets, l_health, r_health): 
	WIN.blit(BACKGROUND, (0, 0)) 							# Ventana
	#pygame.draw.rect(WIN, WHITE, BORDER)

	text_lhealth = HEALTH_FONT.render("Health: " + str(l_health), 1, RED)
	text_rhealth = HEALTH_FONT.render("Health: " + str(r_health), 1, RED)
	text_lhealth.set_alpha(200)
	text_rhealth.set_alpha(200)

	WIN.blit(text_lhealth, (50, 20))
	WIN.blit(text_rhealth, (700, 20))

	WIN.blit(LEFT_SHIP, (left.x, left.y)) 		
	WIN.blit(RIGHT_SHIP, (right.x, right.y))
	

	for bullet in left_bullets:
		pygame.draw.rect(WIN, RED, bullet)
	for bullet in right_bullets:
		pygame.draw.rect(WIN, RED, bullet)

	pygame.display.update()


def left_movement(keys_pressed, left):
	
	if keys_pressed[pygame.K_a] and left.x - VEL > 0: 										# Left
		left.x -= VEL

	if keys_pressed[pygame.K_d] and left.x + VEL < WIDTH/2 - LEFT_SHIP.get_width(): 		# Right
		left.x += VEL

	if keys_pressed[pygame.K_w] and left.y - VEL > 0: 										# Up
		left.y -= VEL

	if keys_pressed[pygame.K_s] and left.y + VEL < HEIGHT - LEFT_SHIP.get_height(): 		# Down
		left.y += VEL


	# El problema con esta forma es que dispara multiples proyectiles a la vez llegan al limite maximo en fraccion de segundos

	#if keys_pressed[pygame.K_SPACE] and len(left_bullets) <= MAX_BULLETS:
	#	left_bullets.append(pygame.Rect(left.x + LEFT_SHIP.get_width(), left.y + LEFT_SHIP.get_height()/2, BULLET_WIDTH, BULLET_HEIGHT))

def right_movement(keys_pressed, right):
	
	if keys_pressed[pygame.K_LEFT] and right.x - VEL > WIDTH/2: 							# Left
		right.x -= VEL

	if keys_pressed[pygame.K_RIGHT] and right.x + VEL < WIDTH - RIGHT_SHIP.get_width(): 	# Right
		right.x += VEL

	if keys_pressed[pygame.K_UP] and right.y - VEL > 0: 									# Up
		right.y -= VEL

	if keys_pressed[pygame.K_DOWN] and right.y + VEL < HEIGHT - RIGHT_SHIP.get_height(): 	# Down
		right.y += VEL		

def handle_bullets(left_bullets, right_bullets, left, right):

	for bullet in left_bullets:
		bullet.x += VEL
		if right.colliderect(bullet):
			pygame.event.post(pygame.event.Event(RIGHT_HIT))
			left_bullets.remove(bullet)

		elif bullet.x > WIDTH:
			left_bullets.remove(bullet)

	for bullet in right_bullets:
		bullet.x -= VEL
		if left.colliderect(bullet):
			pygame.event.post(pygame.event.Event(LEFT_HIT))
			right_bullets.remove(bullet)
		elif bullet.x < 0:
			right_bullets.remove(bullet)

def draw_winner(text):
	draw_text = WINNER_FONT.render(text, 1, RED)
	WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))

	pygame.display.update()
	pygame.time.delay(5000)


def main(): 		# Separo el main donde voy a ejectura el while loop 
					# en si y llamar a las demas funciones

	left = pygame.Rect(WIDTH/10, HEIGHT/2, LEFT_SHIP.get_width(), LEFT_SHIP.get_height())
	right = pygame.Rect(8*WIDTH/10, HEIGHT/2, RIGHT_SHIP.get_width(), RIGHT_SHIP.get_height())

	l_health = 10
	r_health = 10

	left_bullets = []
	right_bullets = []


	clock = pygame.time.Clock()
	run = True
	while run:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and len(left_bullets) <= MAX_BULLETS:
					left_bullets.append(pygame.Rect(left.x + LEFT_SHIP.get_width(), left.y + LEFT_SHIP.get_height()/2, BULLET_WIDTH, BULLET_HEIGHT))
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RCTRL and len(right_bullets) <= MAX_BULLETS:
					right_bullets.append(pygame.Rect(right.x, right.y + RIGHT_SHIP.get_height()/2, BULLET_WIDTH, BULLET_HEIGHT))

			if event.type == LEFT_HIT:
				l_health -= 1

			if event.type == RIGHT_HIT:
				r_health -= 1

		winner_text = ""
		if r_health <= 0:
			winner_text = "Left Wins!"
		if l_health <= 0:
			winner_text = "Right Wins!"

		if winner_text != "":
			draw_winner(winner_text)
			break

		keys_pressed = pygame.key.get_pressed()
		left_movement(keys_pressed, left)
		right_movement(keys_pressed, right)

		handle_bullets(left_bullets, right_bullets, left, right)
		
		draw_window(left, right, left_bullets, right_bullets, l_health, r_health)
		
	pygame.quit()


if __name__ == '__main__':
	main()