import pygame
import sys
import importlib
from utils import draw_text
from star import *
import settings


def level_selection_screen(WIN):
    pygame.init()

    # Datos de los niveles
    levels = [
        {"name": "", "image": ".venv/resources/images/osa_mayor.png", "module": "osa_mayor"},
        {"name": "", "image": ".venv/resources/images/orion.png", "module": "orion"},
        {"name": "", "image": ".venv/resources/images/cassiopeia.png", "module": "casiopea"}
    ]

    selected_level = 0
    clock = pygame.time.Clock()
    running = True
    highlight_color = settings.current_theme.get("highlight", (255, 255, 0))  # Amarillo por defecto

    while running:
        WIN.fill(settings.current_theme["bg"])

        # Dibujar nivel seleccionado
        for idx, level in enumerate(levels):
            # Posiciones horizontales y verticales
            x = settings.WIDTH // 4 + idx * 250  # Separar niveles horizontalmente
            y = settings.HEIGHT // 2

            # Dibujar contorno si es el nivel seleccionado
            if idx == selected_level:
                pygame.draw.rect(WIN, highlight_color,
                                 (x - 100, y - 100, 200, 200), 4)  # Ajustar tamaño del contorno

            # Dibujar imagen del nivel
            constel_image = pygame.image.load(level["image"])
            constel_image = pygame.transform.scale(constel_image, (200, 200))  # Escalar imagen
            WIN.blit(constel_image, (x - 75, y - 75))

            # Dibujar nombre del nivel
            draw_text(WIN, level["name"], pygame.font.Font(None, 36),
                      settings.current_theme["text"], x, y + 100, center=True)

        # Instrucción al jugador
        draw_text(WIN, "Usa las flechas para desplazarte y ENTER para seleccionar",
                  pygame.font.Font(None, 36), settings.current_theme["text"],
                  settings.WIDTH // 2, settings.HEIGHT - 50, center=True)

        # Leyenda de salir con ESC
        draw_text(WIN, "Presiona ESC para salir", pygame.font.Font(None, 24),
                  settings.current_theme["text"], settings.WIDTH // 2, settings.HEIGHT - 20, center=True)

        pygame.display.flip()

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # Mover selección a la izquierda
                    selected_level = (selected_level - 1) % len(levels)
                elif event.key == pygame.K_RIGHT:  # Mover selección a la derecha
                    selected_level = (selected_level + 1) % len(levels)
                elif event.key == pygame.K_RETURN:  # Seleccionar nivel
                    running = False
                    # Cargar y ejecutar el nivel seleccionado
                    try:
                        level_module = importlib.import_module(levels[selected_level]["module"])
                        level_module.start_level(WIN)
                    except ImportError as e:
                        print(f"Error al cargar el nivel: {e}")
                    except AttributeError:
                        print("El nivel seleccionado no tiene la función 'start_level'.")
                elif event.key == pygame.K_ESCAPE:  # Salir de la pantalla actual
                    
                    running = False
                    return None  # Indica que no se seleccionó ningún nivel

        clock.tick(30)
