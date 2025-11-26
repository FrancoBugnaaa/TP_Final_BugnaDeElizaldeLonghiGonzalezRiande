import pygame
import math
import random
from algoritmo import Genomas_Pajaros, Pajaro

from pygame import mixer

#Constantes GA
TAMANO_POBLACION = 100
PROB_CRUCE = 0.5
PROB_MUTACION = 0.1
SELECCION_ELITE = 2

#Constantes Juego
FPS = 60
MAX_TIME = 120

WIDTH, HEIGHT = 1000,600
GRAVEDAD = 0.5
VELOCIDAD_TUBERIAS = 5
GAP_ALTURA = 200
jugadorX = 300
LIMITE_SUELO = 550
BIRDS_2MIN = 50

#Escalas para normalizar las cosas
MAX_DELTA_Y = HEIGHT * 1.5
MAX_DELTA_X = WIDTH - jugadorX
MAX_VELOCIDAD_Y = 15

#Stats y tiempo
stats_generacion = 1
stats_velocidad = "1x"
mult_velocidad = 1
stats_distancia = 0
stats_max_distancia = 0
tiempo_actual = 0
promedio_distancia = 0
prev_gen = 0


#Inicializar pygame
pygame.init()

#Sonido
pygame.mixer.init()

#Creacion de la ventana del juego
screen = pygame.display.set_mode((WIDTH,HEIGHT))

clock = pygame.time.Clock()

poblacion = []
pajaros_vivos = []

tiempo_inicio = pygame.time.get_ticks()

#Fondo
fondo = pygame.image.load("assets/espacio.png")    

#Musica de fondo
mixer.music.load("background.wav")
mixer.music.play(-1)


#Titulo e iconos
pygame.display.set_caption("The Flappy Space Ship")
icon = pygame.image.load("assets/nave.png")
pygame.display.set_icon(icon)

explosion = pygame.image.load("assets/explosion.png").convert_alpha()

imagenPajarito = pygame.image.load("assets/nave.png").convert_alpha()
jugadorX = 300
jugadorY = 300
cambios_jugadorX = 0
velocidad_y = 0

tubo_abajo_img = pygame.image.load("assets/tuberia_abajo.png").convert_alpha()
tubo_arriba_img = pygame.image.load("assets/tuberia_arriba.png").convert_alpha()
tub_abajo_inicial = tubo_abajo_img.get_rect(midtop=(900, 300 + GAP_ALTURA//2))

tub_arriba_inicial = tubo_arriba_img.get_rect(midbottom=(900, 300 - GAP_ALTURA//2))

lista_tuberias = [tub_abajo_inicial, tub_arriba_inicial]
CREARTUBERIA = pygame.USEREVENT
pygame.time.set_timer(CREARTUBERIA, 1200)

propulsor_img = pygame.image.load("assets/propulsor.png").convert_alpha()

panel_rect = pygame.Rect(700, 0, 300, 600)
speed_rect = pygame.Rect(30, 520, 80, 50)
PANEL_COLOR = (16, 16, 16)
TITULO_COLOR = (255, 255, 0)
TEXTO_COLOR = (255, 255, 255)

titulo_fuente = pygame.font.Font(None, 35)
texto_fuente = pygame.font.Font(None, 25)
texto_mini = pygame.font.Font(None, 20)


def crear_tuberia():   
    espacio = random.randint(150, 250)
    espacio_altura = random.randint(200, 400)
   
    tub_abajo = tubo_abajo_img.get_rect(midtop=(1000, espacio_altura + espacio//2))
    
    tub_arriba = tubo_arriba_img.get_rect(midbottom=(1000, espacio_altura - espacio//2))

    return tub_abajo, tub_arriba


def jugador(x,y,tuberias):
    for tubo in tuberias:
         if tubo.bottom >= 600:
              screen.blit(tubo_abajo_img, tubo)
         else:
            screen.blit(tubo_arriba_img, tubo)

def estadisticas():
    pygame.draw.rect(screen, PANEL_COLOR, panel_rect)

    x_pos = 710
    y_pos = 20

    titulo = titulo_fuente.render("GA Statistics", True, TITULO_COLOR)
    screen.blit(titulo, (x_pos, y_pos))
    y_pos += 40

    linea_generacion = texto_fuente.render(f"Generation: {stats_generacion}", True, TEXTO_COLOR)
    screen.blit(linea_generacion, (x_pos, y_pos))
    y_pos += 30

    linea_vivos = texto_fuente.render(f"Alive: {len(pajaros_vivos)}/{TAMANO_POBLACION}", True, TEXTO_COLOR)
    screen.blit(linea_vivos, (x_pos, y_pos))
    y_pos += 30

    linea_prev_gen = texto_fuente.render(f"Prev Gen 2min: {prev_gen}", True, TEXTO_COLOR)
    screen.blit(linea_prev_gen, (x_pos, y_pos))
    y_pos += 30

    linea_velocidad = texto_fuente.render(f"Speed: {stats_velocidad}", True, TEXTO_COLOR)
    screen.blit(linea_velocidad, (x_pos, y_pos))
    y_pos += 60

    linea_distancia = texto_fuente.render(f"Current Distance: {stats_distancia}", True, TEXTO_COLOR)
    screen.blit(linea_distancia, (x_pos, y_pos))
    y_pos += 30

    linea_distancia_max = texto_fuente.render(f"Max Distance: {int(stats_max_distancia)}", True, TEXTO_COLOR)
    screen.blit(linea_distancia_max, (x_pos, y_pos))
    y_pos += 30

    linea_distancia_avg = texto_fuente.render(f"Avg Distance: {int(promedio_distancia)}", True, TEXTO_COLOR)
    screen.blit(linea_distancia_avg, (x_pos, y_pos))
    y_pos += 60
    
    tiempo_segundos = int(tiempo_actual)
    linea_tiempo = texto_fuente.render(f"Time: {tiempo_segundos}s / 120s", True, TEXTO_COLOR)
    screen.blit(linea_tiempo, (x_pos, y_pos))
    y_pos += 40

    dibujar_genomas(screen, x_pos, y_pos, poblacion)

    pygame.draw.rect(screen, PANEL_COLOR, speed_rect)
    pygame.draw.rect(screen, (255, 255, 255), speed_rect, 3)
    cuadrado_velocidad = titulo_fuente.render(stats_velocidad, True, TEXTO_COLOR)
    velocidad_rect = cuadrado_velocidad.get_rect(center=speed_rect.center)
    screen.blit(cuadrado_velocidad, velocidad_rect)

muertes = []

def colisiones(pajarito_rect, tuberias):
    
    for tubo_rect in tuberias:
        if pajarito_rect.colliderect(tubo_rect):
            
            #sonido_de_explosion
            # explosion = mixer.Sound("explosion.wav")
            # explosion.Sound.play()

            muertes.append(pajarito_rect)
            

            return False
        
    
    if pajarito_rect.top <= 0 or pajarito_rect.bottom >= 550:
        #sonido_de_explosion
        # explosion = mixer.play("explosion.wav")
        # explosion.Sound.play()

        muertes.append(pajarito_rect)
        return False
    
    return True

def reset():

    global tiempo_inicio, jugadorY,velocidad_y,lista_tuberias,stats_distancia, promedio_distancia, tiempo_actual
    
    # random.seed(SEMILLA)
    
    jugadorY = 300
    velocidad_y = 0

    tub_abajo_inicial = tubo_abajo_img.get_rect(midtop=(900, 300 + 200//2))
    tub_arriba_inicial = tubo_arriba_img.get_rect(midbottom=(900, 300 - 200//2))
    
    lista_tuberias = [tub_abajo_inicial, tub_arriba_inicial]

    stats_distancia = 0

    tiempo_inicio = pygame.time.get_ticks()

    tiempo_actual = 0

    muertes.clear()

    return jugadorY, velocidad_y, lista_tuberias, stats_distancia

def generar_poblacion_inicial():
    """Genera primera población y resetea el mapa fijo."""
    global poblacion, pajaros_vivos, stats_generacion, stats_distancia

    poblacion = []
    for _ in range(TAMANO_POBLACION):
        genoma = Genomas_Pajaros.asignacion_random(escala=1.0)
        poblacion.append(Pajaro(genoma))

    # Reiniciar estado físico de todos los pájaros
    pajaros_vivos = [p.reiniciar_pajaro() for p in poblacion]

    stats_generacion = 1
    stats_distancia = 0


    reset()

def seleccion_y_evolucion():
    """Selección, cruce y mutación para formar la nueva generación."""
    global poblacion, pajaros_vivos, stats_generacion, stats_max_distancia, stats_distancia, promedio_distancia 

    stats_generacion += 1
    stats_distancia = 0

    # Ordenar por fitness (distancia_recorrida)
    poblacion.sort(key=lambda p: p.distancia_recorrida, reverse=True)

    mutation_strength = 0.5 * (1 + math.exp(-stats_generacion / 30))

    if poblacion:

        stats_max_distancia = max(stats_max_distancia, poblacion[0].distancia_recorrida)

        distancia_total = 0

        for i in range(len(poblacion)):
            distancia_total += poblacion[i].distancia_recorrida

    # Elitismo
    nueva_poblacion = [Pajaro(p.genomas) for p in poblacion[:SELECCION_ELITE]]

    fitness_total = sum(p.distancia_recorrida for p in poblacion)

    promedio_distancia = (distancia_total // len(poblacion))


    def seleccionar_padre():
        if fitness_total == 0:
            return random.choice(poblacion).genomas

        r = random.uniform(0, fitness_total)
        acumulado = 0
        for pajaro in poblacion:
            acumulado += pajaro.distancia_recorrida
            if acumulado > r:
                return pajaro.genomas
        return poblacion[0].genomas

    while len(nueva_poblacion) < TAMANO_POBLACION:
        padre1 = seleccionar_padre()
        padre2 = seleccionar_padre()

        hijo_genoma = Genomas_Pajaros.cruce_uniforme(padre1, padre2, PROB_CRUCE)
        hijo_genoma.mutacion(PROB_MUTACION, mutation_strength)

        nueva_poblacion.append(Pajaro(hijo_genoma))

    poblacion = nueva_poblacion
    pajaros_vivos = [p.reiniciar_pajaro() for p in poblacion]

    reset()

def dibujar_genomas(surface, x_start, y_start, poblacion):
    scale = 35        
    bar_height = 16  
    espaciado = 28 
    bg_width = 150    
    center_x = x_start + 150 

    titulo = texto_fuente.render("Genome (Avg ± Std)", True, (255, 255, 255))
    surface.blit(titulo, (x_start, y_start))
    y_start += 35

    if not poblacion:
        return

    labels = ["w0", "w1(Δy)", "w2(Δy²)", "w3(Δx)", "w4(Δx²)", "w5(Vy)"]

    for i in range(6):
        nombre_peso = f"w{i}"
        valores = [getattr(p.genomas, nombre_peso) for p in poblacion]
        
        promedio = sum(valores) / len(valores)
        varianza = sum((x - promedio) ** 2 for x in valores) / len(valores)
        desviacion = math.sqrt(varianza)

        draw_y = y_start

        lbl = texto_mini.render(labels[i], True, (180, 180, 180))
        surface.blit(lbl, (x_start, y_start))
        bg_rect = pygame.Rect(center_x - bg_width // 2, draw_y, bg_width, bar_height)
        pygame.draw.rect(surface, (40, 40, 40), bg_rect) 
        pygame.draw.rect(surface, (70, 70, 70), bg_rect, 1) 

        start_dev = (promedio - desviacion) * scale
        width_dev = (desviacion * 2) * scale
        
        if width_dev > bg_width: width_dev = bg_width 
        
        rect_dev = pygame.Rect(center_x + start_dev, draw_y, width_dev, bar_height)
        pygame.draw.rect(surface, (100, 100, 100), rect_dev) 
        
        color = (0, 255, 0) if promedio >= 0 else (255, 0, 0)
        largo_promedio = promedio * scale
        
        limit_px = bg_width // 2
        if largo_promedio > limit_px: largo_promedio = limit_px
        if largo_promedio < -limit_px: largo_promedio = -limit_px

        if promedio >= 0:
            rect_avg = pygame.Rect(center_x, draw_y, largo_promedio, bar_height)
        else:
            rect_avg = pygame.Rect(center_x + largo_promedio, draw_y, -largo_promedio, bar_height)
            
        pygame.draw.rect(surface, color, rect_avg)
        pygame.draw.line(surface, (250, 250, 250), (center_x, draw_y), (center_x, draw_y + bar_height), 1)

        val_txt = texto_fuente.render(f"{promedio:.2f}", True, (255, 255, 255))
        surface.blit(val_txt, (center_x + bg_width//2 + 10, y_start))

        y_start += espaciado
        
#Game Loop
generar_poblacion_inicial()
running = True
game_on = True
while running:
    #RGB - Colores - Rojo, Verde, Azul  
    screen.fill((0,0,0))

    #Imagen de fondo
    screen.blit(fondo, (0,0))


    deltatime = clock.tick(FPS)

    deltatime_factor = (deltatime / 16.66)* mult_velocidad
    if deltatime_factor > 10: deltatime_factor = 10


    for event in pygame.event.get():


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                


            # if event.key == pygame.K_SPACE:
            #     if game_on:
            #         velocidad_y = -10
            #         #sonido_disparo.play()
            #     else:
            #         jugadorY, velocidad_y, lista_tuberias, stats_distancia = reset()
            #         game_on = True

            if event.key == pygame.K_1:
                mult_velocidad = 1.0
                stats_velocidad = "1x"
            elif event.key == pygame.K_2:
                mult_velocidad = 2.0
                stats_velocidad = "2x"
            elif event.key == pygame.K_3:
                mult_velocidad = 5.0 
                stats_velocidad = "3x"



        elif event.type == pygame.QUIT:
            running = False
        
    if game_on:  



            # controlar el tiempo que lleva la partida
            tiempo_actual += (deltatime * mult_velocidad) / 1000.

            if tiempo_actual >= MAX_TIME and len(pajaros_vivos) < BIRDS_2MIN:
                prev_gen = len(pajaros_vivos)
                Pajaro.vivo = False
                pajaros_vivos.clear()
                seleccion_y_evolucion()
                continue

            elif tiempo_actual >= MAX_TIME and len(pajaros_vivos) >= BIRDS_2MIN:
                game_on = False


            #game_on = colisiones(imagenPajarito.get_rect(topleft=(jugadorX, jugadorY)), lista_tuberias)
                    
            for tubo in lista_tuberias:
                tubo.centerx -= VELOCIDAD_TUBERIAS * deltatime_factor
            
            for muerte in muertes:
                muerte.centerx -= VELOCIDAD_TUBERIAS * deltatime_factor

            for muerte in muertes:
                screen.blit(explosion, muerte)            

            lista_tuberias = [tubo for tubo in lista_tuberias if tubo.right > -50]

            ultima_tuberia = lista_tuberias[-1]
            if WIDTH - ultima_tuberia.centerx >= 400:
                tub_abajo, tub_arriba = crear_tuberia()
                lista_tuberias.append(tub_abajo)
                lista_tuberias.append(tub_arriba)

            next_pipe = None
            for tubo in lista_tuberias:
                if tubo.right > jugadorX:
                    if next_pipe is None or tubo.left < next_pipe.left:
                        next_pipe = tubo
            
            nuevos_vivos = []
            for pajaro in pajaros_vivos:

                pajaro.velocidad_y += GRAVEDAD * deltatime_factor
                pajaro.y += pajaro.velocidad_y * deltatime_factor

                if next_pipe is not None:
                    next_pipe_center = next_pipe.bottom + GAP_ALTURA//2 

                    delta_y_cruda = next_pipe_center - pajaro.y
                    delta_x_cruda = next_pipe.left - jugadorX

                    delta_y_escalada = delta_y_cruda / MAX_DELTA_Y
                    delta_x_escalada = delta_x_cruda / MAX_DELTA_X
                    vel_escalada    = pajaro.velocidad_y / MAX_VELOCIDAD_Y
                    
                    if pajaro.decidir_aleteo(delta_y_escalada, delta_x_escalada, vel_escalada):
                        pajaro.aletear()
                
                pajaro_rect = imagenPajarito.get_rect(topleft=(jugadorX, pajaro.y))
                if colisiones(pajaro_rect, lista_tuberias):
                    nuevos_vivos.append(pajaro)
                    pajaro.distancia_recorrida += 1 * deltatime_factor
                    pajaro.tiempo_vivo += 1 * deltatime_factor
                else:
                    pajaro.vivo = False
                
            pajaros_vivos = nuevos_vivos

            if not pajaros_vivos:
                prev_gen = 0
                seleccion_y_evolucion()
                continue

            mejor = max(pajaros_vivos, key=lambda p: p.distancia_recorrida)
            jugadorY = mejor.y
            velocidad_y = mejor.velocidad_y

                    
            stats_distancia += int(1*deltatime_factor)
            if stats_distancia > stats_max_distancia:
                stats_max_distancia = stats_distancia

            jugador(jugadorX,jugadorY,lista_tuberias)

            for pajaro in pajaros_vivos:
            # Propulsor de cada pájaro que esté subiendo
                if pajaro.velocidad_y < 0:
                    propulsor_rect = propulsor_img.get_rect(
                        center=(
                        jugadorX + imagenPajarito.get_width() // 2 - 30,
                        pajaro.y + imagenPajarito.get_height() // 2
                            )
                    )
                    screen.blit(propulsor_img, propulsor_rect)

                screen.blit(imagenPajarito, (jugadorX, pajaro.y))
    else:
        # Dibujamos las tuberías
        jugador(jugadorX, jugadorY, lista_tuberias)

        # Dibujamos todos los pájaros congelados donde quedaron
        for pajaro in pajaros_vivos:
            if pajaro.velocidad_y < 0:
                propulsor_rect = propulsor_img.get_rect(
                center=(
                    jugadorX + imagenPajarito.get_width() // 2 - 30,
                    pajaro.y + imagenPajarito.get_height() // 2
                    )
                )
                screen.blit(propulsor_img, propulsor_rect)

            screen.blit(imagenPajarito, (jugadorX, pajaro.y))

        if tiempo_actual >= 120 and len(pajaros_vivos) == BIRDS_2MIN:
                
                goal = texto_fuente.render("Goal Reached", True, (255, 255, 255))
                goal_rect = goal.get_rect(center=(500, 275))
                screen.blit(goal, goal_rect)

                endgame = texto_fuente.render("Press ESC to Exit", True, (255, 255, 255))
                endgame_rect = endgame.get_rect(center=(500, 300))
                screen.blit(endgame, endgame_rect)



    estadisticas()
    pygame.display.update()

pygame.quit()
