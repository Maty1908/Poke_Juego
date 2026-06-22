
import pygame,os,random,io,sys
import estilo  
from funciones import procesar_gif,obtener_botones_segun_menu

from funciones import procesar_turno_logico, generar_equipo_rival, aplicar_consecuencias_billetera

def batalla(ventana, jugador): 
    
    if not hasattr(jugador, "pokemons") or not jugador.pokemons:
        print("[ERROR] El jugador no tiene Pokemon en su inventario para combatir.")
        return

    mi_pokemon = next((p for p in jugador.pokemons if p.vida_actual > 0), jugador.pokemons[0])
    
    
    cantidad_rival = len(jugador.pokemons)
    equipo_rival = generar_equipo_rival(cantidad_rival)
    
    idx_rival_activo = 0
    pokemon_rival = equipo_rival[idx_rival_activo]

    pygame.init()
    pygame.display.set_caption("Poke-Unsam - Batalla")
    reloj = pygame.time.Clock()
    fondo_combate = estilo.obtener_fondo_aleatorio()  


    pos_mia, pos_rival, tam_base = estilo.escenario_actual

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

    

    tamaño_achicado = estilo.fuente_nombre.get_height() - 8
    fuente_texto_panel = pygame.font.Font(os.path.join(estilo.DIRECTORIO_BASE, "tipografia/pokemon_font.ttf"), tamaño_achicado)
    
    MENU_ACTUAL = "PRINCIPAL" 
    OFFSET_POKEMONES = 0
    ejecutando = True
    batalla_terminada = False
    
    TURNO_RIVAL_PENDIENTE = False

    #----------------------BUCLE BATALLA------------------------------
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
                
                if TURNO_RIVAL_PENDIENTE:
                    idx_ataque_rival = random.randint(0, len(pokemon_rival.ataques) - 1)
                    res_rival = procesar_turno_logico(pokemon_rival, mi_pokemon, idx_ataque_rival)
                    
                    texto_pantalla = f"{nombre_rival} enemigo uso {res_rival['nombre_ataque']}! Hizo {res_rival['daño']} de daño."
                    TURNO_RIVAL_PENDIENTE = False 
                    
                    if res_rival["debilitado"]:
                        pokemon_vivo = next((p for p in jugador.pokemons if p.vida_actual > 0), None)
                        if pokemon_vivo is None:
                            texto_pantalla = f"{nombre_mio} se debilito! No te quedan Pokemon... Perdiste el combate. (Clic para salir)"
                            aplicar_consecuencias_billetera(jugador, gano_jugador=False)
                            batalla_terminada = True
                        else:
                            texto_pantalla = f"{nombre_mio} se debilito! Elige otro Pokemon usando el boton Cambiar."
                            MENU_ACTUAL = "PRINCIPAL"
                    continue

                if MENU_ACTUAL == "PRINCIPAL":
                    btns = botones
                else:
                    btns = obtener_botones_segun_menu(MENU_ACTUAL, mi_pokemon, OFFSET_POKEMONES,jugador)
                
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
ç                                        idx_rival_activo += 1
                                        if idx_rival_activo < len(equipo_rival):
                                            pokemon_rival = equipo_rival[idx_rival_activo]
                                            nombre_rival = pokemon_rival.nombre
                                            
                                            frames["rival"] = procesar_gif(pokemon_rival.gif_bytes, factor_escala=2.2)
                                            idx["rival"] = 0
                                            
                                            texto_pantalla = f"{nombre_mio} uso {res_jugador['nombre_ataque']}! El enemigo se debilito. ¡El rival envia a {nombre_rival}! (Clic para continuar)"
                                            TURNO_RIVAL_PENDIENTE = True
                                        else:
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
                            
        if pygame.time.get_ticks() - ultimo_cambio > 90:
            for k in idx: 
                if k == "rival" and batalla_terminada: continue
                idx[k] = (idx[k] + 1) % len(frames[k])
            ultimo_cambio = pygame.time.get_ticks()

        ventana.blit(fondo_combate, (0, 0))
        for k, (x_din, suelo) in [("mio", pos_mia), ("rival", pos_rival)]:
            if k == "rival" and batalla_terminada: pass
            fr = frames[k][idx[k]]
            ventana.blit(fr, (x_din - (fr.get_width() // 2), suelo - fr.get_height()))

        pygame.draw.rect(ventana, estilo.COLOR_PANEL, (0, estilo.ALTO_COMBATE, estilo.ANCHO_VENTANA, estilo.ALTO_PANEL))
        
        info_vida = f"HP: {mi_pokemon.vida_actual}/{mi_pokemon.stats['vida_max']} vs Rival ({idx_rival_activo + 1}/{len(equipo_rival)}): {pokemon_rival.vida_actual}/{pokemon_rival.stats['vida_max']}"
        
        txt_linea1 = fuente_texto_panel.render(texto_pantalla, True, estilo.COLOR_TEXTO)
        ventana.blit(txt_linea1, (30, estilo.ALTO_COMBATE + 32))
        
        txt_linea2 = fuente_texto_panel.render(info_vida, True, (248, 112, 112))
        ventana.blit(txt_linea2, (30, estilo.ALTO_COMBATE + 72))

        if not batalla_terminada and not TURNO_RIVAL_PENDIENTE:
            if MENU_ACTUAL == "PRINCIPAL":
                botones_a_dibujar = botones
            else:
                botones_a_dibujar = obtener_botones_segun_menu(MENU_ACTUAL, mi_pokemon, OFFSET_POKEMONES,jugador)
            
            for nombre, (rect, color, txt_btn) in botones_a_dibujar.items():
                color_f = tuple(min(c + 35, 255) for c in color) if rect.collidepoint(mouse_pos) else color
                pygame.draw.rect(ventana, color_f, rect, border_radius=6)
                pygame.draw.rect(ventana, estilo.COLOR_BORDE, rect, 2, border_radius=6)
                ventana.blit(txt_btn, txt_btn.get_rect(center=rect.center))

        pygame.display.flip()
        reloj.tick(estilo.FPS)

    return "MUNDO_LIBRE"
