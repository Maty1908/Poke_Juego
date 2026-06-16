import pygame,os,sys



def menu_inicial(ventana,personaje_elegido):

    pygame.display.set_caption("Poke-Unsam - Menu")

    # ---------------- FONDO ----------------
    ANCHO = 1064
    ALTO = 704

    fondo = pygame.image.load("img/Menu/campus_juego.png")

    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

    # ---------------- FUENTES ----------------

    RUTA_FUENTE = "tipografia/PressStart2P.ttf"

    # Opciones del menú
    fuente = pygame.font.Font(RUTA_FUENTE,22)

    # SOLO para el título
    fuente_titulo = pygame.font.Font(RUTA_FUENTE,97)

    # Para Juego, Tienda y Gracias
    fuente_ventanas = pygame.font.Font(RUTA_FUENTE,27)

    # ---------------- ESTADO ACTUAL ----------------
    estado = "MENU"

    # ---------------- OPCIONES ----------------
    opciones = ["Comenzar Juego", "Tienda", "Gracias", "Salir"]

    # Lista de botones
    botones = []

    # Reloj
    reloj = pygame.time.Clock()

    while True:

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Click del mouse
            if evento.type == pygame.MOUSEBUTTONDOWN:

                if estado == "MENU":

                    x_mouse, y_mouse = pygame.mouse.get_pos()

                    for i, boton in enumerate(botones):

                        if boton.collidepoint(x_mouse, y_mouse):

                            if opciones[i] == "Comenzar Juego":
                                estado = "SELECCION"
                                return estado

                            elif opciones[i] == "Tienda":
                                estado = "TIENDA"
                                return estado

                            elif opciones[i] == "Gracias":
                                estado = "GRACIAS"
                                return estado

                            elif opciones[i] == "Salir":
                                pygame.quit()
                                sys.exit()

            # ESC para volver al menú
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    estado = "MENU"

        # ---------------- MENÚ ----------------
        if estado == "MENU":

            ventana.blit(fondo, (0, 0))

            # Oscurecer el fondo
            capa = pygame.Surface((ANCHO, ALTO))
            capa.set_alpha(80)
            capa.fill((0, 0, 0))
            ventana.blit(capa, (0, 0))

            # Sombra del título
            sombra = fuente_titulo.render("Poke-Unsam",True,(0, 0, 0))

            ventana.blit(sombra,(ANCHO // 2 - sombra.get_width() // 2 + 4,108))

            # Título principal
            titulo = fuente_titulo.render("Poke-Unsam",True,(0, 100, 255))

            ventana.blit(titulo,(ANCHO // 2 - titulo.get_width() // 2,100))

            botones = []

            for i, opcion in enumerate(opciones):

                x = ANCHO // 2 - 200
                y = 280 + i * 125

                rect = pygame.Rect(x,y,350,50)

                # Resaltar botón con el mouse
                if rect.collidepoint(pygame.mouse.get_pos()):

                    pygame.draw.rect(ventana,(255, 220, 0),rect,border_radius=15)

                    color_texto = (0, 0, 0)

                else:

                    pygame.draw.rect(ventana,(0, 0, 0),rect,border_radius=15)

                    color_texto = (255, 255, 255)

                texto = fuente.render(opcion,True,color_texto)

                ventana.blit(texto,(rect.centerx - texto.get_width() // 2,rect.centery - texto.get_height() // 2))

                botones.append(rect)

        # ---------------- JUEGO ----------------
        elif estado == "juego":

            ventana.fill((0, 0, 0))

            texto = fuente_ventanas.render("Aca debera estar: Juego",True,(255, 255, 255))

            ventana.blit(texto,(ANCHO // 2 - texto.get_width() // 2,ALTO // 2 - texto.get_height() // 2))

        # ---------------- TIENDA ----------------
        elif estado == "tienda":

            ventana.fill((0, 0, 0))

            texto = fuente_ventanas.render("Aca debera estar: Tienda",True,(255, 255, 255))

            ventana.blit(texto,(ANCHO // 2 - texto.get_width() // 2,ALTO // 2 - texto.get_height() // 2))

        # ---------------- GRACIAS ----------------
        elif estado == "gracias":

            ventana.fill((0, 0, 0))

            texto = fuente_ventanas.render("Aca debera estar: Gracias",True,(255, 255, 255))

            ventana.blit(texto,(ANCHO // 2 - texto.get_width() // 2,ALTO // 2 - texto.get_height() // 2))

        pygame.display.update()
        reloj.tick(60)

