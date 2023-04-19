import math

class Spring:
    def __init__(self, particle1, particle2, k, l0):
        self.p1 = particle1
        self.p2 = particle2
        self.k = k
        self.l0 = l0

    
    # Obtiene los componentes de la fuerza de respuesta del resorte con la ley de hooke y las añade a las particulas deseadas
    def apply_force(self, xj, xs = True):
        # Sirve para sacar los delta de la posicion
        dx = self.p2.x - self.p1.x
        dy = self.p2.y - self.p1.y
        distance = math.sqrt(math.pow(dx, 2)+math.pow(dy, 2))

        # Ley de hooke
        magnitude = self.k * (distance - self.l0) 

        # Calcula los componentes del vector de la fuerza ejercida por el muelle
        fx = magnitude * dx / (distance-0.000001)
        fy = magnitude * dy / (distance-0.000001)

        #aplica las fuerzas a las particulas 
        if(xj):
            #si la variable es true, aplica la fuerza, de lo contrario no lo hace
            self.p1.apply_force(fx, fy)
        if(xs):
            #si la variable es true, aplica la fuerza, de lo contrario no lo hace
            self.p2.apply_force(-fx, -fy)