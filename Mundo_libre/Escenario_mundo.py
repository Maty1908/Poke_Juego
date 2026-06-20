import pygame, sys, os
import estilo



def escenario_mundo(ventana,jugador):

    reloj = pygame.time.Clock()

    imagen_fondo = pygame.image.load(os.path.join("img/Mapa_mundo/Mundo.png")).convert() 
    imagen_fondo = pygame.transform.scale(imagen_fondo, (estilo.ANCHO_VENTANA, estilo.ALTO_VENTANA))

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
        reloj.tick(estilo.FPS)
        pygame.display.flip()
    return accion_retorno
