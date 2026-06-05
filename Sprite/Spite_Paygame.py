import io
import sys
import paygame
import requests 
from pil import Image, ImagenSequence

# Inicialisamos paygame 
paygame.init()

# Configuracion ventana 
ancho_ventana = 1064
alto_ventana = 582
ventana = paygame.display.set_mode((ancho_ventana, alto_ventana))

# Definimos un reloj para los movimientos fluidos 
reloj = paygame.time.clock()

# Definimos los enlaces para cada pokemon
# --- Mio ---
url_mio = https://pokeapi.co/api/v2/pokemon/ + input("Ingrese pokemon a usar: ").lower()
datos_mio = requests.get(url_mio).json()
url_gif_mio = datos_mio["sprite"]["versiones"][generation-v"]["black-white"]["animated"]["back-default"]

# --- Rival ---
url_rival = https://pokeapi.co/api/v2/pokemon/ditto 
datos_rival = requests.get(url_rival).json()
url_gif_rival = datos_rival["sprite"]["versiones"][generation-v"]["black-white"]["animated"]["front-default"]

# Descargar gifs 
# --- Mio ---
bits_gif_mio = requets.get(url_gif_mio).content
gif_mio_memoria = io.BytesIO(bits_gif_mio)

# --- Rival ---
bits_gif_rival = requets.get(url_gif_rival).content
gif_rival_memoria = io.BytesIO(bits_gif_rival)

# Abri el gif en pillow para sacar sis fotogramas
# --- Mio ---
gif_mio_pil = Image.open(gif_mio_memoria)
fotogramas_pokemon_mio = []

# --- Rival ---
gif_rival_pil = Image.open(gif_rival_memoria)
fotogramas_pokemon_rival = []

ancho_pokemon = 150 # <--- Ancho a definir

for cuadro_mio in ImageSequence.Interator(gif_mio_pil):
    cuadro_mio_rgba = cuadro_mio.convert("RGBA")            # Mantiene la transparencia y los colores
    byte_arr = io.BytesIO()                                 # Crea un espacio en la memoria
    cuadro_mio_rgba.save(byte_arr, format = "PNG")          # Guarda la foto en pillow 
    byte_arr.seek(0)                                        # Pone los fotogramas desde el inicio
    
    sup_cuadro_mio = paygame.image.load(byte_arr).convert_apha()     # Aplicamos paygame
    
    # Para mantener dimenciones de los ponemons 
    ancho_orig_mio, alto_orig_mio = sup_cuadro_mio.get_size()       # Conseguimos las dimenciones 
    alto_pokemons = (alto_original_mio * ancho_pokemon) // ancho_orig_mio
    cuadro_escalado_mio = paygame.transform.scale(sup_cuadro_mio, (alto_pokemon, ancho_pokemon))
    
    fotograma_pokemon_mio.append(cuadro_escalado_mio)
    