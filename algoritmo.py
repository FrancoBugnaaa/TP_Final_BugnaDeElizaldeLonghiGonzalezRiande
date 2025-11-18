import random

class Genomas_Pajaros:
    '''Representa los 6 genomas de los pajaros'''
    def __init__(self,w0:float,w1:float,w2:float,w3:float,w4:float,w5:float):
        '''
        Designamos los pesos que van a tener los genomas de los pajaros

        Parametros:

        w0,w1,w2,w3,w4,w5(Pesos genomas que defininen si el pajaro aletea o no aletea)

        '''
        self.w0 = w0
        self.w1 = w1
        self.w2 = w2
        self.w3 = w3
        self.w4 = w4
        self.w5 = w5

    def asignacion_random(escala:float=1.0)-> "Genomas_Pajaros":
        '''
        Genera un genoma random usando usando el rango de [-escala, escala] repartiendo al mismo uniformemente

        Parametros:

        escala(Valor max absoluto de los pesos generados)

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
        aletear = (self.w0 + self.w1*delta_y + self.w2 * (delta_y**2)+ self.w3 * delta_x + self.w4 * (delta_x**2)+ self.w5 * velocidad_y)
        if aletear < 0:
            return False
        else:
            return True
    
    def cruce_uniforme (gen_a : "Genomas_Pajaros", gen_b : "Genomas_Pajaros", probabilidad_cruce: float = 0.5)-> "Genomas_Pajaros":
        '''

        Genera una Cria de pajaro en base a un gen_a(padre/madre) y otro gen_b(padre/madre) mediante un cruce uniforme
        
        Parametros:
        
        gen_a : Padre/Madre
        gen_b : Padre/Madre
        probabilidad_cruce : Chances de generar un gen del gen_a es p y de generar uno del gen_b es de 1-p

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
    
    def mutacion (self, probabilidad_mutacion :float = 0.1, sigma: float = 0.1)-> None:
        '''
        Aplica la mutación a los genes del genoma con cierta probabilidad por gen

        Parametros:

        probabilidad_mutacion: probabilidad de que cada gen mute
        sigma: desviacion estandar del ruido gaussiano agregado al gen

        '''
        gen = [self.w0,self.w1,self.w2,self.w3,self.w4,self.w5]
        for i in range(len(gen)):
            if random.random() < probabilidad_mutacion:
                gen[i] += random.gauss(0.0,sigma)
        self.w0,self.w1,self.w2,self.w3,self.w4,self.w5

class Pajaro:
    """
    Representa un pájaro del algoritmo genético.

    Cada pájaro tiene:
    - genomas: los pesos (w0..w5)
    - y: posición vertical en el juego
    - vel_y: velocidad vertical
    - distancia_recorrida: fitness básico
    - vivo: si sigue en juego
    """
    def __init__(self,genomas,y_inicial=300.0):
        self.genomas = genomas
        self.y = y_inicial
        self.velocidad_y = 0.0
        self.distancia_recorrida = 0.0
        self.vivo = True
        self.estado_fisico = 0.0
    
    def reiniciar_pajaro(self,y_inicial=300.0):
        """
        Reinicia el pájaro a su estado inicial.
        """
        self.y = y_inicial
        self.velocidad_y = 0.0
        self.distancia_recorrida = 0.0
        self.vivo = True
        self.estado_fisico = 0.0
    
    def decidir_aleteo(self,delta_y,deltay2,delta_x):
        '''
        LLama a los genomas previamente generados para ver si aletea o no
        '''
        return self.genomas.aleteo(delta_y,deltay2,delta_x,self.velocidad_y)
    
    def actualizacion_fisica(self):
        ''''
        Aplica la gravedad de pygame y mueve el pajaro
        '''
        self.velocidad_y += 0.5
        self.y += self.velocidad_y
    
    def aletear(self):
        '''
        Aplica el aleteo del pajaro haciendo un salto
        '''
        self.velocidad_y = -10
    
    def estado_fisico(self):
        '''
        Usa la distancia recorrida como la base de la aptitud fisica de ese pajaro
        '''
        self.estado_fisico = self.distancia_recorrida
        return self.estado_fisico

