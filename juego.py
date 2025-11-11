import pygame

#Inicializar pygame
pygame.init()

#Creacion de la ventana del juego
screen = pygame.display.set_mode((1000,600))


clock = pygame.time.Clock()

#Fondo

fondo = pygame.image.load("background.png")

#Titulo e iconos
pygame.display.set_caption("The Flappy Bird")
icon = pygame.image.load("/Users/marialaurariande/Downloads/pajarito.png")
pygame.display.set_icon(icon)

#Imagen del flappy bird

imagenPajarito = pygame.image.load("bird.png").convert_alpha()
jugadorX = 500
jugadorY = 300
cambios_jugadorX = 0
velocidad_y = 0

tubo_abajo_img = pygame.image.load("tub_abajo_100.png").convert_alpha()
tubo_arriba_img = pygame.image.load("tub_arriba_100.png").convert_alpha()

tubo_x = 350
hueco = 200
hueco_y = 300

tubo_abajo_rect = tubo_abajo_img.get_rect()
tubo_abajo_rect.x = tubo_x
tubo_abajo_rect.y = hueco_y + (hueco // 2)

tubo_arriba_rect = tubo_arriba_img.get_rect()
tubo_arriba_rect.x = tubo_x
tubo_arriba_rect.y = hueco_y - (hueco // 2) - tubo_arriba_rect.height





def jugador(x,y):
    
    screen.blit(tubo_abajo_img, tubo_abajo_rect)
    screen.blit(tubo_arriba_img, tubo_arriba_rect)
    screen.blit(imagenPajarito, (x, y))


#Game Loop
running = True
while running:

    clock.tick(60)

    #RGB - Colores - Rojo, Verde, Azul  
    screen.fill((0,0,0))

    #Imagen de fondo
    screen.blit(fondo, (0,0))
    
    for event in pygame.event.get():


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_SPACE:
                velocidad_y = -10
        
        elif event.type == pygame.QUIT:
            running = False
    
    velocidad_y += 0.5
    jugadorY += velocidad_y

    if jugadorY < 0:
            jugadorY = 0
            velocidad_y = 0
    
    if jugadorY > 600 - imagenPajarito.get_height():
            jugadorY = 600 - imagenPajarito.get_height()
            velocidad_y = 0
            
            
    
    jugador(jugadorX, jugadorY)
    pygame.display.update()