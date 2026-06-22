import pygame
import os
import random
import io
import sys
from PIL import Image, ImageSequence
import estilo  

# Importamos las funciones de tu archivo de lógica
from Peleas.logica_combate import procesar_turno_logico, generar_equipo_rival, aplicar_consecuencias_billetera

def batalla(ventana, jugador): 
    # 1. VALIDACIÓN DEL INVENTARIO DEL JUGADOR
    if not hasattr(jugador, "pokemons") or not jugador.pokemons:
        print("[ERROR] El jugador no tiene Pokémon en su inventario para combatir.")
        return

    # Seleccionamos el primer Pokémon del jugador que tenga vida disponible
    mi_pokemon = next((p for p in jugador.pokemons if p.vida_actual > 0), jugador.pokemons[0])
    
    # 2. GENERACIÓN DEL EQUIPO RIVAL SEGÚN LA CANTIDAD DEL JUGADOR
    cantidad_rival = len(jugador.pokemons)
    equipo_rival = generar_equipo_rival(cantidad_rival)
    pokemon_rival = equipo_rival[0] # Tomamos el primero para empezar el combate

    pygame.init()
    pygame.display.set_caption("Poke-Unsam - Batalla")
    reloj = pygame.time.Clock()
    fondo_combate = estilo.obtener_fondo_aleatorio()  

    # Función para convertir los bytes del GIF pre-descargado en superficies de Pygame
    def procesar_gif(gif_bytes, factor_escala=2.5):
        if not gif_bytes:
            # Superficie vacía de respaldo por si falló la descarga en la API
            sup_vacia = pygame.Surface((50, 50), pygame.SRCALPHA)
            return [sup_vacia]
            
        gif_pil = Image.open(io.BytesIO(gif_bytes))
        lista_frames = []
        for frame in ImageSequence.Iterator(gif_pil):
            frame_rgba = frame.convert("RGBA")
            sup = pygame.image.frombytes(frame_rgba.tobytes(), frame_rgba.size, "RGBA").convert_alpha()
            w, h = frame_rgba.size
            frame_escalado = pygame.transform.scale(sup, (int(w * factor_escala), int(h * factor_escala))).convert_alpha()
            lista_frames.append(frame_escalado)
        return lista_frames

    pos_mia, pos_rival, tam_base = estilo.escenario_actual

    # Procesamos los frames directamente usando el atributo .gif_bytes de cada objeto
    frames = {
        "mio": procesar_gif(mi_pokemon.gif_bytes, factor_escala=3.0),
        "rival": procesar_gif(pokemon_rival.gif_bytes, factor_escala=2.2)
    }

    idx = {"mio": 0, "rival": 0}
    ultimo_cambio = pygame.time.get_ticks()

    botones = {nom: (r, c, estilo.fuente_nombre.render(nom, True, (255, 255, 255)).convert_alpha()) 
                for nom, (r, c) in estilo.DATOS_BOTONES.items()}

    nombre_mio = mi_pokemon.nombre
    nombre_rival = pokemon_rival.nombre
    texto_pantalla = f"¡Un {nombre_rival} salvaje apareció! ¿Qué hará {nombre_mio}?"

    mensajes_acciones = {
        "Atacar": f"{nombre_mio} se prepara para atacar...",
        "Objetos": "Abriendo la mochila de objetos...",
        "Cambiar": "¿A qué Pokémon quieres llamar?" 
    }

    def obtener_botones_segun_menu(menu, pokemon_obj, offset):
        botones_dinamicos = {}
        if menu == "ATAQUES":
            posiciones = [(600, 600), (810, 600), (600, 650), (810, 650)]
            for i, atk in enumerate(pokemon_obj.ataques[:4]):
                rect = pygame.Rect(posiciones[i][0], posiciones[i][1], 200, 40)
                botones_dinamicos[f"Ataque{i+1}"] = (rect, (248, 112, 112), estilo.fuente_nombre.render(atk["nombre"], True, (255, 255, 255)))
        elif menu == "OBJETOS":
            botones_dinamicos["Pocion"] = (pygame.Rect(600, 600, 400, 40), (120, 200, 80), estilo.fuente_nombre.render("Pocion", True, (255, 255, 255)))
            botones_dinamicos["Revivir"] = (pygame.Rect(600, 650, 400, 40), (120, 200, 80), estilo.fuente_nombre.render("Revivir", True, (255, 255, 255)))
        elif menu == "POKEMONES":
            botones_dinamicos["Izq"] = (pygame.Rect(550, 625, 40, 40), (200, 200, 200), estilo.fuente_nombre.render("<", True, (0, 0, 0)))
            botones_dinamicos["Der"] = (pygame.Rect(1020, 625, 40, 40), (200, 200, 200), estilo.fuente_nombre.render(">", True, (0, 0, 0)))
            
            # Mostramos el inventario real del jugador reflejado en botones
            for i, p in enumerate(jugador.pokemons[offset*2 : (offset*2)+2]):
                rect = pygame.Rect(600 if i==0 else 810, 600, 200, 40)
                botones_dinamicos[f"Pkm{i+1}"] = (rect, (100, 100, 200), estilo.fuente_nombre.render(p.nombre, True, (255, 255, 255)))
        return botones_dinamicos

    MENU_ACTUAL = "PRINCIPAL" 
    OFFSET_POKEMONES = 0
    ejecutando = True
    batalla_terminada = False

    while ejecutando:
        mouse_pos = pygame.mouse.get_pos()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                ejecutando = False
                sys.exit()
                
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                # Si la batalla terminó, el siguiente clic te saca de la pantalla de combate
                if batalla_terminada:
                    ejecutando = False
                    break
                
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
                                if "Ataque" in nom:
                                    idx_ataque = int(nom[-1]) - 1
                                    
                                    # Ejecutamos tu lógica de combate real vinculando los objetos
                                    res = procesar_turno_logico(mi_pokemon, pokemon_rival, idx_ataque)
                                    texto_pantalla = f"{nombre_mio} usó {res['nombre_ataque']}! Hizo {res['daño']} de daño."
                                    
                                    # Si el rival cae derrotado
                                    if res["debilitado"]:
                                        texto_pantalla = f"¡{nombre_rival} enemigo se debilitó! ¡Ganaste el combate! (Clic para continuar)"
                                        # Aplicamos los cambios financieros en tu objeto jugador
                                        aplicar_consecuencias_billetera(jugador, gano_jugador=True)
                                        batalla_terminada = True
                                else:
                                    texto_pantalla = f"Elegiste: {nom}"
                                
                                MENU_ACTUAL = "PRINCIPAL"
                            
        # Animación de frames de los GIFs
        if pygame.time.get_ticks() - ultimo_cambio > 90:
            for k in idx: 
                if k == "rival" and batalla_terminada: continue
                idx[k] = (idx[k] + 1) % len(frames[k])
            ultimo_cambio = pygame.time.get_ticks()

        # Render de fondo y sprites
        ventana.blit(fondo_combate, (0, 0))
        for k, (x_din, suelo) in [("mio", pos_mia), ("rival", pos_rival)]:
            if k == "rival" and batalla_terminada: pass
            fr = frames[k][idx[k]]
            ventana.blit(fr, (x_din - (fr.get_width() // 2), suelo - fr.get_height()))

        # Render de panel de control inferior e información de HP en vivo
        pygame.draw.rect(ventana, estilo.COLOR_PANEL, (0, estilo.ALTO_COMBATE, estilo.ANCHO_VENTANA, estilo.ALTO_PANEL))
        info_vida = f"  [{mi_pokemon.vida_actual}/{mi_pokemon.stats['vida_max']} HP] vs Rival [{pokemon_rival.vida_actual}/{pokemon_rival.stats['vida_max']} HP]"
        ventana.blit(estilo.fuente_nombre.render(texto_pantalla + info_vida, True, estilo.COLOR_TEXTO), (30, estilo.ALTO_COMBATE + 45))

        # Dibujamos botones interactivos si el combate no ha finalizado
        if not batalla_terminada:
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
