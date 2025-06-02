import pygame
import sys
import json
import settings
from utils import *
from player import *
from star import *
from asteroids import *
from cometa import *

def load_settings_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def start_level(WIN):
    clock = pygame.time.Clock()
    running = True
    keys_pressed = {pygame.K_LEFT: False, pygame.K_RIGHT: False, pygame.K_UP: False, pygame.K_DOWN: False}
    player_x, player_y = settings.WIDTH // 2, settings.HEIGHT // 2 + 100
    move_distance = 10

    # Cargar configuración desde JSON
    config = load_settings_from_json('.venv/resources/config.json')

    if config["theme"] == "dark":
        settings.current_theme = settings.DARK_THEME
    elif config["theme"] == "blue":
        settings.current_theme = settings.BLUE_THEME
    else:
        settings.current_theme = settings.DARK_THEME

    settings.player_skin = config.get("skin", "default_skin.png")

    # Inicializar estrella
    current_star = generate_star()
    collected_stars = 0
    total_stars = 3

    # Inicializar asteroides
    asteroides = generar_asteroides(2)
    vidas = 3
    max_asteroides = 2
    tiempo_ultimo_asteroide = pygame.time.get_ticks()
    intervalo_asteroides = 7000

    # Inicializar cometas
    cometas = generar_cometas(1)
    max_cometas = 2
    tiempo_ultimo_cometa = pygame.time.get_ticks()
    intervalo_cometas = 10000

    # Música del nivel
    pygame.mixer.music.stop()
    pygame.mixer.music.load(".venv/resources/music/lvl_1.mp3")
    pygame.mixer.music.play(-1)

    while running:
        WIN.fill(settings.current_theme["bg"])
        player_rect = pygame.Rect(player_x, player_y, 40, 40)

        current_star.update()
        current_star.draw(WIN)
        draw_text(WIN, f"{collected_stars}/{total_stars} estrellas recolectadas", pygame.font.Font(None, 36), settings.current_theme["text"], 20, 20)

        vidas -= actualizar_asteroides(asteroides, player_rect, settings)
        for ast in asteroides:
            ast.draw(WIN)

        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - tiempo_ultimo_asteroide > intervalo_asteroides and len(asteroides) < max_asteroides:
            asteroides.extend(generar_asteroides(1))
            tiempo_ultimo_asteroide = tiempo_actual

        vidas -= actualizar_cometas(cometas, player_rect, settings)
        for cometa in cometas:
            cometa.draw(WIN)

        if tiempo_actual - tiempo_ultimo_cometa > intervalo_cometas and len(cometas) < max_cometas:
            cometas.extend(generar_cometas(1))
            tiempo_ultimo_cometa = tiempo_actual

        draw_text(WIN, f"Vidas: {vidas}", pygame.font.Font(None, 36), (255, 100, 100), settings.WIDTH // 2, 20, center=True)

        if vidas <= 0:
            draw_text(WIN, "¡Perdiste todas tus vidas!", pygame.font.Font(None, 48), (255, 0, 0), settings.WIDTH // 2, settings.HEIGHT // 2, center=True)
            pygame.display.flip()
            pygame.time.delay(2000)
            pygame.mixer.music.stop()
            pygame.mixer.music.load(".venv/resources/music/space_theme.mp3")
            pygame.mixer.music.play()
            return "nivel perdido"

        draw_player_skin(WIN, settings.player_skin, player_x, player_y)
        draw_text(WIN, "Presiona ESC para salir", pygame.font.Font(None, 36), settings.current_theme["text"], settings.WIDTH // 2, settings.HEIGHT - 40, center=True)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in keys_pressed:
                    keys_pressed[event.key] = True
                elif event.key == pygame.K_ESCAPE:
                    return "salir"
            elif event.type == pygame.KEYUP:
                if event.key in keys_pressed:
                    keys_pressed[event.key] = False

        player_x, player_y = move_player(keys_pressed, player_x, player_y, move_distance)

        if player_rect.colliderect(pygame.Rect(current_star.x - current_star.size, current_star.y - current_star.size, current_star.size * 2, current_star.size * 2)):
            collected_stars += 1
            current_star = generate_star()
            if collected_stars >= total_stars:
                draw_text(WIN, "¡Constelación completa! Casiopea", pygame.font.Font(None, 48), (255, 255, 0), settings.WIDTH // 2, settings.HEIGHT // 2, center=True)
                pygame.display.flip()
                pygame.time.delay(2000)
                pygame.mixer.music.stop()
                pygame.mixer.music.load(".venv/resources/music/space_theme.mp3")
                pygame.mixer.music.play()
                return "nivel completado"

        clock.tick(30)
