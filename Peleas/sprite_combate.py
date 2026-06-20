import pygame,os,sys,random,requests,io
from PIL import Image, ImageSequence
import estilo  


from Peleas.logica_combate import (
    inicializar_equipo_combate,
    generar_equipo_rival,
    procesar_turno_logico, # <--- Cambiado a procesar_turno_logico
    aplicar_consecuencias_billetera
)

def procesar_gif(gif_pil, factor_escala=2.5):
    lista_frames = []
    for frame in ImageSequence.Iterator(gif_pil):
        frame_rgba = frame.convert("RGBA")
        sup = pygame.image.frombytes(frame_rgba.tobytes(), frame_rgba.size, "RGBA").convert_alpha()
        w, h = frame_rgba.size
        frame_escalado = pygame.transform.scale(sup, (int(w * factor_escala), int(h * factor_escala)))
        lista_frames.append(frame_escalado)
    return lista_frames

def descargar_asset_pokemon(pokemon_id, espalda=False):
    vista = "back" if espalda else "front"
    url_gif = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/{vista}/{pokemon_id}.gif"
    try:
        res = requests.get(url_gif)
        if res.status_code == 200:
            return Image.open(io.BytesIO(res.content))
    except:
        pass
    url_static = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png"
    res = requests.get(url_static)
    return Image.open(io.BytesIO(res.content))


def batalla(ventana, jugador):
    pygame.display.set_caption("Poke-Unsam - Batalla")
    reloj = pygame.time.Clock()
    
    equipo_j = inicializar_equipo_combate(jugador.pokemons)
    equipo_r = generar_equipo_rival(len(equipo_j))
    
    idx_j = 0
    idx_r = 0
    
    turno_jugador = True
    texto_banner = "¡Un entrenador quiere pelear!"
    bucle_activo = True
    
    fondo_combate = pygame.image.load(os.path.join(estilo.DIRECTORIO_BASE, "img/Fondo_peleas/fondo1.png")).convert()
    fondo_combate = pygame.transform.scale(fondo_combate, (estilo.ANCHO_VENTANA, estilo.ALTO_COMBATE))

    pkmn_j = equipo_j[idx_j]
    pkmn_r = equipo_r[idx_r]
    
    gif_j_pil = descargar_asset_pokemon(pkmn_j["id"], espalda=True)
    gif_r_pil = descargar_asset_pokemon(pkmn_r["id"], espalda=False)
    
    frames_j = procesar_gif(gif_j_pil, factor_escala=3.0)
    frames_r = procesar_gif(gif_r_pil, factor_escala=2.5)
    
    f_idx_j, f_idx_r = 0, 0

    rect_pos_j = pygame.Rect(180, 260, 200, 200)
    rect_pos_r = pygame.Rect(680, 100, 180, 180)

    while bucle_activo:
        mouse_pos = pygame.mouse.get_pos()
        
        pkmn_j = equipo_j[idx_j]
        pkmn_r = equipo_r[idx_r]

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if turno_jugador:
                    for i in range(len(pkmn_j["ataques"])):
                        x_btn = 50 + (i % 2) * 260
                        y_btn = estilo.ALTO_COMBATE + 20 + (i // 2) * 45
                        rect_boton = pygame.Rect(x_btn, y_btn, 230, 35)
                        
                        if rect_boton.collidepoint(mouse_pos):
                           
                            res_turno = procesar_turno_logico(pkmn_j, pkmn_r, i)
                            texto_banner = f"{pkmn_j['nombre']} usó {res_turno['nombre_ataque']} (-{res_turno['daño']})"
                            
                            if res_turno["debilitado"]:
                                idx_r += 1
                                if idx_r >= len(equipo_r):
                                    aplicar_consecuencias_billetera(jugador, gano_jugador=True)
                                    bucle_activo = False
                                    return "MUNDO_LIBRE"
                                else:
                                    pkmn_r = equipo_r[idx_r]
                                    gif_r_pil = descargar_asset_pokemon(pkmn_r["id"], espalda=False)
                                    frames_r = procesar_gif(gif_r_pil, factor_escala=2.5)
                                    f_idx_r = 0
                                    texto_banner = f"¡El rival envió a {pkmn_r['nombre']}!"
                            
                            turno_jugador = False

        if not turno_jugador and bucle_activo:
            pygame.time.delay(1200)
            res_rival = procesar_turno_logico(pkmn_r, pkmn_j, 0)
            texto_banner = f"{pkmn_r['nombre']} rival usó {res_rival['nombre_ataque']} (-{res_rival['daño']})"
            
            if res_rival["debilitado"]:
                idx_j += 1
                if idx_j >= len(equipo_j):
                    aplicar_consecuencias_billetera(jugador, gano_jugador=False)
                    bucle_activo = False
                    return "MUNDO_LIBRE"
                else:
                    pkmn_j = equipo_j[idx_j]
                    gif_j_pil = descargar_asset_pokemon(pkmn_j["id"], espalda=True)
                    frames_j = procesar_gif(gif_j_pil, factor_escala=3.0)
                    f_idx_j = 0
                    texto_banner = f"¡Adelante {pkmn_j['nombre']}!"
                    
            turno_jugador = True

        # --- RENDERIZADO ---
        ventana.blit(fondo_combate, (0, 0))
        
        if frames_j:
            f_idx_j = (f_idx_j + 1) % len(frames_j)
            ventana.blit(frames_j[f_idx_j], rect_pos_j.topleft)
        if frames_r:
            f_idx_r = (f_idx_r + 1) % len(frames_r)
            ventana.blit(frames_r[f_idx_r], rect_pos_r.topleft)

        pygame.draw.rect(ventana, estilo.COLOR_PANEL, (0, estilo.ALTO_COMBATE, estilo.ANCHO_VENTANA, estilo.ALTO_PANEL))
        pygame.draw.rect(ventana, estilo.COLOR_BORDE, (0, estilo.ALTO_COMBATE, estilo.ANCHO_VENTANA, estilo.ALTO_PANEL), 3)

        lbl_j = estilo.fuente_nombre.render(f"{pkmn_j['nombre']}", True, estilo.COLOR_TEXTO)
        ventana.blit(lbl_j, (50, 360))
        pct_j = pkmn_j["vida_actual"] / pkmn_j["vida_max"]
        pygame.draw.rect(ventana, (200, 50, 50), (50, 390, 150, 12))
        pygame.draw.rect(ventana, (50, 200, 50), (50, 390, int(150 * pct_j), 12))

        lbl_r = estilo.fuente_nombre.render(f"{pkmn_r['nombre']}", True, estilo.COLOR_TEXTO)
        ventana.blit(lbl_r, (750, 100))
        pct_r = pkmn_r["vida_actual"] / pkmn_r["vida_max"]
        pygame.draw.rect(ventana, (200, 50, 50), (750, 130, 150, 12))
        pygame.draw.rect(ventana, (50, 200, 50), (750, 130, int(150 * pct_r), 12))

        for i, atq in enumerate(pkmn_j["ataques"][:4]):
            x_btn = 50 + (i % 2) * 260
            y_btn = estilo.ALTO_COMBATE + 20 + (i // 2) * 45
            color_btn = (100, 149, 237) if turno_jugador else (180, 180, 180)
            pygame.draw.rect(ventana, color_btn, (x_btn, y_btn, 230, 35), border_radius=6)
            txt_atq = estilo.fuente_stats.render(atq["nombre"], True, (255, 255, 255))
            ventana.blit(txt_atq, (x_btn + 15, y_btn + 8))

        lbl_info = estilo.fuente_stats.render(texto_banner, True, estilo.COLOR_TEXTO)
        ventana.blit(lbl_info, (600, estilo.ALTO_COMBATE + 45))

        # Tooltips hover de stats
        rects_pkmn = {"mio": rect_pos_j, "rival": rect_pos_r}
        pkmn_hover = "mio" if rects_pkmn["mio"].collidepoint(mouse_pos) else "rival" if rects_pkmn["rival"].collidepoint(mouse_pos) else None
        if pkmn_hover:
            p_data = pkmn_j if pkmn_hover == "mio" else pkmn_r
            w_c, h_c = 170, 115
            cx = mouse_pos[0] + 15 if mouse_pos[0] + 15 + w_c < estilo.ANCHO_VENTANA else mouse_pos[0] - w_c - 15
            cy = mouse_pos[1] + 15 if mouse_pos[1] + 15 + h_c < estilo.ALTO_COMBATE else mouse_pos[1] - h_c - 15
            
            sup_stats = pygame.Surface((w_c, h_c), pygame.SRCALPHA)
            sup_stats.fill(estilo.COLOR_FONDO_TOOLTIP)
            
            stats_a_mostrar = [
                f"HP: {p_data['vida_actual']}/{p_data['vida_max']}",
                f"ATK: {p_data['ataque']}",
                f"DEF: {p_data['defense']}",
                f"SPD: {p_data['speed']}"
            ]
            for idx, text in enumerate(stats_a_mostrar):
                t_surface = estilo.fuente_stats.render(text, True, (255, 255, 255))
                sup_stats.blit(t_surface, (10, 8 + idx * 25))
            ventana.blit(sup_stats, (cx, cy))

        pygame.display.update()
        reloj.tick(estilo.FPS)

    return "MUNDO_LIBRE"