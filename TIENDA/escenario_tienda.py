import pygame, os,sys
import estilo
from personaje import *

def escenario_tienda(ventana,personaje_elegido):

    pygame.display.set_caption("Poke-Unsam - Tienda")

    imagen_fondo = pygame.image.load(os.path.join(estilo.DIRECTORIO_BASE,"img/Tienda/tienda.png")).convert() 
    imagen_fondo = pygame.transform.scale(imagen_fondo, (estilo.ANCHO_VENTANA, estilo.ALTO_VENTANA))

    imagen_mueble = pygame.image.load(os.path.join(estilo.DIRECTORIO_BASE, "img/Tienda/mueble.png")).convert_alpha() 
    imagen_mueble1 = pygame.image.load(os.path.join(estilo.DIRECTORIO_BASE, "img/Tienda/mueble1.png")).convert_alpha() 


    jugador = personaje(532, 640, os.path.join(estilo.DIRECTORIO_BASE, f"img/skins/{personaje_elegido}/OV.png"))

    reloj = pygame.time.Clock()

    ejecutar = True
    while ejecutar:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        teclas = pygame.key.get_pressed()
        
        delta_x = (teclas[pygame.K_RIGHT] - teclas[pygame.K_LEFT]) * estilo.VELOCIDAD
        delta_y = (teclas[pygame.K_DOWN] - teclas[pygame.K_UP]) * estilo.VELOCIDAD

        # La clase se encarga de mover y setear la animación correcta
        jugador.movimiento(delta_x, delta_y)
        ventana.blit(imagen_fondo, (0, 0)) 
        jugador.dibujar(ventana) 
        ventana.blit(imagen_mueble, (111, 486)) 
        ventana.blit(imagen_mueble1, (682, 424))
        ventana.blit(imagen_mueble1, (872, 424))
        
        
        pygame.display.update()
        reloj.tick(estilo.FPS)
