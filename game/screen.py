import pygame
import sys
import random

# Inicializar pygame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 1000, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stellar Quest")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 223, 0)
DARK_BLUE = (10, 10, 50)  # Azul oscuro para tema espacial
LIGHT_BLUE = (143, 227, 220)  # Azul más claro para texto en el tema azul

# Temas de Color
DARK_THEME = {"bg": BLACK, "text": YELLOW}  # Fondo negro con texto amarillo (estilo clásico espacial)
BLUE_THEME = {"bg": DARK_BLUE, "text": LIGHT_BLUE}  # Fondo azul oscuro con texto azul claro

# Fuentes
TITLE_FONT = pygame.font.Font(None, 74)
MENU_FONT = pygame.font.Font(None, 48)

# Música de fondo
try:
    pygame.mixer.music.load("space_theme.mp3")
    pygame.mixer.music.play(-1)
except pygame.error:
    print("No se pudo cargar la música de fondo.")

volume = 0.5
pygame.mixer.music.set_volume(volume)
current_theme = DARK_THEME

# Variables para la skin del jugador
player_skin = "nave1.png"  # Por defecto se usa la skin 1
skins = ["nave1.png","nave2.png", "nave3.png", "nave4.png"]  # Lista de skins disponibles

# Variables para el movimiento del jugador
player_x, player_y = WIDTH // 2, HEIGHT // 2  # Posición inicial
player_speed = 5  # Velocidad normal
sprint_distance = 20  # Distancia de sprint
sprint_active = False  # Estado del sprint

# Clase para animar estrellas en el fondo
class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed = random.uniform(0.5, 2.0)
        self.size = random.randint(1, 3)

    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randint(0, WIDTH)

    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (self.x, int(self.y)), self.size)

# Crear estrellas
stars = [Star() for _ in range(100)]

# Función para dibujar texto
def draw_text(surface, text, font, color, x, y, center=False):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# Función para dibujar la skin del jugador con redimensionamiento para mantener la proporción
def draw_player_skin(surface, skin_image, x, y, max_width=100, max_height=100):
    skin = pygame.image.load(skin_image)
    skin_rect = skin.get_rect()

    # Mantener la proporción de la imagen y ajustarla al tamaño máximo permitido
    skin_ratio = skin_rect.width / skin_rect.height
    if skin_rect.width > skin_rect.height:
        new_width = min(skin_rect.width, max_width)
        new_height = new_width / skin_ratio
    else:
        new_height = min(skin_rect.height, max_height)
        new_width = new_height * skin_ratio

    skin = pygame.transform.scale(skin, (int(new_width), int(new_height)))
    surface.blit(skin, (x, y))

# Función para manejar el movimiento del jugador
def move_player(keys):
    global player_x, player_y
    if keys[pygame.K_LEFT]:
        player_x -= sprint_distance if sprint_active else player_speed
    if keys[pygame.K_RIGHT]:
        player_x += sprint_distance if sprint_active else player_speed
    if keys[pygame.K_UP]:
        player_y -= sprint_distance if sprint_active else player_speed
    if keys[pygame.K_DOWN]:
        player_y += sprint_distance if sprint_active else player_speed

# Pantalla de configuración
def settings_screen():
    global volume, current_theme, player_skin
    clock = pygame.time.Clock()
    running = True

    while running:
        WIN.fill(current_theme["bg"])

        # Texto del título
        draw_text(WIN, "Configuración", MENU_FONT, current_theme["text"], WIDTH // 2, 50, center=True)

        # Controles de volumen
        draw_text(WIN, f"Volumen: {int(volume * 100)}%", MENU_FONT, current_theme["text"], WIDTH // 2, 150, center=True)
        draw_text(WIN, "- Disminuir", MENU_FONT, current_theme["text"], WIDTH // 2 - 150, 200, center=True)
        draw_text(WIN, "Aumentar +", MENU_FONT, current_theme["text"], WIDTH // 2 + 150, 200, center=True)

        # Opciones de tema
        draw_text(WIN, "Tema de Color:", MENU_FONT, current_theme["text"], WIDTH // 2, 300, center=True)
        draw_text(WIN, "1. Azul", MENU_FONT, current_theme["text"], WIDTH // 2, 350, center=True)
        draw_text(WIN, "2. Oscuro", MENU_FONT, current_theme["text"], WIDTH // 2, 400, center=True)

        # Mover la etiqueta y la skin más a la derecha
        draw_text(WIN, "Skin del Jugador", MENU_FONT, current_theme["text"], WIDTH // 2 + 350, 500, center=True)
        draw_player_skin(WIN, player_skin, WIDTH // 2 + 300, 550)  # Mover la imagen más a la derecha

        # Opciones para cambiar la skin
        draw_text(WIN, "3. Cambiar Skin", MENU_FONT, current_theme["text"], WIDTH // 2, 550, center=True)
        draw_text(WIN, "Presiona ESC para volver", MENU_FONT, current_theme["text"], WIDTH // 2, HEIGHT - 50, center=True)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False  # Salir de configuración
                elif event.key == pygame.K_MINUS:
                    volume = max(0.0, volume - 0.1)
                    pygame.mixer.music.set_volume(volume)
                elif event.key == pygame.K_PLUS:
                    volume = min(1.0, volume + 0.1)
                    pygame.mixer.music.set_volume(volume)
                elif event.key == pygame.K_1:
                    current_theme = BLUE_THEME
                elif event.key == pygame.K_2:
                    current_theme = DARK_THEME
                elif event.key == pygame.K_3:
                    # Cambiar entre skins
                    current_skin_index = skins.index(player_skin)
                    new_skin_index = (current_skin_index + 1) % len(skins)
                    player_skin = skins[new_skin_index]  # Cambiar a la siguiente skin

        clock.tick(30)

def instructions_screen():
    clock = pygame.time.Clock()
    running = True
    keys_pressed = {'left': False, 'right': False, 'up': False, 'down': False}
    instruction_step = 1  # 1: Flechas, 2: Sprint

    while running:
        WIN.fill(current_theme["bg"])

        # Mostrar instrucciones según el estado
        if instruction_step == 1:
            draw_text(WIN, "Usa las flechas de desplazamiento", MENU_FONT, current_theme["text"], WIDTH // 2, HEIGHT // 3, center=True)
        elif instruction_step == 2:
            draw_text(WIN, "Usa el espacio para el sprint", MENU_FONT, current_theme["text"], WIDTH // 2, HEIGHT // 3, center=True)

        # Verificar si se han presionado todas las teclas de dirección
        if not any(keys_pressed.values()):  # Si ninguna tecla está presionada, avanzar a siguiente mensaje
            draw_text(WIN, "Presiona las flechas", MENU_FONT, current_theme["text"], WIDTH // 2, HEIGHT // 2, center=True)
        else:
            # Comprobar si se presionaron todas las flechas
            if all(keys_pressed.values()):
                instruction_step = 2  # Cambiar al paso 2

        draw_text(WIN, "Presiona ESC para volver al menú", MENU_FONT, current_theme["text"], WIDTH // 2, HEIGHT - 50, center=True)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Marcar que se ha presionado una tecla de dirección
                if event.key == pygame.K_LEFT:
                    keys_pressed['left'] = True
                elif event.key == pygame.K_RIGHT:
                    keys_pressed['right'] = True
                elif event.key == pygame.K_UP:
                    keys_pressed['up'] = True
                elif event.key == pygame.K_DOWN:
                    keys_pressed['down'] = True
                elif event.key == pygame.K_ESCAPE:
                    running = False  # Salir a la pantalla de menú

        clock.tick(30)

# Pantalla principal
def main_menu():
    clock = pygame.time.Clock()
    running = True

    while running:
        WIN.fill(current_theme["bg"])

        # Dibujar estrellas animadas
        for star in stars:
            star.update()
            star.draw(WIN)

        # Título del juego
        draw_text(WIN, "Stellar Quest", TITLE_FONT, current_theme["text"], WIDTH // 2, HEIGHT // 4, center=True)

        # Opciones de menú
        draw_text(WIN, "1. Iniciar Juego", MENU_FONT, current_theme["text"], WIDTH // 2, HEIGHT // 2 - 40, center=True)
        draw_text(WIN, "2. Instrucciones", MENU_FONT, current_theme["text"], WIDTH // 2, HEIGHT // 2, center=True)
        draw_text(WIN, "3. Configuración", MENU_FONT, current_theme["text"], WIDTH // 2, HEIGHT // 2 + 40, center=True)
        draw_text(WIN, "4. Salir", MENU_FONT, current_theme["text"], WIDTH // 2, HEIGHT // 2 + 80, center=True)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    print("Iniciar Juego")
                    running = False
                elif event.key == pygame.K_2:
                    instructions_screen()
                elif event.key == pygame.K_3:
                    settings_screen()  # Abrir configuración
                elif event.key == pygame.K_4:
                    pygame.quit()
                    sys.exit()

        clock.tick(30)

# Ejecutar pantalla de inicio
main_menu()
