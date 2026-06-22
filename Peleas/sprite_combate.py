import pygame
import os
import random
import requests
import io
import threading
import sys
from PIL import Image, ImageSequence
import estilo  

def batalla(ventana, jugador): 
    pokemon_data = {"mio": None, "rival": None}
    pokemon_gifs = {"mio": None, "rival": None}
    error_carga = False

    def descargar_pokemon(tipo, vista):
        global error_carga
        try:
            data = requests.get(f"https://pokeapi.co/api/v2/pokemon/{random.randint(1, 151)}").json()
            
            # --- AGREGA ESTO PARA PROCESAR LOS ATAQUES ---
            ataques_procesados = []
            for m in data["moves"][:4]: # Tomamos hasta 4 ataques
                nombre_limpio = m["move"]["name"].replace("-", " ").capitalize()
                ataques_procesados.append({"nombre": nombre_limpio})
            
            # Guardamos los datos y la lista de ataques en el diccionario
            data["ataques"] = ataques_procesados
            pokemon_data[tipo] = data
            # ---------------------------------------------
            
            url = data["sprites"]["versions"]["generation-v"]["black-white"]["animated"][vista]
            pokemon_gifs[tipo] = Image.open(io.BytesIO(requests.get(url).content))
        except Exception as e:
            print(f"Error cargando {tipo}: {e}")
            error_carga = True

    # Inicialización de hilos paralelos para agilizar la carga desde la PokeAPI
    hilos = [
        threading.Thread(target=descargar_pokemon, args=("mio", "back_default")),
        threading.Thread(target=descargar_pokemon, args=("rival", "front_default"))
    ]
    for h in hilos: h.start()
    for h in hilos: h.join()

    # Si hubo problemas en la descarga, arrojamos un aviso amigable
    if error_carga:
        print("[ADVERTENCIA] Ocurrió un problema descargando los datos de los Pokémon.")

    pygame.init()
    pygame.display.set_caption("Poke-Unsam - Batalla")
    reloj = pygame.time.Clock()
    fondo_combate = estilo.obtener_fondo_aleatorio()  # hay que traer el fondo segun el NPC que se hable

    def procesar_gif(gif_pil, factor_escala=2.5):
        lista_frames = []
        for frame in ImageSequence.Iterator(gif_pil):
            frame_rgba = frame.convert("RGBA")
            sup = pygame.image.frombytes(frame_rgba.tobytes(), frame_rgba.size, "RGBA").convert_alpha()
            
            # Escalado relativo basado en el tamaño original devuelto por la API
            w, h = frame_rgba.size
            nuevo_ancho = int(w * factor_escala)
            nuevo_alto = int(h * factor_escala)
            
            frame_escalado = pygame.transform.scale(sup, (nuevo_ancho, nuevo_alto)).convert_alpha()
            lista_frames.append(frame_escalado)
        return lista_frames

    pos_mia, pos_rival, tam_base = estilo.escenario_actual

    # Ajuste de escala de visualización: Mayor tamaño para el Pokémon propio (perspectiva de espalda)
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
    texto_pantalla = f"Un {nombre_rival} salvaje apareció! Qué hará {nombre_mio}?"

    # Dentro de la función batalla()
    mensajes_acciones = {
        "Atacar": f"{nombre_mio} usó un ataque devastador!",
        "Objetos": "Abriendo la mochila de objetos...",
        "Cambiar": f"¿A qué Pokémon quieres llamar?" # Nueva entrada
    }

    MOSTRANDO_ATAQUES = False
    def generar_rects_ataques(lista_ataques):
        # Ajuste de coordenadas para los 4 ataques en cuadrícula
        # Usamos estilo.ALTO_COMBATE para mantener la coherencia con tu configuración
        posiciones = [
            (600, estilo.ALTO_COMBATE + 15), (810, estilo.ALTO_COMBATE + 15),
            (600, estilo.ALTO_COMBATE + 65), (810, estilo.ALTO_COMBATE + 65)
        ]
        botones_atk = {}
        
        # Asegúrate de iterar sobre los ataques disponibles
        for i, atk in enumerate(lista_ataques[:4]): 
            # Creamos el botón
            rect = pygame.Rect(posiciones[i][0], posiciones[i][1], 200, 40)
            # Renderizamos el texto del ataque
            txt = estilo.fuente_nombre.render(atk["nombre"], True, (255, 255, 255))
            # Guardamos en el diccionario
            botones_atk[f"Ataque{i+1}"] = (rect, (248, 112, 112), txt)
            
        return botones_atk

    def generar_rects_ataques(lista_ataques):
        posiciones = [
            (600, estilo.ALTO_COMBATE + 15), (810, estilo.ALTO_COMBATE + 15),
            (600, estilo.ALTO_COMBATE + 65), (810, estilo.ALTO_COMBATE + 65)
        ]
        botones_atk = {}
        for i, atk in enumerate(lista_ataques):
            rect = pygame.Rect(posiciones[i][0], posiciones[i][1], 200, 40)
            # Usamos el nombre que procesamos en la descarga
            txt = estilo.fuente_nombre.render(atk["nombre"], True, (255, 255, 255))
            botones_atk[f"Ataque{i+1}"] = (rect, (248, 112, 112), txt)
        return botones_atk


    def obtener_botones_segun_menu(menu, data_mio, offset):
        botones_dinamicos = {}
        
        if menu == "ATAQUES":
            posiciones = [(600, 600), (810, 600), (600, 650), (810, 650)]
            for i, atk in enumerate(data_mio.get("ataques", [])[:4]):
                rect = pygame.Rect(posiciones[i][0], posiciones[i][1], 200, 40)
                botones_dinamicos[f"Ataque{i+1}"] = (rect, (248, 112, 112), estilo.fuente_nombre.render(atk["nombre"], True, (255, 255, 255)))

        elif menu == "OBJETOS":
            # Dos botones grandes
            botones_dinamicos["Pocion"] = (pygame.Rect(600, 600, 400, 40), (120, 200, 80), estilo.fuente_nombre.render("Pocion", True, (255, 255, 255)))
            botones_dinamicos["Revivir"] = (pygame.Rect(600, 650, 400, 40), (120, 200, 80), estilo.fuente_nombre.render("Revivir", True, (255, 255, 255)))

        elif menu == "POKEMONES":
            # Botones horizontales y flechas
            botones_dinamicos["Izq"] = (pygame.Rect(550, 625, 40, 40), (200, 200, 200), estilo.fuente_nombre.render("<", True, (0, 0, 0)))
            botones_dinamicos["Der"] = (pygame.Rect(1020, 625, 40, 40), (200, 200, 200), estilo.fuente_nombre.render(">", True, (0, 0, 0)))
            # Aquí cargarías nombres según el offset (página 1: 0-1, página 2: 2-3, página 3: 4-5)
            botones_dinamicos["Pkm1"] = (pygame.Rect(600, 600, 200, 40), (100, 100, 200), estilo.fuente_nombre.render("Pkmn A", True, (255, 255, 255)))
            botones_dinamicos["Pkm2"] = (pygame.Rect(810, 600, 200, 40), (100, 100, 200), estilo.fuente_nombre.render("Pkmn B", True, (255, 255, 255)))
            
        return botones_dinamicos
# ==================================
# PARTE 3: BUCLE PRINCIPAL JUEGO
# ==================================
# ESTADOS DEL MENÚ (Fuera del while)
    MENU_ACTUAL = "PRINCIPAL" 
    OFFSET_POKEMONES = 0
    
    # ==================================
    # PARTE 3: BUCLE PRINCIPAL JUEGO
    # ==================================
    ejecutando = True
    while ejecutando:
        mouse_pos = pygame.mouse.get_pos()
        
        # 1. GESTIÓN DE EVENTOS
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                ejecutando = False
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                
                # Definimos los botones activos según el estado actual
                if MENU_ACTUAL == "PRINCIPAL":
                    btns = botones
                else:
                    btns = obtener_botones_segun_menu(MENU_ACTUAL, pokemon_data["mio"], OFFSET_POKEMONES)
                
                # Procesamos el clic
                for nom, (rect, _, _) in btns.items():
                    if rect.collidepoint(mouse_pos):
                        
                        if MENU_ACTUAL == "PRINCIPAL":
                            if nom == "Atacar": MENU_ACTUAL = "ATAQUES"
                            elif nom == "Objetos": MENU_ACTUAL = "OBJETOS"
                            elif nom == "Cambiar": MENU_ACTUAL = "POKEMONES"
                            elif nom in mensajes_acciones: texto_pantalla = mensajes_acciones[nom]
                        
                        else:
                            # Lógica dentro de menús secundarios
                            if nom == "Izq": 
                                OFFSET_POKEMONES = max(0, OFFSET_POKEMONES - 1)
                            elif nom == "Der": 
                                OFFSET_POKEMONES = min(2, OFFSET_POKEMONES + 1)
                            else:
                                # Aquí procesas la selección de un ataque, objeto o pokemon
                                if "Ataque" in nom:
                                    idx_ataque = int(nom[-1]) - 1
                                    res = procesar_turno_logico(pokemon_data["mio"], pokemon_data["rival"], idx_ataque)
                                    texto_pantalla = f"{pokemon_data['mio']['name'].capitalize()} usó {res['nombre_ataque']}!"
                                else:
                                    texto_pantalla = f"Elegiste: {nom}"
                                
                                # Volvemos al menú principal tras elegir
                                MENU_ACTUAL = "PRINCIPAL"
                            
        # 2. LÓGICA DE ANIMACIÓN (GIFs)
        if pygame.time.get_ticks() - ultimo_cambio > 90:
            for k in idx: 
                idx[k] = (idx[k] + 1) % len(frames[k])
            ultimo_cambio = pygame.time.get_ticks()

        # 3. DIBUJADO DE ESCENARIO Y POKÉMONS
        ventana.blit(fondo_combate, (0, 0))
        for k, (x_din, suelo) in [("mio", pos_mia), ("rival", pos_rival)]:
            fr = frames[k][idx[k]]
            ventana.blit(fr, (x_din - (fr.get_width() // 2), suelo - fr.get_height()))

        # 4. PANEL INFERIOR Y TEXTO
        pygame.draw.rect(ventana, estilo.COLOR_PANEL, (0, estilo.ALTO_COMBATE, estilo.ANCHO_VENTANA, estilo.ALTO_PANEL))
        ventana.blit(estilo.fuente_nombre.render(texto_pantalla, True, estilo.COLOR_TEXTO), (30, estilo.ALTO_COMBATE + 45))

        # 5. INTERFAZ GRÁFICA DE BOTONES (Dinámica según MENU_ACTUAL)
        if MENU_ACTUAL == "PRINCIPAL":
            botones_a_dibujar = botones
        else:
            botones_a_dibujar = obtener_botones_segun_menu(MENU_ACTUAL, pokemon_data["mio"], OFFSET_POKEMONES)
        
        for nombre, (rect, color, txt_btn) in botones_a_dibujar.items():
            color_f = tuple(min(c + 35, 255) for c in color) if rect.collidepoint(mouse_pos) else color
            pygame.draw.rect(ventana, color_f, rect, border_radius=6)
            pygame.draw.rect(ventana, estilo.COLOR_BORDE, rect, 2, border_radius=6)
            ventana.blit(txt_btn, txt_btn.get_rect(center=rect.center))

        pygame.display.flip()
        reloj.tick(estilo.FPS)
