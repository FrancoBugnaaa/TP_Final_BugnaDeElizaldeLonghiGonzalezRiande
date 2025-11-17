import pygame
import random

#Inicializar pygame
pygame.init()

#Creacion de la ventana del juego
screen = pygame.display.set_mode((1000,600))


clock = pygame.time.Clock()

#Fondo

fondo = pygame.image.load("background.png")

#Titulo e iconos
pygame.display.set_caption("The Flappy Bird")
icon = pygame.image.load("pajarito.png")
pygame.display.set_icon(icon)

#Imagen del flappy bird

imagenPajarito = pygame.image.load("bird.png").convert_alpha()
jugadorX = 500
jugadorY = 300
cambios_jugadorX = 0
velocidad_y = 0

tubo_abajo_img = pygame.image.load("tuberia_abajo.png").convert_alpha()
tubo_arriba_img = pygame.image.load("tuberia_arriba.png").convert_alpha()


def crear_tuberia():   
    espacio = random.randint(150, 250)
    espacio_altura = random.randint(100, 500)
   
    tub_abajo = tubo_abajo_img.get_rect(midtop=(1000, espacio_altura + espacio//2))
    
    tub_arriba = tubo_arriba_img.get_rect(midbottom=(1000, espacio_altura - espacio//2))
    return tub_abajo, tub_arriba


def jugador(x,y,tuberias):
    
    screen.blit(imagenPajarito, (x, y))

    for tubo in tuberias:
         if tubo.bottom >= 600:
              screen.blit(tubo_abajo_img, tubo)
         else:
            screen.blit(tubo_arriba_img, tubo)

tub_abajo_inicial = tubo_abajo_img.get_rect(midtop=(900, 300 + 200//2))

tub_arriba_inicial = tubo_arriba_img.get_rect(midbottom=(900, 300 - 200//2))

lista_tuberias = [tub_abajo_inicial, tub_arriba_inicial]
CREARTUBERIA = pygame.USEREVENT
pygame.time.set_timer(CREARTUBERIA, 1200)

def colisiones(pajarito_rect, tuberias):
    
    for tubo_rect in tuberias:
        if pajarito_rect.colliderect(tubo_rect):
            print("Colision")
            return False
    
    if pajarito_rect.top <= 0 or pajarito_rect.bottom >= 600:
        print("Colision")
        return False
    
    return True



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
        
        if event.type == CREARTUBERIA:
            lista_tuberias.extend(crear_tuberia())
    velocidad_y += 0.5
    jugadorY += velocidad_y

    running = colisiones(imagenPajarito.get_rect(topleft=(jugadorX, jugadorY)), lista_tuberias)
            
    for tubo in lista_tuberias:
        tubo.centerx -= 5

    lista_tuberias = [tubo for tubo in lista_tuberias if tubo.right > -50]
            
    
    jugador(jugadorX, jugadorY, lista_tuberias)
    pygame.display.update() 