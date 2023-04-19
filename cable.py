from particle import Particle
from spring import Spring
import pygame

class Cable:
    def __init__(self, anclajeX, anclajeY):
        self.colorCuerda = (20,20,20)
        self.colorGancho = (0,0,0)

        self.anclajeX = anclajeX
        self.anclajeY = anclajeY

        self._particles = []
        self._springs = []

        for i in range(14):
            if i==0:
                particle = Particle(self.anclajeX, self.anclajeY, 1, 0, self.colorGancho)
            else:
                particle = Particle(self.anclajeX, self.anclajeY + i*25 + 18, 1, 70, self.colorCuerda)
                
            if i > 0:
                spring = Spring(self._particles[i-1], particle, 50, 18)
                self._springs.append(spring)                
            self._particles.append(particle)
        self.agarrado = False

    def move(self, screen):


        #Aplica la gravedad a todas las particulas y actualiza su posicion
        for par in self._particles:
            #aplica la fuerza de gravedad en y
            par.apply_force(0, par.mass * par.gravity)
            #actualiza la posicion de la particula
            par.move(0.1)

            
            
        pygame.draw.rect(screen, self._particles[0].color, (self._particles[0].x - 15/2, self._particles[0].y - 10/2, 17, 15))

        for j in range(len(self._springs)):
            spring = self._springs[j]  
            if(j==0):
                spring.apply_force(False)
            elif(j==len(self._springs)-1 and (self.agarrado or self._particles[-1].gravity == 0)):
                spring.apply_force(True, False)
            else:
                spring.apply_force(True)
            pygame.draw.line(screen, self._particles[j].color, (spring.p1.x,spring.p1.y), (spring.p2.x,spring.p2.y), 9)

    def setClavPos(self, x,y):
        self._particles[len(self._particles)-1].x = x
        self._particles[len(self._particles)-1].y = y
        self._particles[len(self._particles)-1].vy = 0
        self._particles[len(self._particles)-1].gravity = 0
        self._particles[len(self._particles)-1].ay = 0
    def devolverGravedad(self):
        self._particles[-1].gravity = 70


    def getPosClavija(self):
        return (self._particles[-1].x, self._particles[-1].y)
    def getPunto(self, i):
        return (self._particles[i].x, self._particles[i].y)