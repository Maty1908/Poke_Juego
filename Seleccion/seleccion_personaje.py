import pygame,os,sys
import estilo

#------------GAME LOOP------------------
def menu_seleccion(ventana):
    pygame.display.set_caption("Poke-Unsam - Seleccion")
    #--------------FONDO-----------------------
    carpeta_actual = os.path.dirname(__file__)  #archivo actual
    ruta_imagen = os.path.join(carpeta_actual,"..","img","Menu","Seleccion_personaje.png")  #mete archivo en la carpeta actual
    imagen_fondo = pygame.image.load(ruta_imagen)
    imagen_fondo = pygame.transform.scale(imagen_fondo, (estilo.ANCHO_VENTANA,estilo.ALTO_VENTANA))

    #------------POSICION PERSONAJES------------------
    personajes = [                              
        {"nombre": "Fede",   "rect": pygame.Rect(95, 270, 200, 300)},
        {"nombre": "Pablo", "rect": pygame.Rect(435, 270, 200, 300)},
        {"nombre": "Maxi", "rect": pygame.Rect(760, 270, 200, 300)}]
    #rect es un obj de la libreria pygame que crea rectangulos
    #(X,Y,ANCHO,ALTO)
    #---------------FUENTE TEXTO--------------------------
    carpeta_actual = os.path.dirname(__file__)
    # ".." retrocede una carpeta y entra a tipografia para buscar el archivo
    ruta_fuente = os.path.join(carpeta_actual, "..", "tipografia", "pokemon_font.ttf")
    fuente = pygame.font.Font(ruta_fuente, 24)
    profe = None        #variable para mandar eleccion de personaje
    ejecutar = True
    
    while ejecutar:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1: 
                    for p in personajes:
                        if p["rect"].collidepoint(pos_mouse):
                            profe = p["nombre"].lower()
                            ejecutar = False
        
        ventana.blit(imagen_fondo,(0,0))
        pos_mouse = pygame.mouse.get_pos()
        
        for p in personajes:
            if p["rect"].collidepoint(pos_mouse):
                texto_nombre = fuente.render(p["nombre"], True, (255, 255, 255)) #True le mete suavizado a la fuente
                
                # cartel negro atras de texto
                margen_x = 20
                margen_y = 10
                ancho_cartel = texto_nombre.get_width() + margen_x
                alto_cartel = texto_nombre.get_height() + margen_y
                
                
                # pygame.SRCALPHA indica la transparencia al programa
                cartel_fondo = pygame.Surface((ancho_cartel, alto_cartel), pygame.SRCALPHA)
                
                #(color negro, opacidad)
                cartel_fondo.fill((0, 0, 0, 180))
                
                #texto centrado en el cartel
                pos_texto_x = margen_x // 2
                pos_texto_y = margen_y // 2
                cartel_fondo.blit(texto_nombre, (pos_texto_x, pos_texto_y))
                
                # 6. CALCULAMOS LA POSICIÓN EN LA PANTALLA GENERAL (siguiendo al mouse)
                cartel_x = pos_mouse[0] - (ancho_cartel // 2)
                cartel_y = pos_mouse[1] - (alto_cartel + 20) 
                
                # 7. Dibujamos el cartel completo final en la ventana
                ventana.blit(cartel_fondo, (cartel_x, cartel_y))
        pygame.display.flip()
    return profe
