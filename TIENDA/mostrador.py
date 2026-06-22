import pygame,os,sys
import estilo


def mostrador(ventana,jugador,tienda):
    pygame.display.set_caption("Poke-Unsam - Tienda")

    imagen_mostrador = pygame.image.load(os.path.join(estilo.DIRECTORIO_BASE,"img/Tienda/mostrador.png")).convert() 
    imagen_mostrador = pygame.transform.scale(imagen_mostrador, (estilo.ANCHO_VENTANA, estilo.ALTO_VENTANA))

    reloj = pygame.time.Clock()

    hitbox = estilo.HITBOX_OBJ
    info = estilo.INFO_OBJ

    accion_retorno = "TIENDA"

    ejecutar = True
    while ejecutar:

        pos_mouse = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_x:
                    accion_retorno = "TIENDA"
                    ejecutar = False

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:

                    for obj in estilo.HITBOX_OBJ:
                        if obj["rect"].collidepoint(pos_mouse):

                            compra = obj["nombre"]

                            if compra == "normal":
                                tienda.abrir_caja(jugador,"normal",ventana)

                            elif compra == "especial":
                                tienda.abrir_caja(jugador,"especial",ventana)

                            elif compra == "rara":
                                tienda.abrir_caja(jugador,"rara",ventana)

                            elif compra == "legendaria":
                                tienda.abrir_caja(jugador,"legendaria",ventana)

                            elif compra == "pocion":
                                tienda.comprar_objeto(jugador,"pocion")                             

                            elif compra == "revivir":
                                tienda.comprar_objeto(jugador,"revivir") 




        ventana.blit(imagen_mostrador, (0, 0)) 
        pygame.display.update() 
        reloj.tick(estilo.FPS)


    #fin de compra
    return accion_retorno
