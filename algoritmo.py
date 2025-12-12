import random

class Genomas_Pajaros:
    '''
    Representa los 6 genomas(pesos) de los pajaros que deifinen el comportamiento del aleteo
    '''
    def __init__(self,w0:float,w1:float,w2:float,w3:float,w4:float,w5:float):
        '''
        Inicializa los pesos que van a tener los genomas de los pajaros

        Parametros:

        w0,w1,w2,w3,w4,w5:floats
        (Pesos genomas que defininen si el pajaro aletea o no aletea)

        '''
        self.w0 = w0
        self.w1 = w1
        self.w2 = w2
        self.w3 = w3
        self.w4 = w4
        self.w5 = w5

    def asignacion_random(escala:float=5.0)-> "Genomas_Pajaros":
        '''
        Genera un genoma aleatorio usando usando el rango de [-escala, escala] repartiendo los valores de manera uniforme

        Parametros:

        escala: float
        Establecido en 5 y va de [-5 a 5]

        Inicia Genoma_Pajaros con pesos generados aleatoriamente

        '''
        return Genomas_Pajaros(
            random.uniform(-escala,escala),
            random.uniform(-escala,escala),
            random.uniform(-escala,escala),
            random.uniform(-escala,escala),
            random.uniform(-escala,escala),
            random.uniform(-escala,escala)
            )
    
    def aleteo(self,delta_y:float,delta_x:float,velocidad_y:float)->bool:
        '''
        Decide si va a aletear o no usando la formula de la consigna

        La decision de si va a aletear o no se basa en:
        - diferencia vertical respecto al objetivo (delta_y)
        - diferencia horizonta entre la tuberia y la nava (delta_x)
        - la velocidad en la que se mueven las tuberias (velocidad_y)
        - los pesos de los genomas de los pajaros(w0...w5)

        Parametros:
        delta_y : float
        - distancia entre la nave y la abertura del tubo
        delta_x : float
        - distancia entre el tubo y la nave
        velocidad_y: float
        - velocidad de la nave

        Retorna: Bool
        dependiendo que retorne aletea o no aletea
        '''
        aletear = (self.w0 + self.w1*delta_y + self.w2 * (delta_y**2)+ self.w3 * delta_x + self.w4 * (delta_x**2)+ self.w5 * velocidad_y)
        if aletear > 0:
            return True
        else:
            return False
    
    def cruce_uniforme (gen_a : "Genomas_Pajaros", gen_b : "Genomas_Pajaros", probabilidad_cruce: float = 0.5)-> "Genomas_Pajaros":
        '''

        Genera una Cria de pajaro en base a un gen_a(padre/madre) y otro gen_b(padre/madre) mediante un cruce uniforme
        
        Parametros:
        
        gen_a : Padre/Madre
        gen_b : Padre/Madre

        probabilidad_cruce : 
        Chances de generar un gen del gen_a es probabilidad_cruce y de generar uno del gen_b es de 1-probabilidad_cruce

        Parametros:
        gen_a: Genoma_pajaro
        - Genoma del primer progenitor
        gen_b: Genoma_pajaro
        - Genoma del segundo progenitor
        probabilidad_cruce:float
        - Probabilidad que hay para que elija un gen

        Retorna:
        Nuevo genoma resultante del cruce

        '''
        genes_a = [gen_a.w0,gen_a.w1,gen_a.w2,gen_a.w3,gen_a.w4,gen_a.w5]
        genes_b = [gen_b.w0,gen_b.w1,gen_b.w2,gen_b.w3,gen_b.w4,gen_b.w5]
        genes_cria = []
        for ga,gb in zip(genes_a,genes_b):
            if random.random() < probabilidad_cruce: #random.random() devuelve netre 0 y 1
                genes_cria.append(ga)
            else:
                genes_cria.append(gb)
        
        return Genomas_Pajaros(*genes_cria)
    
    def mutacion (self, probabilidad_mutacion :float = 0.1, sigma: float = 0.5)-> None:
        '''
        Aplica la mutación a los genes del genoma con cierta probabilidad por gen

        Parametros:

        probabilidad_mutacion: 
        probabilidad de que cada gen mute
        sigma: 
        desviacion estandar del ruido gaussiano agregado al gen, en el archivo de pygame, armamos una fuerza de mutacion, 
        arranca en 1 hasta que llega a 0.5

        '''
        gen = [self.w0,self.w1,self.w2,self.w3,self.w4,self.w5]
        for i in range(len(gen)):
            if random.random() < probabilidad_mutacion:
                gen[i] += random.gauss(0.0,sigma)
        self.w0,self.w1,self.w2,self.w3,self.w4,self.w5 = gen

class Pajaro:
    """
    Representa un pájaro del algoritmo genético.

    Cada pájaro tiene:
    - genomas: Genomas_Pajaro 
        los pesos (w0..w5)
    - y: float 
        posición vertical en el juego
    - vel_y: float
        velocidad vertical
    - distancia_recorrida: float
        distancia recorrida en el juego (base del fitness)
    - vivo: Bool
        si sigue en juego
    - tiempo_vivo: float
        tiempo total que el pajaro esta vivo
    - estado_fisico: float
        valor de aptitud (fitness)

    """
    def __init__(self,genomas,y_inicial=300.0):
        '''
        Inicializa un pajaro con un conjunto de genomas y posicion inicial

        Parametros:
        genomas: Genomas_pajaro (w0...w5)
            Va a decidir si aletea
        y_inicial: float
            posicion en la que arranca el pajaro el juego
        '''
        self.genomas = genomas
        self.y = y_inicial
        self.velocidad_y = 0.0
        self.distancia_recorrida = 0.0
        self.vivo = True
        self.tiempo_vivo = 0.0
        self.estado_fisico = 0.0
    
    def reiniciar_pajaro(self,y_inicial=300.0):
        """
        Reinicia el pájaro a su estado inicial.

        Parametros:
        y_inicial: float
            vuelve al pajaro en su posicion inicial
        
        Retorna:
        self:
            Misma instancia del pajaro, reiniciada
        """
        self.y = y_inicial
        self.velocidad_y = 0.0
        self.distancia_recorrida = 0.0
        self.vivo = True
        self.tiempo_vivo = 0.0
        self.estado_fisico = 0.0
        return self
    
    def decidir_aleteo(self,delta_y,delta_x,velocidad_y):
        '''
        LLama a los genomas previamente generados para ver si aletea o no

        Parametros:
        delta_y : float
        - distancia entre la nave y la abertura del tubo
        delta_x : float
        - distancia entre el tubo y la nave
        velocidad_y: float
        - velocidad de la nave

        Retorna: Bool
        dependiendo que retorne aletea o no aletea

        '''
        return self.genomas.aleteo(delta_y,delta_x,velocidad_y)
    
    def actualizacion_fisica(self):
        ''''
        Actualiza la posicion del pajaro aplicando la gravedad y la velocidad
        '''
        self.velocidad_y += 0.5
        self.y += self.velocidad_y
    
    def aletear(self):
        '''
        Aplica el aleteo del pajaro haciendo un salto

        Hace que la velocidad vertical tome un valor negativo provocando que el pajaro suba
        '''
        self.velocidad_y = -10
    
    def calcular_estado_fisico(self):
        '''
        Usa la distancia recorrida como la base de la aptitud fisica de ese pajaro
        '''
        self.estado_fisico = self.distancia_recorrida
        return self.estado_fisico

