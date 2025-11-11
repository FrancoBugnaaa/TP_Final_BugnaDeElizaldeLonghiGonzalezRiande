import pygame

#Inicializar pygame
pygame.init()

#Creacion de la ventana del juego
screen = pygame.display.set_mode((1000,600))

#Titulo e iconos
pygame.display.set_caption("The Flappy Bird")
icon = pygame.image.load("/Users/marialaurariande/Downloads/pajarito.png")
pygame.display.set_icon(icon)
#Game Loop


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #RGB - Colores - Rojo, Verde, Azul        
    screen.fill((51,255,255))
    pygame.display.update()