# estilo.py
import pygame, random, os
from personajes import personaje

# Iniciamos el sistema de fuentes
pygame.font.init()

# --- RESOLUCIÓN AUTOMÁTICA DE RUTAS ---
DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))

# Confugracuion general
ANCHO_VENTANA = 1064
ALTO_VENTANA = 704
ALTO_COMBATE = 584
ALTO_PANEL = ALTO_VENTANA - ALTO_COMBATE # Alto panel del combate
FPS = 60 


DATOS_ESCENARIOS = {
    "fondo1.png":   ((280, 470), (770, 320), 120),
    "fondo2.png": ((160, 370), (920, 285),50),
    "fondo3.png": ((270, 470), (920, 287), 50)
    
}

escenario_actual = None # Variable global para guardar el escenario

def obtener_fondo_aleatorio():
    global escenario_actual
    fondo_elegido = random.choice(list(DATOS_ESCENARIOS.keys()))
    escenario_actual = DATOS_ESCENARIOS[fondo_elegido]
    ruta_completa_fondo = os.path.join(DIRECTORIO_BASE, "img", fondo_elegido)
    return pygame.transform.scale(pygame.image.load(ruta_completa_fondo).convert(), (ANCHO_VENTANA, ALTO_COMBATE))

# Ruta para la tipografía
RUTA_FUENTE = os.path.join(DIRECTORIO_BASE, "tipografia", "pokemon_font.ttf")

# Cambiamos el tamaño de la fuente de los botones para que encaje perfectamente
fuente_nombre = pygame.font.Font(RUTA_FUENTE, 18) # Bajado de 22 a 18
fuente_stats = pygame.font.Font(RUTA_FUENTE, 16)

# Colores (Se mantienen igual)
COLOR_TEXTO = (60, 60, 60)
COLOR_BORDE = (60, 60, 60)
COLOR_PANEL = (240, 240, 240)
COLOR_FONDO_TOOLTIP = (40, 40, 40, 220)

COLOR_LUCHAR = (248, 112, 112)
COLOR_MOCHILA = (248, 168, 48)
COLOR_POKEMON = (120, 200, 80)
COLOR_HUIR = (112, 168, 248)

# Configuracion botonera: Alineada a la derecha del panel inferior
# El panel empieza en Y = 584 y mide 120 de alto.
DATOS_BOTONES = {
    "Atacar": (pygame.Rect(600, ALTO_COMBATE + 15, 200, 40), COLOR_LUCHAR),
    "Esquivar": (pygame.Rect(820, ALTO_COMBATE + 15, 200, 40), COLOR_MOCHILA),
    "Defenderse": (pygame.Rect(600, ALTO_COMBATE + 65, 200, 40), COLOR_POKEMON),
    "Huir": (pygame.Rect(820, ALTO_COMBATE + 65, 200, 40), COLOR_HUIR)
}

ALTO_PERSONAJE = 40  # Lo subí a 40 para que una skin se note mejor
ANCHO_PERSONAJE = 40 
COLOR_FONDO = (0, 0, 20)
VELOCIDAD = 5