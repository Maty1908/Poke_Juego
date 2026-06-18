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
    ruta = os.path.join(DIRECTORIO_BASE, "img","Fondo_peleas",fondo_elegido)
    return pygame.transform.scale(pygame.image.load(ruta).convert(), (ANCHO_VENTANA, ALTO_COMBATE))


VELOCIDAD_TIENDA = 5
VELOCIDAD_MUNDO_LIBRE = 3
COOLDOWN_ANIMACION = 150

# --- COORDENADAS SPRITESHEET---

#estos conjuntos significan (x,y,ancho,alto)

COORDENADAS = {
    "abajo":     [(5, 4, 270, 380), (5, 392, 270, 380), (5, 782, 270, 380)],
    "arriba":    [(285, 4, 270, 380), (285, 392, 270, 380), (285, 782, 270, 380)],
    "izquierda": [(565, 4, 270, 380), (565, 392, 270, 380), (565, 782, 270, 380)]
}

# --- HITBOXES DE TIENDA---
LIMITES_TIENDA = {
    (160, 325, 250, 25), (410, 315, 30, 25), (440, 290, 240, 25),
    (655, 210, 25, 80), (690, 210, 290, 25), (980, 210, 25, 100),
    (1005, 285, 40, 25), (1040, 310, 25, 130), (890, 460, 150, 25),
    (890, 465, 25, 175), (805, 640, 85, 25), (780, 465, 25, 175),
    (705, 460, 100, 25), (705, 465, 25, 175), (612, 645, 95, 25),
    (430, 645, 20, 25), (405, 540, 25, 115), (185, 540, 220, 25),
    (100, 575, 95, 25), (75, 400, 25, 190), (100, 375, 30, 25),
    (130, 350, 30, 25)
}

LIMITES_MUNDO_LIBRE = {
    (1, 470, 278, 117), (170, 545, 145, 65), (245, 565, 95, 15), (20, 605, 55, 5),
    (350, 585, 108, 1), (325, 485, 15, 30), (479, 590, 3, 1), (589, 590, 3, 1),  (510, 400, 50, 75),
    (465, 425, 134, 28), (488,  410, 93, 55), (610, 585, 108, 1), (725, 575, 95, 125), (730, 485, 15, 30), 
    (765, 480, 55, 95), (825, 495, 35, 50), (860, 525, 30, 1), (818, 620, 246, 84), (927, 578, 137, 84), 
    (960, 550, 104, 30), (970, 485, 94, 80), (1040, 415, 24, 80), (955, 370, 109, 45), (845, 370, 214, 15),
    (760, 290, 304, 80), (760, 370, 85, 25), (738, 390, 3, 1), (728, 290, 25, 1), (927, 215, 137, 75),
    (805, 141, 254, 74), (470, 1, 594, 140), (640, 141, 75, 35), (470, 141, 112, 142), (582, 238, 23, 45), 
    (627, 287, 3, 1), (440, 287, 3, 1), (415, 250, 55, 30), (440, 230, 30, 20), (1, 1, 130, 190), 
    (131, 1, 75, 140), (205, 1, 90, 190), (295, 1, 35, 150), (325, 1, 60, 115),  (1, 305, 245, 55), 
    (58, 378, 3, 1), (206, 370, 3, 1), (330, 370, 3, 1), (25, 275, 3, 1), (450, 150, 3, 1), (430, 75, 3, 1),  
}

#                 x , y, ancho, alto
NPC_MUNDO_LIBRE ={(169,192,25,30),(730,175,25,30),(894,480,25,30)}   #npc muelle, cueva y bosque
ENTRADA_TIENDA = {(117,613,25,30)}
SALIDA_TIENDA = {(530,668,25,30)}