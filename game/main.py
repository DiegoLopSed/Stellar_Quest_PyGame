import pygame
import sys
import settings  
from player import *
from instructions import *
from star import Star
from utils import draw_text
from game import *

# Inicializar pygame
pygame.init()
pygame.mixer.init()

stars = [Star() for _ in range(50)]

# Configuración de pantalla
WIDTH, HEIGHT = 1000, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stellar Quest")

# Cargar configuración al iniciar
settings.load_config()

# Configurar volumen de música de fondo
pygame.mixer.music.stop()
pygame.mixer.music.load(".venv/resources/music/space_theme.mp3")
pygame.mixer.music.set_volume(settings.volume)
pygame.mixer.music.play(-1, 0.0)  # Reproducir en bucle infinito

# Crear estrellas


def main_menu():
    

    clock = pygame.time.Clock()
    running = True

    while running:
        WIN.fill(settings.current_theme["bg"])

        # Dibujar estrellas animadas
        for star in stars:
            star.update()
            star.draw(WIN)

        # Título del juego
        draw_text(WIN, "Stellar Quest", pygame.font.Font(None, 74), settings.current_theme["text"], WIDTH // 2, HEIGHT // 4, center=True)

        # Opciones del menú
        draw_text(WIN, "1. Iniciar Juego", pygame.font.Font(None, 48), settings.current_theme["text"], WIDTH // 2, HEIGHT // 2 - 40, center=True)
        draw_text(WIN, "2. Instrucciones", pygame.font.Font(None, 48), settings.current_theme["text"], WIDTH // 2, HEIGHT // 2, center=True)
        draw_text(WIN, "3. Configuración", pygame.font.Font(None, 48), settings.current_theme["text"], WIDTH // 2, HEIGHT // 2 + 40, center=True)
        draw_text(WIN, "4. Salir", pygame.font.Font(None, 48), settings.current_theme["text"], WIDTH // 2, HEIGHT // 2 + 80, center=True)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    level_selection_screen(WIN)  # Llamar a la pantalla de selección de nivel
                    
                elif event.key == pygame.K_2:
                    instructions_screen(WIN)  
                elif event.key == pygame.K_3:
                    settings.settings_screen(WIN)  
                    settings.load_config()
                    pygame.mixer.music.set_volume(settings.volume)  # Actualizar volumen de la música
                elif event.key == pygame.K_4:
                    pygame.quit()
                    sys.exit()

        clock.tick(30)

# Ejecutar pantalla de inicio
main_menu()     

# Detener música al salir
pygame.mixer.music.stop()
