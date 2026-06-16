import pygame, os, random

pygame.font.init()

DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))

# --- CONFIGURACIÓN DE VENTANA ---
ANCHO_VENTANA = 1064
ALTO_COMBATE = 584
ALTO_PANEL = 120
ALTO_VENTANA = ALTO_COMBATE + ALTO_PANEL
FPS = 60 

DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_FUENTE = os.path.join(DIRECTORIO_BASE, "tipografia", "pokemon_font.ttf")

fuente_nombre = pygame.font.Font(RUTA_FUENTE, 18)
fuente_stats = pygame.font.Font(RUTA_FUENTE, 16)

# --- PALETA DE COLORES ---
COLOR_TEXTO = (60, 60, 60)
COLOR_BORDE = (60, 60, 60)
COLOR_PANEL = (245, 245, 245)
COLOR_FONDO_TOOLTIP = (30, 30, 30, 230)

# Botones: [Rect, Color]
DATOS_BOTONES = {
    "Atacar":    (pygame.Rect(600, ALTO_COMBATE + 15, 400, 40), (248, 112, 112)),
    "Objetos":  (pygame.Rect(600, ALTO_COMBATE + 65, 400, 40), (120, 200, 80)),
}

BOTONES_ATAQUE = {
    "Ataque1":    (pygame.Rect(600, ALTO_COMBATE + 15, 200, 40), (248, 112, 112)),
    "Ataque2":    (pygame.Rect(600, ALTO_COMBATE + 15, 400, 40), (248, 112, 112)),
    "Ataque3":    (pygame.Rect(600, ALTO_COMBATE + 65, 200, 40), (248, 112, 112)),
    "Ataque4":    (pygame.Rect(600, ALTO_COMBATE + 65, 400, 40), (248, 112, 112)),
}

DATOS_ESCENARIOS = {
    "fondo1.png": ((280, 470), (770, 320), 120),
    "fondo2.png": ((160, 370), (920, 285), 50),
    "fondo3.png": ((270, 470), (920, 287), 50)
}

escenario_actual = None

def obtener_fondo_aleatorio():
    global escenario_actual
    fondo_elegido = random.choice(list(DATOS_ESCENARIOS.keys()))
    escenario_actual = DATOS_ESCENARIOS[fondo_elegido]
    ruta = os.path.join(DIRECTORIO_BASE, "img", fondo_elegido)
    return pygame.transform.scale(pygame.image.load(ruta).convert(), (ANCHO_VENTANA, ALTO_COMBATE))


COLOR_FONDO = (0, 0, 20)
VELOCIDAD = 5
SCALA_PERSONAJE = 0.3
COOLDOWN_ANIMACION = 150
# --- COORDENADAS SPRITESHEET---
COORDENADAS_PABLO = {
    "abajo":     [(5, 4, 270, 380), (5, 392, 270, 380), (5, 782, 270, 380)],
    "arriba":    [(285, 4, 270, 380), (285, 392, 270, 380), (285, 782, 270, 380)],
    "izquierda": [(565, 4, 270, 380), (565, 392, 270, 380), (565, 782, 270, 380)]
}

# --- HITBOXES DEL MAPA LIBRE ---
LIMITES_MUNDO_LIBRE = {
    (160, 325, 250, 25), (410, 315, 30, 25), (440, 290, 240, 25),
    (655, 210, 25, 80), (690, 210, 290, 25), (980, 210, 25, 100),
    (1005, 285, 40, 25), (1040, 310, 25, 130), (890, 460, 150, 25),
    (890, 465, 25, 175), (805, 640, 85, 25), (780, 465, 25, 175),
    (705, 460, 100, 25), (705, 465, 25, 175), (612, 645, 95, 25),
    (430, 645, 20, 25), (405, 540, 25, 115), (185, 540, 220, 25),
    (100, 575, 95, 25), (75, 400, 25, 190), (100, 375, 30, 25),
    (130, 350, 30, 25)
}
