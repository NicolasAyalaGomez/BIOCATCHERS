from particle import Particle
from spring import Spring
import pygame
from math import sqrt
from random import randint

def distancia_euclidiana(x1, y1, x2, y2):
    distancia = sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distancia

class Cuerda:
    def __init__(self, colorCuerda, colorGancho, origenX, origenY):
        self.colorCuerda = colorCuerda
        self.colorGancho = colorGancho

        self.origenX = origenX
        self.origenY = origenY

        self._particles = []
        self._springs = []

        self.cuerdaEnganchada = False

        for i in range(14):
            if i==0:
                particle = Particle(origenX,origenY,            1,40,colorGancho)
            else:
                particle = Particle(origenX,origenY,     1,40,colorCuerda)
                
            if i > 0:
                spring = Spring(self._particles[i-1], particle, 50, 18)
                self._springs.append(spring)

            particle.vy = -380 + i*10
            if i>0:
                particle.vx = randint(-2, 2)
                
            self._particles.append(particle)

        self.flag = False
        self.escalando = False
        self.indiceParticula = -2


    # Calcular la interaccion entre el jugador y la cuerda
    def phisics(self, player, current_position, cPosAnt):
        for i in range(len(self._particles)):
            self._particles[i].mass = 1
        if(self.flag):
            if not self.escalando:
                if self.indiceParticula != 0:
                    self._particles[self.indiceParticula].vx = (current_position-cPosAnt)/0.1    
            else:
                player.rect.x = self._particles[self.indiceParticula].x-player.rect.width/2
                player.rect.y = self._particles[self.indiceParticula].y-player.rect.height/2+10

                self._particles[self.indiceParticula].mass = 3

                player.change_y=0
        
    # Se encarga de poder impulsarte hacia arriba cuando estas agarrado a la cuerda
    def subirCuerda(self, player):
        if self.flag:
            if self.escalando:
                self.escalando=False
                player.change_y=-7
                if self.indiceParticula != 0:
                    self._particles[self.indiceParticula].vy=200
                    self._particles[self.indiceParticula].vx=50
            else:
                self.escalando = True

    # Recorrer la cuerda completa hacia un lado para dar el efecto de seguimiento de camara
    def recorrerCuerda(self, diff):
        for i in range(len(self._particles)):
            particle = self._particles[i]
            particle.x+=diff

    # Aplicar la fuerza de los muelles y la gravedad a las particulas
    def move(self, screen, player):
        # verifica si el jugador esta lo suficientemente cerca para que convenga verificar si las demas particulas estan colisionando
        conviene = distancia_euclidiana(player.rect.x+player.rect.width/2, player.rect.y+player.rect.height/2, self._particles[6].x, self._particles[6].y)<220
        if(self._particles[0].vy>=0 and not self.cuerdaEnganchada):
            self.cuerdaEnganchada = True

            # Le aplica gravedad a todas las particulas, excepto a la primera (self._particles[0]) pues se queda enganchada 
            for particulas in self._particles:
                particulas.gravity = 80
            self._particles[0].gravity = 0
            self._particles[0].vy=0

        
        # Hace uso de la variable "Conviene" para saber si conviene verificar la colision con las demas particulas
        if conviene:
            for i in range(len(self._particles)):
                particle = self._particles[i]

                if(distancia_euclidiana(player.rect.x+player.rect.width/2, player.rect.y+player.rect.height/2, particle.x, particle.y)<30):
                    if not self.flag:
                        self.indiceParticula = i
                        
                    self.flag=True
                # Fisicas --------------------------------------------------------------------------------------------
                particle.apply_force(0, particle.mass * particle.gravity)
                particle.move(0.1)
        else:
            if(self._particles[0].x>-10 and self._particles[0].x<810):
                for par in self._particles:
                    par.apply_force(0, par.mass * par.gravity)
                    par.move(0.1)

            
            
        pygame.draw.rect(screen, self._particles[0].color, (self._particles[0].x - 15/2, self._particles[0].y - 10/2, 17, 15))

        if(self._particles[0].x>-20 and self._particles[0].x<810):
            for j in range(len(self._springs)):
                spring = self._springs[j]
                if self.cuerdaEnganchada:
                    if(j==0):
                        spring.apply_force(False)
                    else:
                        spring.apply_force(True)
                pygame.draw.line(screen, (124,72,0), (spring.p1.x,spring.p1.y), (spring.p2.x,spring.p2.y), 9)