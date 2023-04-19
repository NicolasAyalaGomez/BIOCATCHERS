import pygame

class Particle:
    def __init__(self, x, y, mass, grav, color, tiempoDeVida=-1):
        self.x = x
        self.y = y
        self.mass = mass
        self.vx = 0 
        self.vy = 0
        self.ax = 0
        self.ay = 0
        self.resistance = 0.5
        self.gravity = grav
        self.color = color

        self.tiempoDeVida = tiempoDeVida
        self.nacimiento = pygame.time.get_ticks()
    
    # Recibe dos parametros (Fuerza en x y Fuerza en y) y las añade a la particula
    def apply_force(self, fx, fy):
        self.ax += (fx / self.mass)
        self.ay += (fy / self.mass)
        
    # Aplica el cambio de posicion en abse a la velocidad y aceleracion de la particula
    def move(self, dt):
        # Aplcia resistencia para generar un movimiento mas natural
        self.ax -= self.vx * self.resistance
        self.ay -= self.vy * self.resistance
        self.vx += self.ax * dt
        self.vy += self.ay * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.ax = 0
        self.ay = 0

    def __str__(self):
        return f"Particle(x={self.x}, y={self.y}, mass={self.mass}, vx={self.vx}, vy={self.vy}, ax={self.ax}, ay={self.ay}, resistance={self.resistance}, gravity={self.gravity})"