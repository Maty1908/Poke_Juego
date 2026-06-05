import io
import sys
import pygame
import random
import requests 
from PIL import Image, ImageSequence

# ==========================================
# PARTE 1: CONSULTA API Y DESCARGA (Antes de Pygame)
# ==========================================

pokemon_usuario =  random.randint(1, 20) #"pikachu" #input("Ingrese pokemon a usar: ").strip().lower()   
print(f"Buscando al pokemon en la PokeAPI...")

# --- Mio ---
url_mio = f"https://pokeapi.co/api/v2/pokemon/{pokemon_usuario}"
respuesta_mio = requests.get(url_mio)
if respuesta_mio.status_code == 404:
    raise ValueError(f"¡El Pokémon '{pokemon_usuario}' no existe! Revisá si lo escribiste bien.")
    
datos_mio = respuesta_mio.json()
url_gif_mio = datos_mio["sprites"]["versions"]["generation-v"]["black-white"]["animated"]["back_default"]

# --- Rival ---
pokemon_rival = random.randint(1, 150)
url_rival = f"https://pokeapi.co/api/v2/pokemon/{pokemon_rival}"
datos_rival = requests.get(url_rival).json()
url_gif_rival = datos_rival["sprites"]["versions"]["generation-v"]["black-white"]["animated"]["front_default"]

if not url_gif_mio or not url_gif_rival:
    raise ValueError("Este Pokémon no tiene una animación oficial de espalda en esta generación. Probá con otro (ej: pikachu, charizard, lucario).")

print("Descargando fotogramas animados...")

# Descargar gifs a memoria RAM
bits_gif_mio = requests.get(url_gif_mio).content
gif_mio_memoria = io.BytesIO(bits_gif_mio)

bits_gif_rival = requests.get(url_gif_rival).content
gif_rival_memoria = io.BytesIO(bits_gif_rival)

# Abrir con Pillow
gif_mio_pil = Image.open(gif_mio_memoria)
gif_rival_pil = Image.open(gif_rival_memoria)

# ==========================================
# PARTE 2: INICIALIZACIÓN Y CONFIGURACIÓN DE PYGAME
# ==========================================

pygame.init()

ancho_ventana = 1064
alto_ventana = 582
ventana = pygame.display.set_mode((ancho_ventana, alto_ventana))
pygame.display.set_caption("Simulador de Combate Pokémon")

reloj = pygame.time.Clock()

ancho_pokemon = 200 

# Procesar fotogramas de mi Pokémon
fotogramas_pokemon_mio = []
for cuadro_mio in ImageSequence.Iterator(gif_mio_pil):
    cuadro_mio_rgba = cuadro_mio.convert("RGBA")                                                           # Convertir a RGBA para manejar transparencia
    byte_arr = io.BytesIO()                                                                                # Crear un buffer en memoria para guardar el cuadro como PNG
    cuadro_mio_rgba.save(byte_arr, format="PNG")                                                           # Guardar el cuadro en el buffer
    byte_arr.seek(0)                                                                                       # Volver al inicio del buffer para leerlo con Pygame
    sup_cuadro_mio = pygame.image.load(byte_arr).convert_alpha()                                           # Cargar el cuadro en Pygame manteniendo la transparencia
    
    ancho_orig_mio, alto_orig_mio = sup_cuadro_mio.get_size()                                              # Calcular el alto proporcional al ancho deseado para mantener la relación de aspecto
    alto_pokemon_calc = ((alto_orig_mio * ancho_pokemon) // ancho_orig_mio) * 1.5                          # Escalar el cuadro al nuevo tamaño manteniendo la calidad
    ancho_pokemon_calc = ancho_pokemon * 1.5
    cuadro_escalado_mio = pygame.transform.scale(sup_cuadro_mio, (ancho_pokemon_calc, alto_pokemon_calc))  # Agregar el cuadro escalado a la lista de fotogramas del Pokémon mío
    fotogramas_pokemon_mio.append(cuadro_escalado_mio)                                                     # Repetir el proceso para cada cuadro del gif del Pokémon rival

# Procesar fotogramas del Pokémon rival
fotogramas_pokemon_rival = []
for cuadro_rival in ImageSequence.Iterator(gif_rival_pil):
    cuadro_rival_rgba = cuadro_rival.convert("RGBA")
    byte_arr = io.BytesIO()
    cuadro_rival_rgba.save(byte_arr, format="PNG")
    byte_arr.seek(0)
    sup_cuadro_rival = pygame.image.load(byte_arr).convert_alpha()
    
    ancho_orig_rival, alto_orig_rival = sup_cuadro_rival.get_size()
    alto_pokemon_calc = (alto_orig_rival * ancho_pokemon) // ancho_orig_rival
    cuadro_escalado_rival = pygame.transform.scale(sup_cuadro_rival, (ancho_pokemon, alto_pokemon_calc))
    fotogramas_pokemon_rival.append(cuadro_escalado_rival)

# Cargar imagen de Fondo
try:
    fondo = pygame.image.load("fondo.png").convert()
except:
    print("\n[⚠️ ADVERTENCIA]: No se encontró 'fondo.png'. Creando un fondo gris por defecto.")
    fondo = pygame.Surface((ancho_ventana, alto_ventana))
    fondo.fill((100, 100, 100))

fondo = pygame.transform.scale(fondo, (ancho_ventana, alto_ventana))

# Variables de control de animación
indice_mio = 0
indice_rival = 0
ultimo_cambio_tiempo = pygame.time.get_ticks()
velocidad_de_animacion = 100 

# Coordenadas y líneas de suelo dinámicas
SUELO_MIO = 470      
SUELO_RIVAL = 320    
mio_x = 180          
rival_x = 675        

print("¡Todo listo! Abriendo ventana de juego...")

# ==========================================
# PARTE 3: BUCLE PRINCIPAL DEL JUEGO
# ==========================================
ejecutando = True                                                                                 
while ejecutando:
    # 1. Capturar eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # 2. Lógica de animación por tiempo
    tiempo_actual = pygame.time.get_ticks()
    if tiempo_actual - ultimo_cambio_tiempo > velocidad_de_animacion:
        indice_mio = (indice_mio + 1) % len(fotogramas_pokemon_mio)
        indice_rival = (indice_rival + 1) % len(fotogramas_pokemon_rival)
        ultimo_cambio_tiempo = tiempo_actual

    # 3. Dibujar capas en pantalla
    # Capa 1: El Fondo
    ventana.blit(fondo, (0, 0))
    
    # Capa 2: Pokémon Mío (Apoyado en su suelo)
    frame_mio = fotogramas_pokemon_mio[indice_mio]
    mio_y_dinamica = SUELO_MIO - frame_mio.get_height()
    ventana.blit(frame_mio, (mio_x, mio_y_dinamica))
    
    # Capa 3: Pokémon Rival (Apoyado en su suelo)
    frame_rival = fotogramas_pokemon_rival[indice_rival]
    rival_y_dinamica = SUELO_RIVAL - frame_rival.get_height()
    ventana.blit(frame_rival, (rival_x, rival_y_dinamica))

    # Actualizar gráficos e imponer FPS
    pygame.display.flip()
    reloj.tick(60)

# Cierre ordenado al salir del bucle
pygame.quit()
sys.exit()
