import pygame,io,json,os,random,sys,requests
from PIL import Image, ImageSequence
import estilo,Personaje
from pokemons.PokePlantilla import Pokemon

#-------------------GESTOR_GUARDADO--------------------------------------------

def guardar_partida(jugador):
    """Convierte los datos complejos del objeto jugador a texto JSON."""
    lista_pokemons_serializada = []
    
    for poke in jugador.pokemons:

        lista_pokemons_serializada.append({
            "nombre": poke.nombre.lower() 
        })

    datos_a_guardar = {
        "billetera": jugador.billetera,
        "inventario": jugador.inventario,
        "ruta_spritesheet": jugador.ruta_spritesheet,
        "pokemons": lista_pokemons_serializada
    }
    
    with open("partida.json", "w") as archivo:
        json.dump(datos_a_guardar, archivo, indent=4)


def cargar_partida(ruta_defecto=None):
    
    if not os.path.exists("partida.json"):
        return None
        
    with open("partida.json", "r") as archivo:
        datos = json.load(archivo)
        
    ruta_skin = datos.get("ruta_spritesheet", ruta_defecto)
    
    
    jugador_cargado = Personaje.personaje(ruta_skin)
    jugador_cargado.billetera = datos.get("billetera", 100)
    jugador_cargado.inventario = datos.get("inventario", {"pocion": 0, "revivir": 0})
    
    
    datos_pokes = datos.get("pokemons", [])
    lista_objetos_pokemon = []
    
    for datos_poke in datos_pokes:
        nombre_pokemon = datos_poke["nombre"]
        
        try:
            nuevo_poke = Pokemon(id=nombre_pokemon, es_jugador=True)
            lista_objetos_pokemon.append(nuevo_poke)
        except Exception as e:
            print(f"Error al conectar con la API para cargar a {nombre_pokemon}: {e}")
        
    jugador_cargado.pokemons = lista_objetos_pokemon
    return jugador_cargado

#-------------------ARCHIVO_SPRITE_COMBATE--------------------------------------

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

def obtener_botones_segun_menu(menu, pokemon_obj, offset,jugador):
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
                if p == pokemon_obj:
                    info_txt += " *Activo*"
                
                idx_absoluto = indice_inicio + i
                botones_dinamicos[f"Pkm_{idx_absoluto}"] = (rect, (100, 100, 200), estilo.fuente_nombre.render(info_txt, True, (255, 255, 255)))
            
            if indice_inicio + 2 < len(jugador.pokemons):
                botones_dinamicos["Der"] = (pygame.Rect(1010, 625, 40, 40), (200, 200, 200), estilo.fuente_nombre.render(">", True, (0, 0, 0)))
                
        return botones_dinamicos

#----------------------------SONIDO---------------------------------------
def reproducir_musica(musica,bucle):

    nombre_archivo = f"Sonido/Musica/{musica}"

    try:
        pygame.mixer.music.load(nombre_archivo)

        #-1 significa bucle infinito, y 0 significa reproducir solo 1 vez.
        repeticiones = -1 if bucle else 0

        pygame.mixer.music.set_volume(0.2) #volumen se regula entre 0 y 1

        pygame.mixer.music.play(repeticiones)

    except pygame.error:
        print("error en archivo de audio")


def reproducir_sonido(sonido):
   
    nombre_archivo = f"Sonido/Efectos/{sonido}"  
    
    try:
        # 1. Cargamos el sonido en la memoria RAM para acceso instantáneo
        efecto = pygame.mixer.Sound(nombre_archivo)
        
        # 2. Regulamos su volumen (0.0 a 1.0)
        efecto.set_volume(0.6)
        
        # 3. Lo reproducimos. play() sin argumentos lo reproduce una sola vez
        efecto.play()
        
    except pygame.error:
        print(f"error en archivo de sonido: {nombre_archivo}")


#---------------------TIENDA----------------------
def mostrar_animacion_caja(pantalla, ruta_imagen,pokemon,columnas=4, filas=2):
    try:
        sheet = pygame.image.load(ruta_imagen).convert_alpha()
        fondo_caja = pygame.image.load("img/Tienda/fondo_cajas.png").convert()

    except pygame.error as e:
        print(f"Error al cargar la imagen {ruta_imagen}: {e}")
        return  # Si la imagen no existe, evita que el juego se rompa

    # Cálculo dinámico: divide el ancho total por 4 y el alto total por 2
    w = sheet.get_width() // columnas
    h = sheet.get_height() // filas
    
    # Recorte de los 8 frames de la cuadrícula
    frames = []
    for f in range(filas):
        for c in range(columnas):
            rect = pygame.Rect(c * w, f * h, w, h)
            frames.append(sheet.subsurface(rect))

    # Variables de control de la animación
    frame_actual = 0
    ultimo_cambio = pygame.time.get_ticks()
    velocidad = 200  # Tiempo en milisegundos entre frames (bájalo si quieres que vaya más rápido)
    esperando_enter = False
    
    reloj = pygame.time.Clock()
    reproduciendo = True

    # Bucle interno de la animación
    while reproduciendo:
        reloj.tick(60)
        ahora = pygame.time.get_ticks()
        
        # --- Captura de Eventos ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if evento.type == pygame.KEYDOWN:
                # Si está en el frame 5 (el destello con luces celestes) y presiona ENTER
                if esperando_enter and evento.key == pygame.K_RETURN:
                    esperando_enter = False
                    ultimo_cambio = ahora  # Reanuda el tiempo para pasar al frame 6

        # --- Lógica de la Línea de Tiempo ---
        if ahora - ultimo_cambio > velocidad:
            if not (frame_actual == 5 and esperando_enter):  # Si está pausado, no avanza
                if frame_actual < len(frames) - 1:
                    frame_actual += 1
                    ultimo_cambio = ahora
                    # El frame 5 (índice 5, es decir, el sexto frame) es el destello máximo
                    if frame_actual == 5: 
                        esperando_enter = True
                else:
                    reproduciendo = False  # Llegó al último frame (caja cerrada/reiniciada), termina

        
        if fondo_caja:
            pantalla.blit(fondo_caja, (0, 0))
        else:
            pantalla.fill((30, 30, 30))
        
        # Centrado automático en base al tamaño real del frame calculado
        x_centro = (pantalla.get_width() - w) // 2
        y_centro = (pantalla.get_height() - h) // 2 - 30
        pantalla.blit(frames[frame_actual], (x_centro, y_centro))
        
        # Letrero parpadeante/fijo durante el destello
        if esperando_enter:
            fuente = pygame.font.Font("tipografia/pokemon_font.ttf", 22)
            
            # 1. Renderizamos la primera línea (con el nombre del Pokémon)
            # NOTA: Pasale la variable 'nombre_p' a tu función si querés usarla acá
            linea1 = fuente.render(f"Te ha salido un {pokemon}!", True, (255, 255, 255))
            
            # 2. Renderizamos la segunda línea
            linea2 = fuente.render("Presiona ENTER para cerrar", True, (200, 200, 200)) # Un tono más grisáceo
            
            # Calculamos el centrado en X para cada una
            x_linea1 = (pantalla.get_width() - linea1.get_width()) // 2
            x_linea2 = (pantalla.get_width() - linea2.get_width()) // 2
            
            # Las dibujamos una debajo de la otra sumando píxeles a la 'y'
            y_base = y_centro + h + 20
            pantalla.blit(linea1, (x_linea1, y_base))
            pantalla.blit(linea2, (x_linea2, y_base + 28)) # 28 píxeles más abajo para el salto de línea
            
        pygame.display.flip()

#-----------------------COMBATES (LOGICA)----------------------------------------

def generar_equipo_rival(cantidad):
    """Genera una lista de objetos Pokemon aleatorios para el rival"""
    equipo_rival = []
    for _ in range(cantidad):
        id_aleatorio = random.randint(1, 151)
        
        equipo_rival.append(Pokemon(id_aleatorio, es_jugador=False))
    return equipo_rival

def procesar_turno_logico(pkmn_atacante, pkmn_defensor, indice_ataque):
    """Conecta la acción del atacante con la reacción del defensor"""
    ataque = pkmn_atacante.ataques[indice_ataque]
    
    # 1. El atacante nos dice su daño base
    daño_base = pkmn_atacante.calcular_daño_base(indice_ataque)
    
    # 2. El defensor procesa el daño usando sus stats y tipos
    daño_final, mult = pkmn_defensor.recibir_daño(daño_base, ataque["tipo"])
    
    return {
        "nombre_ataque": ataque["nombre"],
        "daño": daño_final,
        "multiplicador": mult,
        "debilitado": pkmn_defensor.vida_actual <= 0
    }

def aplicar_consecuencias_billetera(jugador, gano_jugador):
    if gano_jugador:
        jugador.billetera += 25
    else:
        jugador.billetera = max(0, jugador.billetera - 50)
        # Curamos a todos los pokemons del jugador usando su método propio
        for p in jugador.pokemons:
            p.curar()

