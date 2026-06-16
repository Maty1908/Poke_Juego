# mundo_libre.py
import pygame, os,sys
import estilo
from personaje import *

def escenario_tienda(ventana,personaje_elegido):

    pygame.display.set_caption("Poke-Unsam - Tienda")

    imagen_fondo = pygame.image.load(os.path.join(estilo.DIRECTORIO_BASE,"img/Tienda/tienda.png")).convert() 
    imagen_fondo = pygame.transform.scale(imagen_fondo, (estilo.ANCHO_VENTANA, estilo.ALTO_VENTANA))

    jugador = personaje(532, 640, os.path.join(estilo.DIRECTORIO_BASE, f"img/skins/{personaje_elegido}/OV.png"))

    reloj = pygame.time.Clock()

    ejecutar = True
    while ejecutar:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        teclas = pygame.key.get_pressed()
        
        delta_x = (teclas[pygame.K_d] - teclas[pygame.K_a]) * estilo.VELOCIDAD
        delta_y = (teclas[pygame.K_s] - teclas[pygame.K_w]) * estilo.VELOCIDAD

        # La clase se encarga de mover y setear la animación correcta
        jugador.movimiento(delta_x, delta_y)
        ventana.blit(imagen_fondo, (0, 0))
        ventana.blit(imagen_fondo, (0, 0))
        
        jugador.dibujar(ventana)
        pygame.display.update()
        reloj.tick(estilo.FPS)
