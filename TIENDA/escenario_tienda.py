import pygame, os,sys
import estilo
import mochila
import funciones

def escenario_tienda(ventana,jugador):

    pygame.display.set_caption("Poke-Unsam - Tienda")

    imagen_fondo = pygame.image.load(os.path.join(estilo.DIRECTORIO_BASE,"img/Tienda/tienda.png")).convert() 
    imagen_fondo = pygame.transform.scale(imagen_fondo, (estilo.ANCHO_VENTANA, estilo.ALTO_VENTANA))

    imagen_mueble = pygame.image.load(os.path.join(estilo.DIRECTORIO_BASE, "img/Tienda/mueble.png")).convert_alpha() 
    imagen_mueble1 = pygame.image.load(os.path.join(estilo.DIRECTORIO_BASE, "img/Tienda/mueble1.png")).convert_alpha() 

    reloj = pygame.time.Clock()

    jugador.cargar_sprites(jugador.escalas_mapas["tienda"])
    jugador.forma.center = (532, 640)

    menu_jugador = mochila.inicializar_menu()
    
    ejecutar = True
    while ejecutar:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
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
                                funciones.guardar_partida(jugador) 
                            
                            menu_jugador["indice_seleccionado"] = 0

                        elif evento.key == pygame.K_x:  
                            menu_jugador["abierto"] = False
                
                    else:
                        if menu_jugador["seccion"] == "POKEMONS":
                            cant_pokes = len(jugador.pokemons)
                            
                            if cant_pokes > 0:
                                if evento.key == pygame.K_UP:
                                    menu_jugador["indice_seleccionado"] = (menu_jugador["indice_seleccionado"] - 1) % cant_pokes
                                elif evento.key == pygame.K_DOWN:
                                    menu_jugador["indice_seleccionado"] = (menu_jugador["indice_seleccionado"] + 1) % cant_pokes
                                
                                elif evento.key == pygame.K_d:
                                    idx = menu_jugador["indice_seleccionado"]
                                    if 0 <= idx < len(jugador.pokemons):
                                        print(f"Liberando a: {jugador.pokemons[idx].nombre}")
                                        jugador.pokemons.pop(idx)
                                        
                                        if menu_jugador["indice_seleccionado"] >= len(jugador.pokemons) and len(jugador.pokemons) > 0:
                                            menu_jugador["indice_seleccionado"] = len(jugador.pokemons) - 1
                                        elif len(jugador.pokemons) == 0:
                                            menu_jugador["indice_seleccionado"] = 0

                        if evento.key == pygame.K_x:  
                            menu_jugador["seccion"] = "PRINCIPAL"
                            menu_jugador["indice_seleccionado"] = 0

        if not menu_jugador["abierto"]:
            teclas = pygame.key.get_pressed()
            
            delta_x = (teclas[pygame.K_RIGHT] - teclas[pygame.K_LEFT]) * estilo.VELOCIDAD_TIENDA
            delta_y = (teclas[pygame.K_DOWN] - teclas[pygame.K_UP]) * estilo.VELOCIDAD_TIENDA
    
    
            jugador.movimiento(delta_x, delta_y,estilo.LIMITES_TIENDA)
            ventana.blit(imagen_fondo, (0, 0)) 
            jugador.dibujar(ventana)
    
            #---------------------SALIR DE LA TIENDA Y COMPRAR-----------------------------
            accion = jugador.interactuar(teclas)
            if accion is not None:
                accion_retorno = accion
                ejecutar = False 
                

        #------ponemos encima estas imagenes para crear profundidad-------
        
        ventana.blit(imagen_mueble, (111, 486)) 
        ventana.blit(imagen_mueble1, (681, 423))
        ventana.blit(imagen_mueble1, (871, 423))
        
        pygame.draw.rect(ventana, (0, 0, 0), (824, -1, 241, 63), border_radius=6)       
        pygame.draw.rect(ventana, (194, 159, 130), (826, 1, 237, 59), border_radius=5) 
        pygame.draw.rect(ventana, (53, 59, 83), (829, 4, 231, 53), border_radius=4)   
        texto_billetera = estilo.FUENTE_SALDO.render(f"Saldo: {jugador.billetera}", True, (255, 255, 255))
        ventana.blit(texto_billetera, (826 + (237 - texto_billetera.get_width()) // 2, 1 + (59 - texto_billetera.get_height()) // 2))

        mochila.dibujar_menu(ventana,jugador,menu_jugador)
        
        pygame.display.flip()
        reloj.tick(estilo.FPS)

    jugador.cargar_sprites(jugador.escalas_mapas["mundo"])
    return accion_retorno
