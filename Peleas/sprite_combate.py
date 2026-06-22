import pygame,sys,os,random,requests,io,threading
import os
import random
import requests
import io
import threading
import sys
from PIL import Image, ImageSequence
import estilo  

# 1. IMPORTAMOS TU CLASE REAL Y LA LÓGICA DE COMBATE
from pokemons.PokePlantilla import Pokemon
from Peleas.logica_combate import procesar_turno_logico

def batalla(ventana, jugador): 
    # Ahora guardaremos instancias reales de la clase Pokemon
    pokemon_instancias = {"mio": None, "rival": None}
    pokemon_gifs = {"mio": None, "rival": None}
    error_carga = False

    def descargar_y_crear_pokemon(tipo, vista):
        global error_carga
        try:
            # Generamos un ID aleatorio de la primera generación
            id_aleatorio = random.randint(1, 151)
            
            # --- INTEGRACIÓN CON TU CLASE PYTHON ---
            # Instanciamos la clase Pokemon (ella se encarga de descargar stats, ataques reales, etc.)
            pkmn = Pokemon(id_aleatorio)
            pokemon_instancias[tipo] = pkmn
            # ---------------------------------------
            
            # Buscamos la URL del GIF animado usando los datos crudos que necesita Pygame/PIL
            # Hacemos una consulta rápida solo para la animación usando el ID de nuestra instancia
            url_api = f"https://pokeapi.co/api/v2/pokemon/{pkmn.id}"
            data_cruda = requests.get(url_api).json()
            url_gif = data_cruda["sprites"]["versions"]["generation-v"]["black-white"]["animated"][vista]
            
            pokemon_gifs[tipo] = Image.open(io.BytesIO(requests.get(url_gif).content))
        except Exception as e:
            print(f"Error cargando {tipo}: {e}")
            error_carga = True

    # Inicialización de hilos paralelos para agilizar la carga de imágenes
    hilos = [
        threading.Thread(target=descargar_y_crear_pokemon, args=("mio", "back_default")),
        threading.Thread(target=descargar_y_crear_pokemon, args=("rival", "front_default"))
    ]
    for h in hilos: h.start()
    for h in hilos: h.join()

    # Si hubo problemas en la descarga, arrojamos un aviso amigable
    if error_carga or not pokemon_instancias["mio"] or not pokemon_instancias["rival"]:
        print("[ADVERTENCIA] Ocurrió un problema descargando los datos de los Pokémon.")
        return

    # Asignamos las variables de combate usando los objetos de tu clase
    mi_pokemon = pokemon_instancias["mio"]
    pokemon_rival = pokemon_instancias["rival"]

    pygame.init()
    pygame.display.set_caption("Poke-Unsam - Batalla")
    reloj = pygame.time.Clock()
    fondo_combate = estilo.obtener_fondo_aleatorio()  

    def procesar_gif(gif_pil, factor_escala=2.5):
        lista_frames = []
        for frame in ImageSequence.Iterator(gif_pil):
            frame_rgba = frame.convert("RGBA")
            sup = pygame.image.frombytes(frame_rgba.tobytes(), frame_rgba.size, "RGBA").convert_alpha()
            
            w, h = frame_rgba.size
            nuevo_ancho = int(w * factor_escala)
            nuevo_alto = int(h * factor_escala)
            
            frame_escalado = pygame.transform.scale(sup, (nuevo_ancho, nuevo_alto)).convert_alpha()
            lista_frames.append(frame_escalado)
        return lista_frames

    pos_mia, pos_rival, tam_base = estilo.escenario_actual

    # Procesamos los frames de los gifs descargados
    frames = {
        "mio": procesar_gif(pokemon_gifs["mio"], factor_escala=3.0),
        "rival": procesar_gif(pokemon_gifs["rival"], factor_escala=2.2)
    }

    idx = {"mio": 0, "rival": 0}
    ultimo_cambio = pygame.time.get_ticks()

    botones = {nom: (r, c, estilo.fuente_nombre.render(nom, True, (255, 255, 255)).convert_alpha()) 
                for nom, (r, c) in estilo.DATOS_BOTONES.items()}

    # Accedemos a las propiedades reales (.nombre) de tus objetos
    nombre_mio = mi_pokemon.nombre
    nombre_rival = pokemon_rival.nombre
    texto_pantalla = f"Un {nombre_rival} salvaje apareció! Qué hará {nombre_mio}?"

    mensajes_acciones = {
        "Atacar": f"{nombre_mio} usó un ataque devastador!",
        "Objetos": "Abriendo la mochila de objetos...",
        "Cambiar": f"¿A qué Pokémon quieres llamar?" 
    }

    def obtener_botones_segun_menu(menu, pokemon_obj, offset):
        botones_dinamicos = {}
        
        if menu == "ATAQUES":
            posiciones = [(600, 600), (810, 600), (600, 650), (810, 650)]
            # Usamos los ataques reales cargados por tu clase Pokémon
            for i, atk in enumerate(pokemon_obj.ataques[:4]):
                rect = pygame.Rect(posiciones[i][0], posiciones[i][1], 200, 40)
                botones_dinamicos[f"Ataque{i+1}"] = (
                    rect, 
                    (248, 112, 112), 
                    estilo.fuente_nombre.render(atk["nombre"], True, (255, 255, 255))
                )

        elif menu == "OBJETOS":
            botones_dinamicos["Pocion"] = (pygame.Rect(600, 600, 400, 40), (120, 200, 80), estilo.fuente_nombre.render("Pocion", True, (255, 255, 255)))
            botones_dinamicos["Revivir"] = (pygame.Rect(600, 650, 400, 40), (120, 200, 80), estilo.fuente_nombre.render("Revivir", True, (255, 255, 255)))

        elif menu == "POKEMONES":
            botones_dinamicos["Izq"] = (pygame.Rect(550, 625, 40, 40), (200, 200, 200), estilo.fuente_nombre.render("<", True, (0, 0, 0)))
            botones_dinamicos["Der"] = (pygame.Rect(1020, 625, 40, 40), (200, 200, 200), estilo.fuente_nombre.render(">", True, (0, 0, 0)))
            botones_dinamicos["Pkm1"] = (pygame.Rect(600, 600, 200, 40), (100, 100, 200), estilo.fuente_nombre.render("Pkmn A", True, (255, 255, 255)))
            botones_dinamicos["Pkm2"] = (pygame.Rect(810, 600, 200, 40), (100, 100, 200), estilo.fuente_nombre.render("Pkmn B", True, (255, 255, 255)))
            
        return botones_dinamicos

    MENU_ACTUAL = "PRINCIPAL" 
    OFFSET_POKEMONES = 0
    
    ejecutando = True
    while ejecutando:
        mouse_pos = pygame.mouse.get_pos()
        
        # 1. GESTIÓN DE EVENTOS
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                ejecutando = False
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                
                if MENU_ACTUAL == "PRINCIPAL":
                    btns = botones
                else:
                    btns = obtener_botones_segun_menu(MENU_ACTUAL, mi_pokemon, OFFSET_POKEMONES)
                
                for nom, (rect, _, _) in btns.items():
                    if rect.collidepoint(mouse_pos):
                        
                        if MENU_ACTUAL == "PRINCIPAL":
                            if nom == "Atacar": MENU_ACTUAL = "ATAQUES"
                            elif nom == "Objetos": MENU_ACTUAL = "OBJETOS"
                            elif nom == "Cambiar": MENU_ACTUAL = "POKEMONES"
                            elif nom in mensajes_acciones: texto_pantalla = mensajes_acciones[nom]
                        
                        else:
                            if nom == "Izq": 
                                OFFSET_POKEMONES = max(0, OFFSET_POKEMONES - 1)
                            elif nom == "Der": 
                                OFFSET_POKEMONES = min(2, OFFSET_POKEMONES + 1)
                            else:
                                # --- PROCESAMIENTO DEL TURNO LOGICO REAL ---
                                if "Ataque" in nom:
                                    # Extraemos el índice del ataque seleccionado (0 a 3)
                                    idx_ataque = int(nom[-1]) - 1
                                    
                                    # Ejecutamos tu función conectando las dos instancias de clase
                                    res = procesar_turno_logico(mi_pokemon, pokemon_rival, idx_ataque)
                                    
                                    # Cambiamos el texto de pantalla con el daño calculado por el modelo matemático
                                    texto_pantalla = f"{nombre_mio} usó {res['nombre_ataque']}! Hizo {res['daño']} de daño."
                                    
                                    if res["debilitado"]:
                                        texto_pantalla += f" ¡El {nombre_rival} enemigo se debilitó!"
                                else:
                                    texto_pantalla = f"Elegiste: {nom}"
                                
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
        
        # Agregamos un indicador rápido de Vida actual en el texto para testear el daño en pantalla
        info_vida = f" [{mi_pokemon.vida_actual}/{mi_pokemon.stats['vida_max']} HP] vs Rival [{pokemon_rival.vida_actual}/{pokemon_rival.stats['vida_max']} HP]"
        ventana.blit(estilo.fuente_nombre.render(texto_pantalla + info_vida, True, estilo.COLOR_TEXTO), (30, estilo.ALTO_COMBATE + 45))

        # 5. INTERFAZ GRÁFICA DE BOTONES
        if MENU_ACTUAL == "PRINCIPAL":
            botones_a_dibujar = botones
        else:
            botones_a_dibujar = obtener_botones_segun_menu(MENU_ACTUAL, mi_pokemon, OFFSET_POKEMONES)
        
        for nombre, (rect, color, txt_btn) in botones_a_dibujar.items():
            color_f = tuple(min(c + 35, 255) for c in color) if rect.collidepoint(mouse_pos) else color
            pygame.draw.rect(ventana, color_f, rect, border_radius=6)
            pygame.draw.rect(ventana, estilo.COLOR_BORDE, rect, 2, border_radius=6)
            ventana.blit(txt_btn, txt_btn.get_rect(center=rect.center))

        pygame.display.flip()
        reloj.tick(estilo.FPS)