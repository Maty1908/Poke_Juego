import pygame
import estilo

class personaje():

    #-------INICIADOR-----------
    def __init__(self,ruta_spritesheet):
        self.billetera = 100
        self.inventario = {"pocion":0,"revivir":0} 
        self.pokemons = []
        self.escalas_mapas = {"tienda": 0.3,"mundo":0.125}
        self.ruta_spritesheet = ruta_spritesheet
        self.ultimo_viaje = 0

        self.direccion = "abajo"
        self.frame_actual = 0
        self.esta_moviendose = False
       
        self.cargar_sprites(self.escalas_mapas["mundo"])

        ancho_inicial = self.animaciones["abajo"][0].get_width()
        alto_inicial = self.animaciones["abajo"][0].get_height()
        self.forma = pygame.Rect(0, 0, ancho_inicial, alto_inicial)

        self.ultimo_update = pygame.time.get_ticks()
    #------------METODOS-------------------------
    def cargar_sprites(self, escala):
            self.animaciones = {
                "abajo": [],
                "arriba": [],
                "izquierda": [],
                "derecha": []
            }
            
            spritesheet = pygame.image.load(self.ruta_spritesheet).convert_alpha()
            
            for direccion, lista_frames in estilo.COORDENADAS.items():
                for (origen_x, origen_y, ancho, alto) in lista_frames:
                    cuadro = pygame.Surface((ancho, alto), pygame.SRCALPHA)
                    cuadro.blit(spritesheet, (0, 0), (origen_x, origen_y, ancho, alto))
                    
                    ancho_escalado = int(ancho * escala)
                    alto_escalado = int(alto * escala)
                    cuadro_escalado = pygame.transform.scale(cuadro, (ancho_escalado, alto_escalado))
                    
                    self.animaciones[direccion].append(cuadro_escalado)
                    
                    if direccion == "izquierda":
                        cuadro_derecho = pygame.transform.flip(cuadro_escalado, True, False)
                        self.animaciones["derecha"].append(cuadro_derecho)
                        
            if hasattr(self, "forma"):
                frame_actual = self.animaciones[self.direccion][self.frame_actual]
                self.forma.size = frame_actual.get_size()

    def actualizar_animacion(self):
        ahora = pygame.time.get_ticks()
        if self.esta_moviendose:
            if ahora - self.ultimo_update > estilo.COOLDOWN_ANIMACION:
                self.frame_actual = (self.frame_actual + 1) % 3
                self.ultimo_update = ahora
        else:
            self.frame_actual = 0  # Frame quieto

    def movimiento(self, delta_x, delta_y,limites):
        self.esta_moviendose = (delta_x != 0 or delta_y != 0)

        if delta_x < 0: self.direccion = "izquierda"
        elif delta_x > 0: self.direccion = "derecha"
        
        if delta_y < 0: self.direccion = "arriba"
        elif delta_y > 0: self.direccion = "abajo"

        if delta_x != 0:
            self.forma.x += delta_x
            if self.forma.left < 0 or self.forma.right > estilo.ANCHO_VENTANA or self.revisar_choque_objetos(limites):
                self.forma.x -= delta_x

        if delta_y != 0:
            self.forma.y += delta_y
            if self.forma.top < 0 or self.forma.bottom > estilo.ALTO_VENTANA or self.revisar_choque_objetos(limites):
                self.forma.y -= delta_y

        frame_actual = self.animaciones[self.direccion][self.frame_actual]
        self.forma.size = frame_actual.get_size()
        
        self.actualizar_animacion()

    def revisar_choque_objetos(self,limites):
        for (obs_x, obs_y, obs_ancho, obs_alto) in limites:
            rect_obstaculo = pygame.Rect(obs_x, obs_y, obs_ancho, obs_alto)
            
            if self.forma.colliderect(rect_obstaculo):
                return True
        return False

    def dibujar(self, ventana):
        imagen_a_dibujar = self.animaciones[self.direccion][self.frame_actual]
        ventana.blit(imagen_a_dibujar, self.forma.topleft)

    def interactuar(self, teclas):
            if teclas[pygame.K_c]:
                ahora = pygame.time.get_ticks()
                if ahora - self.ultimo_viaje < 600: 
                    return None
                self.ultimo_viaje = ahora
                            
                for (tienda_x, tienda_y, ancho, alto) in estilo.ENTRADA_TIENDA:
                    rect_tienda = pygame.Rect(tienda_x, tienda_y, ancho, alto)
                    if self.forma.colliderect(rect_tienda):
                        return "TIENDA"
                    
                for (compra_x, compra_y, ancho, alto) in estilo.MOSTRADOR:
                    rect_mostrador = pygame.Rect(compra_x, compra_y, ancho, alto)
                    if self.forma.colliderect(rect_mostrador):
                        return "COMPRAR"
                
                    
                for (tienda_x, tienda_y, ancho, alto) in estilo.SALIDA_TIENDA:
                    rect_tienda = pygame.Rect(tienda_x, tienda_y, ancho, alto)
                    if self.forma.colliderect(rect_tienda):
                        return "SALIR"
                
                for (npc_x, npc_y, ancho, alto) in estilo.NPC_MUNDO_LIBRE:
                    rect_npc = pygame.Rect(npc_x, npc_y, ancho, alto)
                    if self.forma.colliderect(rect_npc):
                        return "PELEANDO"
                        
            return None  # Si no interactúa o no presiona 'C', no cambia el estado
