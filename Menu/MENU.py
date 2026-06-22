import pygame,os,sys
import estilo

def menu_inicial(ventana):

    pygame.display.set_caption("Poke-Unsam - Menu")

    # ---------------- FONDO ----------------
    fondo = pygame.image.load("img/Menu/campus_juego.png")

    fondo = pygame.transform.scale(fondo, (estilo.ANCHO_VENTANA, estilo.ALTO_VENTANA))

    # ---------------- FUENTES ----------------

    RUTA_FUENTE = "tipografia/PressStart2P.ttf"
    fuente = pygame.font.Font(RUTA_FUENTE,22)
    fuente_titulo = pygame.font.Font(RUTA_FUENTE,97)
    fuente_ventanas = pygame.font.Font(RUTA_FUENTE,13)

    # ---------------- ESTADO ACTUAL ----------------
    estado = "MENU"

    # ---------------- OPCIONES ----------------
    opciones = ["Comenzar Juego", "Continuar Partida", "Gracias", "Salir"]
    botones = []
    reloj = pygame.time.Clock()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1: 
                    if estado == "MENU":
                        x_mouse, y_mouse = pygame.mouse.get_pos()
                        for i, boton in enumerate(botones):
                            if boton.collidepoint(x_mouse, y_mouse):
                                if opciones[i] == "Comenzar Juego":
                                    estado = "SELECCION"
                                    return estado
                                elif opciones[i] == "Continuar Partida":
                                    if os.path.exists("partida.json"): 
                                        estado = "CONTINUAR"
                                        return estado 
                                    else:
                                        estado = "SIN_PARTIDA"
                                elif opciones[i] == "Gracias":
                                    estado = "GRACIAS"
                                elif opciones[i] == "Salir":
                                    pygame.quit()
                                    sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    estado = "MENU"
        # ---------------- MENÚ ----------------
        
        if estado == "MENU":
            ventana.blit(fondo, (0, 0))
            capa = pygame.Surface((estilo.ANCHO_VENTANA,estilo.ALTO_VENTANA))
            capa.set_alpha(80)
            capa.fill((0, 0, 0))
            ventana.blit(capa, (0, 0))
            sombra = fuente_titulo.render("Poke-Unsam",True,(0, 0, 0))
            ventana.blit(sombra,(estilo.ANCHO_VENTANA // 2 - sombra.get_width() // 2 + 4,108))
            titulo = fuente_titulo.render("Poke-Unsam",True,(255, 255, 255))
            ventana.blit(titulo,(estilo.ANCHO_VENTANA // 2 - titulo.get_width() // 2,100))
            botones = []
            for i, opcion in enumerate(opciones):
                x = estilo.ANCHO_VENTANA // 2 - 200
                y = 280 + i * 125
                rect = pygame.Rect(x,y,350,50)
                if rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(ventana,(255, 220, 0),rect,border_radius=15)
                    color_texto = (0, 0, 0)
                else:
                    pygame.draw.rect(ventana,(0, 0, 0),rect,border_radius=15)
                    color_texto = (255, 255, 255)
                texto = fuente.render(opcion,True,color_texto)
                ventana.blit(texto,(rect.centerx - texto.get_width() // 2,rect.centery - texto.get_height() // 2))
                botones.append(rect)
                
        # ---------------- GRACIAS ----------------
        elif estado == "GRACIAS":
            ventana.fill((30, 30, 30))
            texto = fuente_ventanas.render("¡Muchas gracias profes por este cuatrimestre, esperamos que disfruten el juego!",True,(255, 255, 255))
            ventana.blit(texto,(estilo.ANCHO_VENTANA // 2 - texto.get_width() // 2,estilo.ALTO_VENTANA // 2 - texto.get_height() // 2))
        elif estado == "SIN_PARTIDA":
            ventana.fill((30, 30, 30))
            texto = fuente_ventanas.render("NO TIENES PARTIDAS GUARDADAS!",True,(255, 255, 255))
            ventana.blit(texto,(estilo.ANCHO_VENTANA // 2 - texto.get_width() // 2,estilo.ALTO_VENTANA // 2 - texto.get_height() // 2))

        pygame.display.update()
        reloj.tick(60)
