import pygame
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
