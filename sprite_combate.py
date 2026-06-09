import estilo  # Llamada al archivo de los estilos de la página
import io, sys, pygame, random, requests, threading
from PIL import Image, ImageSequence

# ==================================================
# PARTE 1: PETICIÓN DE POKÉMON Y DESCARGA MULTITHREADING
# ==================================================
pokemon_data = {"mio": None, "rival": None}
pokemon_gifs = {"mio": None, "rival": None}
error_carga = False

def descargar_pokemon(tipo, vista):
    global error_carga
    try:
        data = requests.get(f"https://pokeapi.co/api/v2/pokemon/{random.randint(1, 151)}").json()
        url = data["sprites"]["versions"]["generation-v"]["black-white"]["animated"][vista]
        pokemon_data[tipo] = data
        pokemon_gifs[tipo] = Image.open(io.BytesIO(requests.get(url).content))
    except Exception as e:
        print(f"Error cargando {tipo}: {e}")
        error_carga = True

hilos = [
    threading.Thread(target=descargar_pokemon, args=("mio", "back_default")),
    threading.Thread(target=descargar_pokemon, args=("rival", "front_default"))
]
for h in hilos: h.start()
for h in hilos: h.join()

# =================================================
# PARTE 2: INICIALIZACIÓN DE PYGAME Y TEXTURAS
# =================================================
pygame.init()
ventana = pygame.display.set_mode((estilo.ANCHO_VENTANA, estilo.ALTO_VENTANA))
reloj = pygame.time.Clock()
fondo_combate = estilo.obtener_fondo_aleatorio()

def procesar_gif(gif_pil, factor_escala=2.5):
    lista_frames = []
    for frame in ImageSequence.Iterator(gif_pil):
        frame_rgba = frame.convert("RGBA")
        sup = pygame.image.frombytes(frame_rgba.tobytes(), frame_rgba.size, "RGBA").convert_alpha()
        
        # Obtenemos el tamaño original del sprite de la API
        w, h = frame_rgba.size
        
        # Escalamos multiplicando el tamaño original por el factor (ej: 2.5 veces más grande)
        nuevo_ancho = int(w * factor_escala)
        nuevo_alto = int(h * factor_escala)
        
        frame_escalado = pygame.transform.scale(sup, (nuevo_ancho, nuevo_alto)).convert_alpha()
        lista_frames.append(frame_escalado)
    return lista_frames

pos_mia, pos_rival, tam_base = estilo.escenario_actual

# Ajustá estos números a tu gusto. 
# 3.0 para tu espalda (más cerca) y 2.2 para el rival (más lejos) suele quedar muy bien.
frames = {
    "mio": procesar_gif(pokemon_gifs["mio"], factor_escala=3.0),
    "rival": procesar_gif(pokemon_gifs["rival"], factor_escala=2.2)
}

idx = {"mio": 0, "rival": 0}
ultimo_cambio = pygame.time.get_ticks()

botones = {nom: (r, c, estilo.fuente_nombre.render(nom, True, (255, 255, 255)).convert_alpha()) 
            for nom, (r, c) in estilo.DATOS_BOTONES.items()}

nombre_mio = pokemon_data["mio"]["name"].capitalize()
nombre_rival = pokemon_data["rival"]["name"].capitalize()
texto_pantalla = f"Un {nombre_rival} salvaje aparecio! Que hara {nombre_mio}?"

mensajes_acciones = {
    "Atacar": f"{nombre_mio} uso un ataque devastador!",
    "Esquivar": f"{nombre_mio} se mueve velozmente!",
    "Defenderse": f"La Defensa de {nombre_mio} aumento!",
    "Huir": "Intentaste escapar con exito!"
}

# ==================================
# PARTE 3: BUCLE PRINCIPAL JUEGO
# ==================================
ejecutando = True
while ejecutando:
    mouse_pos = pygame.mouse.get_pos()
    
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT: ejecutando = False
        elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            for nom, (rect, _, _) in botones.items():
                if rect.collidepoint(mouse_pos) and nom in mensajes_acciones:
                    texto_pantalla = mensajes_acciones[nom]
                    break

    if pygame.time.get_ticks() - ultimo_cambio > 90:
        for k in idx: idx[k] = (idx[k] + 1) % len(frames[k])
        ultimo_cambio = pygame.time.get_ticks()

    # 1. DIBUJADO DE ESCENARIO
    ventana.blit(fondo_combate, (0, 0))
    pos_mia, pos_rival, _ = estilo.escenario_actual
    
    # Renderizado inteligente de ambos Pokémon en un bucle corto
    rects_pkmn = {}
    for k, (x_din, suelo) in [("mio", pos_mia), ("rival", pos_rival)]:
        fr = frames[k][idx[k]]
        
        # Restamos la mitad del ancho del sprite para que x_din sea el CENTRO
        x_centro = x_din - (fr.get_width() // 2)
        y_din = suelo - fr.get_height()
        
        # Dibujamos en la posición centrada
        ventana.blit(fr, (x_centro, y_din))
        
        # Guardamos el Rect correcto para que el sistema de Tooltips (hover) funcione bien
        rects_pkmn[k] = pygame.Rect(x_centro, y_din, fr.get_width(), fr.get_height())

    # 2. PANEL INFERIOR DE TEXTO
    pygame.draw.rect(ventana, estilo.COLOR_PANEL, (0, estilo.ALTO_COMBATE, estilo.ANCHO_VENTANA, estilo.ALTO_PANEL))
    pygame.draw.line(ventana, estilo.COLOR_BORDE, (0, estilo.ALTO_COMBATE), (estilo.ANCHO_VENTANA, estilo.ALTO_COMBATE), 4)
    
    if "!" in texto_pantalla:
        partes = texto_pantalla.split("!")
        ventana.blit(estilo.fuente_nombre.render(partes[0] + "!", True, estilo.COLOR_TEXTO), (30, estilo.ALTO_COMBATE + 30))
        if len(partes) > 1 and partes[1].strip():
            ventana.blit(estilo.fuente_nombre.render(partes[1].strip(), True, estilo.COLOR_TEXTO), (30, estilo.ALTO_COMBATE + 65))
    else:
        ventana.blit(estilo.fuente_nombre.render(texto_pantalla, True, estilo.COLOR_TEXTO), (30, estilo.ALTO_COMBATE + 45))

    # 3. DIBUJADO DE BOTONES
    for nombre, (rect, color, txt_btn) in botones.items():
        color_f = tuple(min(c + 35, 255) for c in color) if rect.collidepoint(mouse_pos) else color
        pygame.draw.rect(ventana, color_f, rect, border_radius=6)
        pygame.draw.rect(ventana, estilo.COLOR_BORDE, rect, 2, border_radius=6)
        ventana.blit(txt_btn, txt_btn.get_rect(center=rect.center))

    # 4. SISTEMA DE TOOLTIPS
    pkmn_hover = "mio" if rects_pkmn["mio"].collidepoint(mouse_pos) else "rival" if rects_pkmn["rival"].collidepoint(mouse_pos) else None
    if pkmn_hover:
        p_data = pokemon_data[pkmn_hover]
        stats = {s["stat"]["name"].upper(): s["base_stat"] for s in p_data["stats"] if s["stat"]["name"] in ["hp", "attack", "defense", "speed"]}
        
        w_c, h_c = 170, 115
        cx = mouse_pos[0] + 15 if mouse_pos[0] + 15 + w_c < estilo.ANCHO_VENTANA else mouse_pos[0] - w_c - 15
        cy = mouse_pos[1] + 15 if mouse_pos[1] + 15 + h_c < estilo.ALTO_COMBATE else mouse_pos[1] - h_c - 15
        
        sup_stats = pygame.Surface((w_c, h_c), pygame.SRCALPHA)
        sup_stats.fill(estilo.COLOR_FONDO_TOOLTIP)
        pygame.draw.rect(sup_stats, estilo.COLOR_BORDE, (0, 0, w_c, h_c), 2, border_radius=4)
        
        for i, (s_nom, s_val) in enumerate(stats.items()):
            sup_stats.blit(estilo.fuente_stats.render(f"{s_nom}: {s_val}", True, (255, 255, 255)), (12, 12 + i * 24))
        
        ventana.blit(sup_stats, (cx, cy))

    pygame.display.flip()
    reloj.tick(estilo.FPS)

pygame.quit()
sys.exit()