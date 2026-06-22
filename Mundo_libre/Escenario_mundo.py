import pygame, sys, os
import estilo
import mochila
import gestor_datos

def escenario_mundo(ventana,jugador):

    reloj = pygame.time.Clock()

    imagen_fondo = pygame.image.load(os.path.join("img/Mapa_mundo/Mundo.png")).convert() 
    imagen_fondo = pygame.transform.scale(imagen_fondo, (estilo.ANCHO_VENTANA, estilo.ALTO_VENTANA))

    arbol = pygame.image.load(os.path.join("img/Mapa_mundo/arbol1.png")).convert_alpha()
    posiciones_arboles = [
        (372, 667), (296, 667), (223, 667), (148, 667),  (77, 667), (8, 667),
        (651, 667), (763, 454), (955, 453), (794, 259), (870, 259),
    ]

    farol = pygame.image.load(os.path.join("img/Mapa_mundo/farol.png")).convert_alpha()
    posiciones_faroles = [
        (322, 327), (619, 236), (729, 340), (580, 546), (469, 546)
    ]


    maceta = pygame.image.load(os.path.join("img/Mapa_mundo/maceta.png")).convert_alpha()
    posiciones_macetas = [
        (350, 577), (609, 577)
    ]

    shop = pygame.image.load(os.path.join("img/Mapa_mundo/shop.png")).convert_alpha()
    respaldo1 = pygame.image.load(os.path.join("img/Mapa_mundo/respaldo1.png")).convert_alpha()
    respaldo2 = pygame.image.load(os.path.join("img/Mapa_mundo/respaldo2.png")).convert_alpha()
    
    barril = pygame.image.load(os.path.join("img/Mapa_mundo/barril.png")).convert_alpha()
    posiciones_barril = [
        (287, 537), (723, 564)
    ]
    
    NPC_bosque = pygame.image.load(os.path.join("img/Mapa_mundo/NPC_bosque.png")).convert_alpha()
    NPC_bosque = pygame.transform.scale(NPC_bosque, (estilo.ANCHO_PERSONAJE, estilo.ALTO_PERSONAJE))
    
    fuente = pygame.image.load(os.path.join("img/Mapa_mundo/fuente.png")).convert_alpha()
    
    jugador.forma.center = (135,625)    #spawn del jugador

    menu_jugador = mochila.inicializar_menu()

    ejecutar = True 
    while ejecutar:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if not menu_jugador["abierto"]:
                    if evento.key == pygame.K_x:
                        menu_jugador["abierto"] = True
                        menu_jugador["seccion"] = "PRINCIPAL"
                        menu_jugador["indice_seleccionado"] = 0
                else:
                   
                    if menu_jugador["seccion"] == "PRINCIPAL":
                        if evento.key == pygame.K_UP:
                            menu_jugador["indice_seleccionado"] = (menu_jugador["indice_seleccionado"] - 1) % 3
                        elif evento.key == pygame.K_DOWN:
                            menu_jugador["indice_seleccionado"] = (menu_jugador["indice_seleccionado"] + 1) % 3
                        
                        elif evento.key == pygame.K_c:  
                            if menu_jugador["indice_seleccionado"] == 0:
                                menu_jugador["seccion"] = "POKEMONS"
                            elif menu_jugador["indice_seleccionado"] == 1:
                                menu_jugador["seccion"] = "OBJETOS"
                            elif menu_jugador["indice_seleccionado"] == 2:
                                menu_jugador["seccion"] = "GUARDAR"
                                gestor_datos.guardar_partida(jugador) 
                            
                            menu_jugador["indice_seleccionado"] = 0

                        elif evento.key == pygame.K_x:  
                            menu_jugador["abierto"] = False

                   
                    else:
                        if evento.key == pygame.K_x:  
                            menu_jugador["seccion"] = "PRINCIPAL"
                            menu_jugador["indice_seleccionado"] = 0


        if not menu_jugador["abierto"]:                    
            teclas = pygame.key.get_pressed()
                
            delta_x = (teclas[pygame.K_RIGHT] - teclas[pygame.K_LEFT]) * estilo.VELOCIDAD_MUNDO_LIBRE
            delta_y = (teclas[pygame.K_DOWN] - teclas[pygame.K_UP]) * estilo.VELOCIDAD_MUNDO_LIBRE


        
            limites_totales = estilo.LIMITES_MUNDO_LIBRE
            jugador.movimiento(delta_x, delta_y, limites_totales)

            accion = jugador.interactuar(teclas)
            if accion is not None:
                accion_retorno = accion
                ejecutar = False # Rompemos el bucle para volver al index.py con el nuevo estado
            
            
        ventana.blit(imagen_fondo, (0, 0)) 
        jugador.dibujar(ventana)

        for pos in posiciones_arboles:
            ventana.blit(arbol, pos)
        
        for pos in posiciones_faroles:
            ventana.blit(farol, pos)

        ventana.blit(shop,(1, 446))

        for pos in posiciones_macetas:
            ventana.blit(maceta, pos)

        ventana.blit(respaldo1, (320, 473))
        ventana.blit(respaldo2, (726, 472))
        ventana.blit(NPC_bosque, (860, 465))
        ventana.blit(fuente,(457, 373))

        for pos in posiciones_barril:
            ventana.blit(barril,pos)

        mochila.dibujar_menu(ventana,jugador,menu_jugador)

        reloj.tick(estilo.FPS)
        pygame.display.flip()
        
    return accion_retorno
