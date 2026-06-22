import pygame
import sys


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
