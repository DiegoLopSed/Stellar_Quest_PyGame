import pygame
import random
import math
from utils import *
from settings import *

class Cometa:
    def __init__(self, direction):
        self.size = random.randint(60, 100)
        self.speed = random.uniform(10, 15)
        self.direction = direction
        self.warning_time = 60  # Frames de advertencia
        self.warning_shown = True

        # Establecer posición inicial basada en la dirección
        if direction == "right_to_left":
            self.x = WIDTH + self.size
            self.y = random.randint(0, HEIGHT)
        elif direction == "top_to_bottom":
            self.x = random.randint(0, WIDTH)
            self.y = -self.size
        elif direction == "diagonal":
            if random.choice([True, False]):
                self.x = WIDTH + self.size
                self.y = random.randint(0, HEIGHT)
            else:
                self.x = random.randint(0, WIDTH)
                self.y = -self.size
        
        # Establecer ángulo basado en la dirección
        if direction == "right_to_left":
            self.angle = math.pi  # 180 grados
        elif direction == "top_to_bottom":
            self.angle = math.pi / 2  # 90 grados
        elif direction == "diagonal":
            self.angle = math.pi * 3 / 4 if self.x > WIDTH else math.pi / 4

        # Sprite del cometa
        self.sprite = pygame.image.load(".venv/resources/images/cometa.png")
        self.sprite = pygame.transform.scale(self.sprite, (self.size, self.size))

    def update(self):
        if self.warning_time > 0:
            self.warning_time -= 1
        else:
            self.warning_shown = False
            self.x += math.cos(self.angle) * self.speed
            self.y += math.sin(self.angle) * self.speed

    def draw(self, surface):
        if self.warning_shown:
            # Dibujar advertencia
            if self.direction == "right_to_left":
                warning_pos = (WIDTH - 30, self.y)
            elif self.direction == "top_to_bottom":
                warning_pos = (self.x, 10)
            elif self.direction == "diagonal":
                warning_pos = (WIDTH - 30, 10) if self.x > WIDTH else (10, 10)
            font = pygame.font.Font(None, 90)
            warning_text = font.render("!", True, (255, 0, 0))
            surface.blit(warning_text, warning_pos)
        else:
            # Dibujar cometa
            rotated_sprite = pygame.transform.rotate(self.sprite, -math.degrees(self.angle))
            rect = rotated_sprite.get_rect(center=(self.x, self.y))
            surface.blit(rotated_sprite, rect)

def generar_cometas(cantidad):
    cometas = []
    for _ in range(cantidad):
        direction = random.choice(["right_to_left", "top_to_bottom", "diagonal"])
        cometas.append(Cometa(direction))
    return cometas

def actualizar_cometas(cometas, player_rect,settings):
    vidas_perdidas = 0
    for cometa in cometas:
        cometa.update()
        if cometa.warning_shown:
            continue
        cometa_rect = pygame.Rect(
            cometa.x - cometa.size / 2,
            cometa.y - cometa.size / 2,
            cometa.size,
            cometa.size
        )
        if cometa_rect.colliderect(player_rect):
            vidas_perdidas += 1
            # Reproducir sonido de impacto
            impacto_sound = pygame.mixer.Sound(".venv/resources/music/hit.wav")
            impacto_sound.set_volume(settings.volume)
            impacto_sound.play()


            cometas.remove(cometa)
            
        elif (cometa.x < -cometa.size or cometa.y > HEIGHT + cometa.size):
            cometas.remove(cometa)  # Eliminar cometas que salen de la pantalla
    return vidas_perdidas
