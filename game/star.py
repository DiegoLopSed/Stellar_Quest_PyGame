import random
import pygame
WIDTH, HEIGHT = 1000, 700

# Clase para la estrella
class Star:
    def __init__(self):
        # Posiciones iniciales aleatorias
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        # Velocidad en la dirección X y Y
        self.speed_x = random.uniform(-1.5, 1.5)
        self.speed_y = random.uniform(1.0, 2.0)
        # Tamaño de la estrella
        self.size = 30  # Tamaño fijo más grande para las estrellas recolectables
        # Cargar sprite de la estrella
        self.sprite = pygame.image.load(".venv/resources/images/star.png")
        self.sprite = pygame.transform.scale(self.sprite, (self.size, self.size))

    def update(self):
        # Movimiento errático en las dos direcciones
        self.x += self.speed_x
        self.y += self.speed_y

        # Cuando la estrella sale de los límites de la pantalla, vuelve a aparecer en una posición aleatoria
        if self.x < 0 or self.x > WIDTH:
            self.x = random.randint(0, WIDTH)
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randint(0, WIDTH)

    def draw(self, surface):
        # Dibujar el sprite de la estrella en lugar del círculo
        surface.blit(self.sprite, (int(self.x - self.size/2), int(self.y - self.size/2)))
# Función para generar una nueva estrella
def generate_star():
    return Star()

# Función para generar una estrella grande
def generate_big_star():
    big_star = Star()
    big_star.size = random.randint(20, 50)  # Tamaño más grande
    big_star.speed_x = random.uniform(-5.0, 5.0)  # Movimiento más rápido
    big_star.speed_y = random.uniform(2.5, 4.5)
    return big_star

# Función para actualizar y dibujar la estrella en el tutorial
def update_star_and_check_collision(WIN, player_x, player_y, collected_stars, total_stars):
    # Generar una estrella normal o grande aleatoriamente

    star = generate_big_star()

    star.update()
    star.draw(WIN)

    # Crear el rectángulo del jugador para verificar colisión con la estrella
    player_rect = pygame.Rect(player_x, player_y, 40, 40)
    star_rect = pygame.Rect(star.x - star.size, star.y - star.size, star.size * 2, star.size * 2)

    if player_rect.colliderect(star_rect):  # Si el jugador colisiona con la estrella
        collected_stars += 1
        star = generate_big_star()
        


    return star, collected_stars

