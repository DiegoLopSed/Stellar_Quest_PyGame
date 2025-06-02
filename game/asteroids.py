import pygame
import random
import math
from utils import *

class Asteroide:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(40, 80)  # Tamaño más grande
        self.speed = random.uniform(3, 8)  # Velocidad más rápida
        self.angle = random.uniform(0, 2 * math.pi)  # Dirección aleatoria inicial
        self.rotation = random.uniform(-3, 3)  # Rotación aleatoria
        self.rotation_angle = 0
        self.sprite = pygame.image.load(".venv/resources/images/asteroid.png")
        self.sprite = pygame.transform.scale(self.sprite, (self.size, self.size))

    def update(self):
        # Cambios aleatorios en la dirección para movimiento errático
        self.angle += random.uniform(-0.1, 0.1)
        
        # Movimiento basado en ángulo y velocidad
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.rotation_angle += self.rotation

        # Reaparecer en el otro lado si sale de la pantalla
        if self.x < -self.size:
            self.x = WIDTH + self.size
        elif self.x > WIDTH + self.size:
            self.x = -self.size
        if self.y < -self.size:
            self.y = HEIGHT + self.size
        elif self.y > HEIGHT + self.size:
            self.y = -self.size

    def draw(self, surface):
        # Rotar y dibujar el sprite
        rotated_sprite = pygame.transform.rotate(self.sprite, self.rotation_angle)
        rect = rotated_sprite.get_rect(center=(self.x, self.y))
        surface.blit(rotated_sprite, rect)

    def check_collision(self, player_rect):
        # Crear rectángulo del asteroide
        asteroid_rect = pygame.Rect(
            self.x - self.size/2,
            self.y - self.size/2,
            self.size,
            self.size
        )
        return asteroid_rect.colliderect(player_rect)

def generar_asteroides(cantidad):
    asteroides = []
    for _ in range(cantidad):
        # Generar posición aleatoria
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        asteroides.append(Asteroide(x, y))
    return asteroides

def actualizar_asteroides(asteroides, player_rect, settings):
    vidas_perdidas = 0
    for asteroide in asteroides:
        asteroide.update()
        if asteroide.check_collision(player_rect):
            impacto_sound = pygame.mixer.Sound(".venv/resources/music/hit.wav")
            impacto_sound.set_volume(settings.volume)
            impacto_sound.play()

            vidas_perdidas += 1
            # Reposicionar el asteroide después de la colisión
            asteroide.x = random.randint(0, WIDTH)
            asteroide.y = random.randint(0, HEIGHT)
    return vidas_perdidas
