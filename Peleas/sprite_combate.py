import pygame
import os
import random
import io
import sys
from PIL import Image, ImageSequence
import estilo  

# Importamos las funciones de tu archivo de logica
from Peleas.logica_combate import procesar_turno_logico, generar_equipo_rival, aplicar_consecuencias_billetera

def batalla(ventana, jugador): 
    # 1. VALIDACION DEL INVENTARIO DEL JUGADOR
    if not hasattr(jugador, "pokemons") or not jugador.pokemons:
        print("[ERROR] El jugador no tiene Pokemon en su inventario para combatir.")
        return

    # Seleccionamos el primer Pokemon del jugador que tenga vida disponible
    mi_pokemon = next((p for p in jugador.pokemons if p.vida_actual > 0), jugador.pokemons[0])
    
    # 2. GENERACION DEL EQUIPO RIVAL SEGUN LA CANTIDAD DEL JUGADOR
    cantidad_rival = len(jugador.pokemons)
    equipo_rival = generar_equipo_rival(cantidad_rival)
    
    # Indice para saber que pokemon del rival esta activo actualmente
    idx_rival_activo = 0
    pokemon_rival = equipo_rival[idx_rival_activo]

    pygame.init()
    pygame.display.set_caption("Poke-Unsam - Batalla")
    reloj = pygame.time.Clock()
    fondo_combate = estilo.obtener_fondo_aleatorio()  

    # Funcion para convertir los bytes del GIF pre-descargado en superficies de Pygame
    def procesar_gif(gif_bytes, factor_escala=2.5):
        if not gif_bytes:
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
    texto_pantalla = f"Un {nombre_rival} salvaje aparecio! Que hara {nombre_mio}?"

    mensajes_acciones = {
        "Atacar": f"{nombre_mio} se prepara para atacar...",
        "Objetos": "Abriendo la mochila de objetos...",
        "Cambiar": "A que Pokemon quieres llamar?" 
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
            if offset > 0:
                botones_dinamicos["Izq"] = (pygame.Rect(560, 625, 40, 40), (200, 200, 200), estilo.fuente_nombre.render("<", True, (0, 0, 0)))
            
            indice_inicio = offset * 2
            for i, p in enumerate(jugador.pokemons[indice_inicio : indice_inicio + 2]):
                y_pos = 600 if i == 0 else 650
                rect = pygame.Rect(620, y_pos, 380, 40)
                
                info_txt = f"{p.nombre} (HP: {p.vida_actual}/{p.stats['vida_max']})"
                if p == mi_pokemon:
                    info_txt += " *Activo*"
                
                idx_absoluto = indice_inicio + i
                botones_dinamicos[f"Pkm_{idx_absoluto}"] = (rect, (100, 100, 200), estilo.fuente_nombre.render(info_txt, True, (255, 255, 255)))
            
            if indice_inicio + 2 < len(jugador.pokemons):
                botones_dinamicos["Der"] = (pygame.Rect(1010, 625, 40, 40), (200, 200, 200), estilo.fuente_nombre.render(">", True, (0, 0, 0)))
                
        return botones_dinamicos

    tamano_achicado = estilo.fuente_nombre.get_height() - 8
    fuente_texto_panel = pygame.font.Font(os.path.join(estilo.DIRECTORIO_BASE, "tipografia/pokemon_font.ttf"), tamano_achicado)
    
    MENU_ACTUAL = "PRINCIPAL" 
    OFFSET_POKEMONES = 0
    ejecutando = True
    batalla_terminada = False
    
    # Variables de control de turnos
    TURNO_RIVAL_PENDIENTE = False

    while ejecutando:
        mouse_pos = pygame.mouse.get_pos()
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if batalla_terminada:
                    ejecutando = False
                    break
                
                # FASE INTERMEDIA: Al hacer un clic pendiente, ataca el rival
                if TURNO_RIVAL_PENDIENTE:
                    idx_ataque_rival = random.randint(0, len(pokemon_rival.ataques) - 1)
                    res_rival = procesar_turno_logico(pokemon_rival, mi_pokemon, idx_ataque_rival)
                    
                    texto_pantalla = f"{nombre_rival} enemigo uso {res_rival['nombre_ataque']}! Hizo {res_rival['daño']} de daño."
                    TURNO_RIVAL_PENDIENTE = False 
                    
                    if res_rival["debilitado"]:
                        # Verificamos si al jugador le queda algun otro Pokemon vivo en su lista
                        pokemon_vivo = next((p for p in jugador.pokemons if p.vida_actual > 0), None)
                        if pokemon_vivo is None:
                            texto_pantalla = f"{nombre_mio} se debilito! No te quedan Pokemon... Perdiste el combate. (Clic para salir)"
                            aplicar_consecuencias_billetera(jugador, gano_jugador=False)
                            batalla_terminada = True
                        else:
                            texto_pantalla = f"{nombre_mio} se debilito! Elige otro Pokemon usando el boton Cambiar."
                            # Forzamos a que el jugador tenga que entrar a cambiar de pokemon
                            MENU_ACTUAL = "PRINCIPAL"
                    continue

                if MENU_ACTUAL == "PRINCIPAL":
                    btns = botones
                else:
                    btns = obtener_botones_segun_menu(MENU_ACTUAL, mi_pokemon, OFFSET_POKEMONES)
                
                for nom, (rect, _, _) in btns.items():
                    if rect.collidepoint(mouse_pos):
                        
                        if MENU_ACTUAL == "PRINCIPAL":
                            if nom == "Atacar": 
                                if mi_pokemon.vida_actual <= 0:
                                    texto_pantalla = f"{nombre_mio} esta debilitado! Debes cambiar de Pokemon."
                                else:
                                    MENU_ACTUAL = "ATAQUES"
                            elif nom == "Objetos": 
                                MENU_ACTUAL = "OBJETOS"
                            elif nom == "Cambiar": 
                                MENU_ACTUAL = "POKEMONES"
                                texto_pantalla = mensajes_acciones["Cambiar"]
                            elif nom in mensajes_acciones: 
                                texto_pantalla = mensajes_acciones[nom]
                        
                        else:
                            if nom == "Izq": 
                                OFFSET_POKEMONES = max(0, OFFSET_POKEMONES - 1)
                            elif nom == "Der": 
                                if (OFFSET_POKEMONES + 1) * 2 < len(jugador.pokemons):
                                    OFFSET_POKEMONES += 1
                            else:
                                if "Ataque" in nom:
                                    idx_ataque = int(nom[-1]) - 1
                                    res_jugador = procesar_turno_logico(mi_pokemon, pokemon_rival, idx_ataque)
                                    
                                    if res_jugador["debilitado"]:
                                        # ¡Derrotamos al rival activo! Evaluamos si tiene mas en su equipo
                                        idx_rival_activo += 1
                                        if idx_rival_activo < len(equipo_rival):
                                            # Traemos al siguiente contrincante
                                            pokemon_rival = equipo_rival[idx_rival_activo]
                                            nombre_rival = pokemon_rival.nombre
                                            
                                            # Cargamos los nuevos sprites/frames del rival entrante
                                            frames["rival"] = procesar_gif(pokemon_rival.gif_bytes, factor_escala=2.2)
                                            idx["rival"] = 0
                                            
                                            texto_pantalla = f"{nombre_mio} uso {res_jugador['nombre_ataque']}! El enemigo se debilito. ¡El rival envia a {nombre_rival}! (Clic para continuar)"
                                            TURNO_RIVAL_PENDIENTE = True
                                        else:
                                            # Si ya no quedan mas rivales en su lista, ganamos del todo
                                            texto_pantalla = f"{nombre_mio} uso {res_jugador['nombre_ataque']}! Derrotaste a todo el equipo rival! (Clic para salir)"
                                            aplicar_consecuencias_billetera(jugador, gano_jugador=True)
                                            batalla_terminada = True
                                    else:
                                        texto_pantalla = f"{nombre_mio} uso {res_jugador['nombre_ataque']}! Hizo {res_jugador['daño']} de daño. (Clic para continuar)"
                                        TURNO_RIVAL_PENDIENTE = True
                                        
                                elif "Pkm_" in nom:
                                    idx_elegido = int(nom.split("_")[1])
                                    pokemon_seleccionado = jugador.pokemons[idx_elegido]
                                    
                                    if pokemon_seleccionado == mi_pokemon:
                                        texto_pantalla = f"{pokemon_seleccionado.nombre} ya esta peleando!"
                                        continue
                                    elif pokemon_seleccionado.vida_actual <= 0:
                                        texto_pantalla = f"{pokemon_seleccionado.nombre} esta debilitado!"
                                        continue
                                    else:
                                        mi_pokemon = pokemon_seleccionado
                                        nombre_mio = mi_pokemon.nombre
                                        
                                        frames["mio"] = procesar_gif(mi_pokemon.gif_bytes, factor_escala=3.0)
                                        idx["mio"] = 0
                                        
                                        texto_pantalla = f"Sali {nombre_mio}! El rival aprovecha tu cambio para atacar. (Clic para continuar)"
                                        TURNO_RIVAL_PENDIENTE = True
                                
                                MENU_ACTUAL = "PRINCIPAL"
                            break 
                            
        # Animacion de frames de los GIFs
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

        # Render de panel de control inferior e informacion de HP
        pygame.draw.rect(ventana, estilo.COLOR_PANEL, (0, estilo.ALTO_COMBATE, estilo.ANCHO_VENTANA, estilo.ALTO_PANEL))
        
        info_vida = f"HP: {mi_pokemon.vida_actual}/{mi_pokemon.stats['vida_max']} vs Rival ({idx_rival_activo + 1}/{len(equipo_rival)}): {pokemon_rival.vida_actual}/{pokemon_rival.stats['vida_max']}"
        
        txt_linea1 = fuente_texto_panel.render(texto_pantalla, True, estilo.COLOR_TEXTO)
        ventana.blit(txt_linea1, (30, estilo.ALTO_COMBATE + 32))
        
        txt_linea2 = fuente_texto_panel.render(info_vida, True, (248, 112, 112))
        ventana.blit(txt_linea2, (30, estilo.ALTO_COMBATE + 72))

        # Dibujamos botones interactivos si corresponde
        if not batalla_terminada and not TURNO_RIVAL_PENDIENTE:
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

    return "MUNDO_LIBRE"
