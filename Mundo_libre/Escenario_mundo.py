import pygame, sys, os
import estilo

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


    ejecutar = True 
    while ejecutar:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sys.exit()

                    
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
        
        reloj.tick(estilo.FPS)
        pygame.display.flip()
    return accion_retorno
