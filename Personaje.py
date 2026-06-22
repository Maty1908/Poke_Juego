import pygame
import estilo

class personaje():

    #-------INICIADOR-----------

    def __init__(self,ruta_spritesheet):
        self.billetera = 100
        self.inventario = {"pocion":0,"revivir":0} #diccionario con objetos y cantidad
        self.pokemons = []          #lista de pokemons (objetos de python)
        self.escalas_mapas = {"tienda": 0.3,"mundo":0.125} #inicializamos al personaje en el mundo libre con esta escala
        self.ruta_spritesheet = ruta_spritesheet
        self.ultimo_viaje = 0
    
        # Estados iniciales del personaje
        self.direccion = "abajo"
        self.frame_actual = 0
        self.esta_moviendose = False

       
        self.cargar_y_escalar_sprites(self.escalas_mapas["mundo"])

        # Definimos LA hitbox del personaje basado en el primer frame de frente
        ancho_inicial = self.animaciones["abajo"][0].get_width()
        alto_inicial = self.animaciones["abajo"][0].get_height()
        self.forma = pygame.Rect(0, 0, ancho_inicial, alto_inicial)

        self.ultimo_update = pygame.time.get_ticks()
    #------------METODOS-------------------------
    def cargar_y_escalar_sprites(self, escala):
            self.animaciones = {
                "abajo": [],
                "arriba": [],
                "izquierda": [],
                "derecha": []
            }
            
            # Cargamos la hoja de sprites completa
            spritesheet = pygame.image.load(self.ruta_spritesheet).convert_alpha()
            
            # Recortamos y escalamos cada frame usando las coordenadas de estilo.py
            for direccion, lista_frames in estilo.COORDENADAS.items():
                for (origen_x, origen_y, ancho, alto) in lista_frames:
                    # Creamos la superficie para el frame individual
                    cuadro = pygame.Surface((ancho, alto), pygame.SRCALPHA)
                    cuadro.blit(spritesheet, (0, 0), (origen_x, origen_y, ancho, alto))
                    
                    # Escalamos el frame usando el parámetro flotante 'escala'
                    ancho_escalado = int(ancho * escala)
                    alto_escalado = int(alto * escala)
                    cuadro_escalado = pygame.transform.scale(cuadro, (ancho_escalado, alto_escalado))
                    
                    # Guardamos en la dirección correspondiente
                    self.animaciones[direccion].append(cuadro_escalado)
                    
                    # Si es izquierda, creamos la versión espejada para la derecha
                    if direccion == "izquierda":
                        cuadro_derecho = pygame.transform.flip(cuadro_escalado, True, False)
                        self.animaciones["derecha"].append(cuadro_derecho)
                        
            # Si la hitbox física ya existía, actualizamos su tamaño para evitar que se quede con medidas viejas
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
        # 1. Control de movimiento y animaciones
        self.esta_moviendose = (delta_x != 0 or delta_y != 0)

        if delta_x < 0: self.direccion = "izquierda"
        elif delta_x > 0: self.direccion = "derecha"
        
        if delta_y < 0: self.direccion = "arriba"
        elif delta_y > 0: self.direccion = "abajo"

        # 2. Movimiento y sistema de freno en Eje X
        if delta_x != 0:
            self.forma.x += delta_x
            if self.forma.left < 0 or self.forma.right > estilo.ANCHO_VENTANA or self.revisar_choque_objetos(limites):
                self.forma.x -= delta_x

        # 3. Movimiento y sistema de freno en Eje Y
        if delta_y != 0:
            self.forma.y += delta_y
            if self.forma.top < 0 or self.forma.bottom > estilo.ALTO_VENTANA or self.revisar_choque_objetos(limites):
                self.forma.y -= delta_y

        # 4. Adaptar hitbox al tamaño del frame actual y animar
        frame_actual = self.animaciones[self.direccion][self.frame_actual]
        self.forma.size = frame_actual.get_size()
        
        self.actualizar_animacion()

    def revisar_choque_objetos(self,limites):
        # Recorremos la lista de tuplas de estilo.py
        for (obs_x, obs_y, obs_ancho, obs_alto) in limites:
            # Creamos un Rect virtual para usar la herramienta colliderect de pygame
            rect_obstaculo = pygame.Rect(obs_x, obs_y, obs_ancho, obs_alto)
            
            # Si nuestra caja física toca el obstáculo, avisa que hay choque (True)
            if self.forma.colliderect(rect_obstaculo):
                return True
        return False

    def dibujar(self, ventana):
        # Dibujamos al personaje
        imagen_a_dibujar = self.animaciones[self.direccion][self.frame_actual]
        ventana.blit(imagen_a_dibujar, self.forma.topleft)

    def interactuar(self, teclas):
            # Verificamos si la tecla 'C' está presionada
            if teclas[pygame.K_c]:
                ahora = pygame.time.get_ticks()
                if ahora - self.ultimo_viaje < 600: 
                    return None
                self.ultimo_viaje = ahora
                            
                # 1. Comprobar colisión con la Entrada de la Tienda
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
                
                # 2. Comprobar colisión con cualquier NPC del mundo libre
                for (npc_x, npc_y, ancho, alto) in estilo.NPC_MUNDO_LIBRE:
                    rect_npc = pygame.Rect(npc_x, npc_y, ancho, alto)
                    if self.forma.colliderect(rect_npc):
                        return "PELEANDO"
                        
            return None  # Si no interactúa o no presiona 'C', no cambia el estado
