import pygame, os,sys
import estilo


def escenario_tienda(ventana,jugador):

    pygame.display.set_caption("Poke-Unsam - Tienda")

    imagen_fondo = pygame.image.load(os.path.join(estilo.DIRECTORIO_BASE,"img/Tienda/tienda.png")).convert() 
    imagen_fondo = pygame.transform.scale(imagen_fondo, (estilo.ANCHO_VENTANA, estilo.ALTO_VENTANA))

    imagen_mueble = pygame.image.load(os.path.join(estilo.DIRECTORIO_BASE, "img/Tienda/mueble.png")).convert_alpha() 
    imagen_mueble1 = pygame.image.load(os.path.join(estilo.DIRECTORIO_BASE, "img/Tienda/mueble1.png")).convert_alpha() 

    reloj = pygame.time.Clock()

    jugador.cargar_y_escalar_sprites(jugador.escalas_mapas["tienda"])
    jugador.forma.center = (532, 640)   #spawn inicial del jugador

    ejecutar = True
    while ejecutar:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        teclas = pygame.key.get_pressed()
        
        delta_x = (teclas[pygame.K_RIGHT] - teclas[pygame.K_LEFT]) * estilo.VELOCIDAD_TIENDA
        delta_y = (teclas[pygame.K_DOWN] - teclas[pygame.K_UP]) * estilo.VELOCIDAD_TIENDA


        # La clase se encarga de mover y setear la animación correcta
        jugador.movimiento(delta_x, delta_y,estilo.LIMITES_TIENDA)
        ventana.blit(imagen_fondo, (0, 0)) 
        jugador.dibujar(ventana) #posicion del jugador

        #---------------------SALIR DE LA TIENDA Y COMPRAR-----------------------------
        accion = jugador.interactuar(teclas)
        if accion is not None:
            accion_retorno = accion
            ejecutar = False 
            

        #------ponemos encima estas imagenes para crear profundidad-------
        
        ventana.blit(imagen_mueble, (111, 486)) 
        ventana.blit(imagen_mueble1, (681, 423))
        ventana.blit(imagen_mueble1, (871, 423))
        
        pygame.draw.rect(ventana, (0, 0, 0), (824, -1, 241, 63), border_radius=6)       # 🟢 NUEVO: Borde exterior Negro (+2px)
        pygame.draw.rect(ventana, (194, 159, 130), (826, 1, 237, 59), border_radius=5) # Borde marrón
        pygame.draw.rect(ventana, (53, 59, 83), (829, 4, 231, 53), border_radius=4)   # Fondo azul
        texto_billetera = estilo.FUENTE_SALDO.render(f"Saldo: {jugador.billetera}", True, (255, 255, 255))
        ventana.blit(texto_billetera, (826 + (237 - texto_billetera.get_width()) // 2, 1 + (59 - texto_billetera.get_height()) // 2))
        
        pygame.display.flip()
        reloj.tick(estilo.FPS)

    jugador.cargar_y_escalar_sprites(jugador.escalas_mapas["mundo"])
    return accion_retorno
