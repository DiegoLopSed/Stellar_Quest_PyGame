import pygame
move_distance = 10  # Distancia de movimiento del jugador
# Función para dibujar la skin del jugador en la pantalla
def draw_player_skin(surface, skin_image, x, y, max_width=100, max_height=100):
    skin = pygame.image.load(skin_image)
    skin_rect = skin.get_rect()
    skin_ratio = skin_rect.width / skin_rect.height
    if skin_rect.width > skin_rect.height:
        new_width = min(skin_rect.width, max_width)
        new_height = new_width / skin_ratio
    else:
        new_height = min(skin_rect.height, max_height)
        new_width = new_height * skin_ratio

    skin = pygame.transform.scale(skin, (int(new_width), int(new_height)))
    surface.blit(skin, (x, y))

# Función para mover al jugador con límites de pantalla
def move_player(keys, player_x, player_y, move_distance):
    # Obtener dimensiones de la pantalla
    screen_width, screen_height = pygame.display.get_surface().get_size()
    
    # Calcular el tamaño del jugador (asumiendo 40x40 píxeles)
    player_size = 40
    
    # Mover solo si no se sale de los límites
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= move_distance
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_size:
        player_x += move_distance
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= move_distance
    if keys[pygame.K_DOWN] and player_y < screen_height - player_size:
        player_y += move_distance

    return player_x, player_y

# Instrucciones visuales para el jugador
def show_movement_instructions(surface, current_theme, font, screen_width, screen_height):
    # Mostrar instrucciones de control
    draw_text(surface, "Usa las flechas para mover", font, current_theme["text"], screen_width // 2, screen_height // 3, center=True)

# Función de texto
def draw_text(surface, text, font, color, x, y, center=False):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)
