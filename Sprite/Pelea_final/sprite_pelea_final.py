import io, sys, pygame, random, requests, threading
import estilos
from PIL import Image, ImageSequence

# ==================================================
# PARTE 1: DESCARGA EN PARALELO (MULTITHREADING)
# ==================================================
poke_mio, poke_riv = random.randint(1, 20), random.randint(1, 150)
gif_mio = gif_riv = None
res_mio = res_riv = None

def descargar_mio():
    global gif_mio, res_mio
    res_mio = requests.get(f"https://pokeapi.co/api/v2/pokemon/{poke_mio}").json()
    url = res_mio["sprites"]["versions"]["generation-v"]["black-white"]["animated"]["back_default"]
    gif_mio = Image.open(io.BytesIO(requests.get(url).content))

def descargar_rival():
    global gif_riv, res_riv
    res_riv = requests.get(f"https://pokeapi.co/api/v2/pokemon/{poke_riv}").json()
    url = res_riv["sprites"]["versions"]["generation-v"]["black-white"]["animated"]["front_default"]
    gif_riv = Image.open(io.BytesIO(requests.get(url).content))

print("Descargando ambos Pokémon en paralelo...")
hilo_mio = threading.Thread(target=descargar_mio)
hilo_rival = threading.Thread(target=descargar_rival)

hilo_mio.start()
hilo_rival.start()
hilo_mio.join() 
hilo_rival.join() 

# =================================================
# PARTE 2: INICIALIZACIÓN Y CONFIGURACIÓN DESDE MODULO
# =================================================
pygame.init()
ventana = pygame.display.set_mode((estilos.ANCHO_VENTANA, estilos.ALTO_VENTANA))
pygame.display.set_caption(estilos.TITULO_JUEGO)
reloj = pygame.time.Clock()

fuente = pygame.font.SysFont("Helvetica", 22, bold=True)
fuente_stats = pygame.font.SysFont("Helvetica", 16, bold=True)

# --- PROCESAMIENTO OPTIMIZADO DE TEXTURAS ---
def procesar_gif(gif_pil, escala_extra=1.0):
    lista_frames = []
    for frame in ImageSequence.Iterator(gif_pil):
        frame_rgba = frame.convert("RGBA")
        sup = pygame.image.fromstring(frame_rgba.tobytes(), frame_rgba.size, "RGBA").convert_alpha()
        
        w, h = frame_rgba.size
        nuevo_ancho = int(100 * escala_extra)
        nuevo_alto = int((h * nuevo_ancho) // w)
        
        frame_escalado = pygame.transform.scale(sup, (nuevo_ancho, nuevo_alto)).convert_alpha()
        lista_frames.append(frame_escalado)
    return lista_frames

frames_mio = procesar_gif(gif_mio, 1.2)
frames_rival = procesar_gif(gif_riv, 1.0)

fondo = pygame.transform.scale(pygame.image.load("fondo.png").convert(), (estilos.ANCHO_VENTANA, estilos.ALTO_COMBATE))

idx_mio = idx_rival = 0
ultimo_cambio = pygame.time.get_ticks()

# Estructura limpia de botones inyectando los estilos cargados
botones = {}
for nombre, (rect, color) in estilos.DATOS_BOTONES.items():
    txt_sup = fuente.render(nombre, True, (255, 255, 255)).convert_alpha()
    botones[nombre] = (rect, color, txt_sup)

nombre_mio, nombre_rival = res_mio["name"].capitalize(), res_riv["name"].capitalize()
texto_pantalla = f"¡Un {nombre_rival} salvaje apareció! ¿Qué hará {nombre_mio}?"

# ==================================
# PARTE 3: BUCLE PRINCIPAL
# ==================================
ejecutando = True                                                                                
while ejecutando:
    mouse_pos = pygame.mouse.get_pos()
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for nombre, (rect, _, _) in botones.items():
                if rect.collidepoint(mouse_pos):
                    if nombre == "Atacar": texto_pantalla = f"¡{nombre_mio} usó un ataque devastador!"
                    elif nombre == "Esquivar": texto_pantalla = f"¡{nombre_mio} se prepara para esquivar!"
                    elif nombre == "Defenderse": texto_pantalla = f"¡{nombre_mio} aumentó su Defensa!"
                    elif nombre == "Cambiar Pokemon": texto_pantalla = "Buscando en la Pokébola..."

    # Animación por tiempo
    tiempo_actual = pygame.time.get_ticks()
    if tiempo_actual - ultimo_cambio > 100:
        idx_mio = (idx_mio + 1) % len(frames_mio)
        idx_rival = (idx_rival + 1) % len(frames_rival)
        ultimo_cambio = tiempo_actual

    # 1. Dibujado de Escenario y Pokémon
    ventana.blit(fondo, (0, 0))
    
    frame_actual_mio = frames_mio[idx_mio]
    mio_y_dinamica = estilos.SUELO_MIO - frame_actual_mio.get_height()
    ventana.blit(frame_actual_mio, (estilos.MIO_X, mio_y_dinamica))
    
    frame_actual_rival = frames_rival[idx_rival]
    rival_y_dinamica = estilos.SUELO_RIVAL - frame_actual_rival.get_height()
    ventana.blit(frame_actual_rival, (estilos.RIVAL_X, rival_y_dinamica))

    # 2. Dibujado de Panel Inferior
    pygame.draw.rect(ventana, estilos.COLOR_PANEL, (0, estilos.ALTO_COMBATE, estilos.ANCHO_VENTANA, estilos.ALTO_PANEL))
    pygame.draw.line(ventana, estilos.COLOR_BORDE, (0, estilos.ALTO_COMBATE), (estilos.ANCHO_VENTANA, estilos.ALTO_COMBATE), 4)
    ventana.blit(fuente.render(texto_pantalla, True, estilos.COLOR_TEXTO), (30, estilos.ALTO_COMBATE + 45))

    # 3. Dibujado de Botones
    for nombre, (rect, color, txt_btn) in botones.items(): 
        color_f = tuple(min(c + 45, 255) for c in color) if rect.collidepoint(mouse_pos) else color
        pygame.draw.rect(ventana, color_f, rect, border_radius=5)
        pygame.draw.rect(ventana, estilos.COLOR_BORDE, rect, 2, border_radius=5)
        ventana.blit(txt_btn, txt_btn.get_rect(center=rect.center))

    # 4. Sistema de Tooltips (Estadísticas al pasar el Mouse)
    rect_mio = pygame.Rect(estilos.MIO_X, mio_y_dinamica, frame_actual_mio.get_width(), frame_actual_mio.get_height())
    rect_riv = pygame.Rect(estilos.RIVAL_X, rival_y_dinamica, frame_actual_rival.get_width(), frame_actual_rival.get_height())

    pokemon_detectado = None
    if rect_mio.collidepoint(mouse_pos):
        pokemon_detectado = res_mio
    elif rect_riv.collidepoint(mouse_pos):
        pokemon_detectado = res_riv

    if pokemon_detectado:
        stats = {s["stat"]["name"].upper(): s["base_stat"] for s in pokemon_detectado["stats"] if s["stat"]["name"] in ["hp", "attack", "defense", "speed"]}
        
        ancho_cartel, alto_cartel = 160, 110
        cartel_x = mouse_pos[0] + 15 if mouse_pos[0] + 15 + ancho_cartel < estilos.ANCHO_VENTANA else mouse_pos[0] - ancho_cartel - 15
        cartel_y = mouse_pos[1] + 15 if mouse_pos[1] + 15 + alto_cartel < estilos.ALTO_COMBATE else mouse_pos[1] - alto_cartel - 15
        
        sup_stats = pygame.Surface((ancho_cartel, alto_cartel), pygame.SRCALPHA)
        sup_stats.fill(estilos.COLOR_FONDO_TOOLTIP) 
        pygame.draw.rect(sup_stats, estilos.COLOR_BORDE, (0, 0, ancho_cartel, alto_cartel), 2, border_radius=4)
        
        y_off = 12
        for s_nom, s_val in stats.items():
            txt_stat = fuente_stats.render(f"{s_nom}: {s_val}", True, (255, 255, 255))
            sup_stats.blit(txt_stat, (12, y_off))
            y_off += 22
            
        ventana.blit(sup_stats, (cartel_x, cartel_y))

    pygame.display.flip()
    reloj.tick(estilos.FPS)

pygame.quit()
sys.exit()