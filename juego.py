import pygame
import random
import os


#Inicializar pygame
pygame.init()

#Sonido
pygame.mixer.init()

#Creacion de la ventana del juego
screen = pygame.display.set_mode((1000,600))

clock = pygame.time.Clock()

#Stats y tiempo

stats_generacion = 1
stats_vivos = "1/1"
stats_velocidad = "1x"
stats_distancia = 0
stats_max_distancia = 0

tiempo_inicio = pygame.time.get_ticks()

#Fondo

fondo = pygame.image.load("assets/background.png")

#Musica de fondo
pygame.mixer.music.load("galaga_start.wav")
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.5)

#Efectos de sonido para el juego
sonido_disparo = pygame.mixer.Sound("galaga_shot.wav")
sonido_explosion = pygame.mixer.Sound("galaga_enemy_explosion.wav")
sonido_muerte = pygame.mixer.Sound("galaga_ship_hit.wav")

#Titulo e iconos
pygame.display.set_caption("The Flappy Bird")
icon = pygame.image.load("assets/pajarito.png")
pygame.display.set_icon(icon)

#Imagen del flappy bird

imagenPajarito = pygame.image.load("assets/bird.png").convert_alpha()
jugadorX = 300
jugadorY = 300
cambios_jugadorX = 0
velocidad_y = 0

SEMILLA = 67
random.seed(SEMILLA)

tubo_abajo_img = pygame.image.load("assets/tuberia_abajo.png").convert_alpha()
tubo_arriba_img = pygame.image.load("assets/tuberia_arriba.png").convert_alpha()
tub_abajo_inicial = tubo_abajo_img.get_rect(midtop=(900, 300 + 200//2))

tub_arriba_inicial = tubo_arriba_img.get_rect(midbottom=(900, 300 - 200//2))

lista_tuberias = [tub_abajo_inicial, tub_arriba_inicial]
CREARTUBERIA = pygame.USEREVENT
pygame.time.set_timer(CREARTUBERIA, 1200)


panel_rect = pygame.Rect(800, 0, 300, 600)
PANEL_COLOR = (16, 16, 16)
TITULO_COLOR = (255, 255, 0)
TEXTO_COLOR = (255, 255, 255)

titulo_fuente = pygame.font.Font(None, 35)
texto_fuente = pygame.font.Font(None, 30)


def crear_tuberia():   
    espacio = random.randint(150, 250)
    espacio_altura = random.randint(200, 500)
   
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

def estadisticas():
    pygame.draw.rect(screen, PANEL_COLOR, panel_rect)

    x_pos = 800
    y_pos = 20

    titulo = titulo_fuente.render("GA Statistics", True, TITULO_COLOR)
    screen.blit(titulo, (x_pos, y_pos))
    y_pos += 40

    linea_generacion = texto_fuente.render(f"Generation: {stats_generacion}", True, TEXTO_COLOR)
    screen.blit(linea_generacion, (x_pos, y_pos))
    y_pos += 30

    linea_vivos = texto_fuente.render(f"Alive: {stats_vivos}", True, TEXTO_COLOR)
    screen.blit(linea_vivos, (x_pos, y_pos))
    y_pos += 30

    linea_velocidad = texto_fuente.render(f"Speed: {stats_velocidad}", True, TEXTO_COLOR)
    screen.blit(linea_velocidad, (x_pos, y_pos))
    y_pos += 60

    linea_distancia = texto_fuente.render(f"Distance: {stats_distancia}", True, TEXTO_COLOR)
    screen.blit(linea_distancia, (x_pos, y_pos))
    y_pos += 30

    linea_distancia_max = texto_fuente.render(f"Max Distance: {stats_max_distancia}", True, TEXTO_COLOR)
    screen.blit(linea_distancia_max, (x_pos, y_pos))
    y_pos += 30
    
    linea_pajarito = texto_fuente.render(f"Bird Y: {(-(int(jugadorY)-600))}", True, TEXTO_COLOR)
    screen.blit(linea_pajarito, (x_pos, y_pos))
    y_pos += 30

    tiempo_segundos = (pygame.time.get_ticks() - tiempo_inicio) // 1000
    linea_tiempo = texto_fuente.render(f"Time: {tiempo_segundos}s / 120s", True, TEXTO_COLOR)
    screen.blit(linea_tiempo, (x_pos, y_pos))




def colisiones(pajarito_rect, tuberias):
    
    for tubo_rect in tuberias:
        if pajarito_rect.colliderect(tubo_rect):
            sonido_muerte.play()
            return False
    
    if pajarito_rect.top <= 0 or pajarito_rect.bottom >= 550:
        sonido_muerte.play() 
        return False
    
    return True

def reset():

    global tiempo_inicio
    
    random.seed(SEMILLA)
    
    jugadorY = 300
    velocidad_y = 0

    tub_abajo_inicial = tubo_abajo_img.get_rect(midtop=(900, 300 + 200//2))
    tub_arriba_inicial = tubo_arriba_img.get_rect(midbottom=(900, 300 - 200//2))
    lista_tuberias = [tub_abajo_inicial, tub_arriba_inicial]

    stats_distancia = 0

    pygame.time.set_timer(CREARTUBERIA, 0)
    pygame.time.set_timer(CREARTUBERIA, 1200)

    tiempo_inicio = pygame.time.get_ticks()

    return jugadorY, velocidad_y, lista_tuberias, stats_distancia


#Game Loop
running = True
game_on = False
while running:
    
    #RGB - Colores - Rojo, Verde, Azul  
    screen.fill((0,0,0))

    #Imagen de fondo
    screen.blit(fondo, (0,0))
    
    

    clock.tick(60) 

    for event in pygame.event.get():


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_SPACE:
                if game_on:
                    velocidad_y = -10
                    sonido_disparo.play()
                else:
                    jugadorY, velocidad_y, lista_tuberias, stats_distancia = reset()
                    game_on = True
        
        elif event.type == pygame.QUIT:
            running = False
        
        if event.type == CREARTUBERIA:
            lista_tuberias.extend(crear_tuberia())

    if game_on:  

            # controlar el tiempo que lleva la partida
            tiempo_actual = (pygame.time.get_ticks() - tiempo_inicio)/ 1000

            if tiempo_actual >= 120:


                game_on = False

            #Pajarito y sus caracteristicas
            velocidad_y += 0.5
            jugadorY += velocidad_y

            game_on = colisiones(imagenPajarito.get_rect(topleft=(jugadorX, jugadorY)), lista_tuberias)
                    
            for tubo in lista_tuberias:
                tubo.centerx -= 5

            lista_tuberias = [tubo for tubo in lista_tuberias if tubo.right > -50]
                    
            stats_distancia += 1
            if stats_distancia > stats_max_distancia:
                stats_max_distancia = stats_distancia

            jugador(jugadorX, jugadorY, lista_tuberias)
            
    else:
        
        jugador(jugadorX, jugadorY, lista_tuberias)

        empezar = texto_fuente.render("Press SPACE to Start", True, (255, 255, 255))
        empezar_rect = empezar.get_rect(center=(500, 300))
        screen.blit(empezar, empezar_rect)

    estadisticas()
    pygame.display.update()

pygame.quit()
