import pygame
import sys
import json
from utils import draw_text
from player import draw_player_skin

# Inicializar Pygame
pygame.init()

# Variables globales
WIDTH, HEIGHT = 1000, 700
MENU_FONT = pygame.font.Font(None, 48)  # Fuente para el menú

# Definición de temas
BLUE_THEME = {
    "bg": (10, 10, 50),
    "text": (143, 227, 220)
}
DARK_THEME = {
    "bg": (0, 0, 0),
    "text": (5, 247, 228)
}

skins = [".venv/resources/images/nave1.png", ".venv/resources/images/nave2.png",
         ".venv/resources/images/nave3.png", ".venv/resources/images/nave4.png"]

# Variables de configuración inicial
volume = 0.5
current_theme = DARK_THEME
player_skin = "nave1.png"

# Función para cargar la configuración
def load_config():
    global current_theme, player_skin, volume
    try:
        with open( ".venv/resources/config.json", "r") as f:
            config = json.load(f)
            theme_name = config.get("theme", "dark")  # Default "dark" si no existe
            if theme_name == "blue":
                current_theme = BLUE_THEME
            else:
                current_theme = DARK_THEME
            player_skin = config.get("skin", "nave1.png")  # Default skin
            volume = config.get("volume", 0.5)  # Default volume
            pygame.mixer.music.set_volume(volume)  # Aplicar volumen
    except FileNotFoundError:
        print("Archivo de configuración no encontrado. Usando valores predeterminados.")

# Función para guardar la configuración
def save_config():
    config = {
        "theme": "blue" if current_theme == BLUE_THEME else "dark",
        "skin": player_skin,
        "volume": volume
    }
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)  # indentado para legibilidad

# Cargar configuración al iniciar
load_config()

def settings_screen(WIN):
    global current_theme, player_skin, volume  # Usar las globales
    clock = pygame.time.Clock()
    running = True

    while running:
        WIN.fill(current_theme["bg"])

        # Títulos
        draw_text(WIN, "Configuración", MENU_FONT, current_theme["text"], WIDTH // 2, 50, center=True)

        # Volumen
        draw_text(WIN, f"Volumen: {int(volume * 100)}%", MENU_FONT, current_theme["text"], WIDTH // 2, 150, center=True)
        draw_text(WIN, "- Disminuir", MENU_FONT, current_theme["text"], WIDTH // 2 - 150, 200, center=True)
        draw_text(WIN, "Aumentar +", MENU_FONT, current_theme["text"], WIDTH // 2 + 150, 200, center=True)

        # Temas
        draw_text(WIN, "Tema de Color:", MENU_FONT, current_theme["text"], WIDTH // 2, 300, center=True)
        draw_text(WIN, "1. Azul", MENU_FONT, current_theme["text"], WIDTH // 2, 350, center=True)
        draw_text(WIN, "2. Oscuro", MENU_FONT, current_theme["text"], WIDTH // 2, 400, center=True)

        # Skins
        draw_text(WIN, "Skin del Jugador", MENU_FONT, current_theme["text"], WIDTH // 2 + 350, 500, center=True)
        draw_player_skin(WIN, player_skin, WIDTH // 2 + 300, 550)
        draw_text(WIN, "3. Cambiar Skin", MENU_FONT, current_theme["text"], WIDTH // 2, 550, center=True)

        # Opción de salir
        draw_text(WIN, "Presiona ESC para volver", MENU_FONT, current_theme["text"], WIDTH // 2, HEIGHT - 50, center=True)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    save_config()
                    running = False

                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    volume = max(0.0, volume - 0.1)
                    pygame.mixer.music.set_volume(volume)

                elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS or event.key == pygame.K_EQUALS:
                    volume = min(1.0, volume + 0.1)
                    pygame.mixer.music.set_volume(volume)

                elif event.key == pygame.K_1:
                    current_theme = BLUE_THEME

                elif event.key == pygame.K_2:
                    current_theme = DARK_THEME

                elif event.key == pygame.K_3:
                    current_skin_index = skins.index(player_skin)
                    player_skin = skins[(current_skin_index + 1) % len(skins)]

        clock.tick(30)
