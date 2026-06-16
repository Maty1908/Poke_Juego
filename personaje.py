import pygame
import estilo

class personaje():
    def __init__(self, x, y, ruta_spritesheet):
        self.__objetos = {}           #diccionario con objetos y cantidad
        self.__pokemons = []          #lista de pokemons (objetos de python)
        self.__billetera = 50        #dinero del jugador INICIAL!!!!!

        # 1. Cargamos la hoja de sprites completa
        spritesheet = pygame.image.load(ruta_spritesheet).convert_alpha()
        
        # Diccionario para separar las animaciones
        self.animaciones = {
            "abajo": [],
            "arriba": [],
            "izquierda": [],
            "derecha": []
        }
        
        # 2. Recortamos y escalamos cada frame usando las coordenadas de estilo.py
        for direccion, lista_frames in estilo.COORDENADAS_PABLO.items():
            for (origen_x, origen_y, ancho, alto) in lista_frames:
                # Creamos la superficie para el frame individual
                cuadro = pygame.Surface((ancho, alto), pygame.SRCALPHA)
                cuadro.blit(spritesheet, (0, 0), (origen_x, origen_y, ancho, alto))
                
                # Escalamos el frame
                ancho_escalado = int(ancho * estilo.SCALA_PERSONAJE)
                alto_escalado = int(alto * estilo.SCALA_PERSONAJE)
                cuadro_escalado = pygame.transform.scale(cuadro, (ancho_escalado, alto_escalado))
                
                # Guardamos en la dirección correspondiente
                self.animaciones[direccion].append(cuadro_escalado)
                
                # Si es izquierda, creamos la versión espejada para la derecha
                if direccion == "izquierda":
                    cuadro_derecho = pygame.transform.flip(cuadro_escalado, True, False)
                    self.animaciones["derecha"].append(cuadro_derecho)

        # Estados iniciales del personaje
        self.direccion = "abajo"
        self.frame_actual = 0
        self.esta_moviendose = False
        
        # Definimos el Rect físico inicial basado en el primer frame de frente
        ancho_inicial = self.animaciones["abajo"][0].get_width()
        alto_inicial = self.animaciones["abajo"][0].get_height()
        self.forma = pygame.Rect(0, 0, ancho_inicial, alto_inicial)
        self.forma.center = (x, y)
        
        self.ultimo_update = pygame.time.get_ticks()

    def actualizar_animacion(self):
        ahora = pygame.time.get_ticks()
        if self.esta_moviendose:
            if ahora - self.ultimo_update > estilo.COOLDOWN_ANIMACION:
                self.frame_actual = (self.frame_actual + 1) % 3
                self.ultimo_update = ahora
        else:
            self.frame_actual = 0  # Frame quieto

    def movimiento(self, delta_x, delta_y):
        self.esta_moviendose = False
        
        # Control de direcciones de la animación
        if delta_x < 0:
            self.direccion = "izquierda"
            self.esta_moviendose = True
        elif delta_x > 0:
            self.direccion = "derecha"
            self.esta_moviendose = True
            
        if delta_y < 0:
            self.direccion = "arriba"
            self.esta_moviendose = True
        elif delta_y > 0:
            self.direccion = "abajo"
            self.esta_moviendose = True

        # --- SISTEMA DE FRENO EN EJE X ---
        self.forma.x += delta_x  # Intentamos mover en X
        
        # Si se pasa de la pantalla o choca un obstáculo, lo tiramos para atrás
        if self.forma.left < 0 or self.forma.right > estilo.ANCHO_VENTANA or self.revisar_choque_objetos():
            self.forma.x -= delta_x

        # --- SISTEMA DE FRENO EN EJE Y ---
        self.forma.y += delta_y  # Intentamos mover en Y
        
        # Si se pasa de la pantalla o choca un obstáculo, lo tiramos para atrás
        if self.forma.top < 0 or self.forma.bottom > estilo.ALTO_VENTANA or self.revisar_choque_objetos():
            self.forma.y -= delta_y

        # Adaptamos dinámicamente el tamaño de la caja al frame actual
        self.forma.width = self.animaciones[self.direccion][self.frame_actual].get_width()
        self.forma.height = self.animaciones[self.direccion][self.frame_actual].get_height()
        
        self.actualizar_animacion()

    def revisar_choque_objetos(self):
        # Recorremos la lista de tuplas de estilo.py
        for (obs_x, obs_y, obs_ancho, obs_alto) in estilo.LIMITES_MUNDO_LIBRE:
            # Creamos un Rect virtual para usar la herramienta colliderect de Pygame
            rect_obstaculo = pygame.Rect(obs_x, obs_y, obs_ancho, obs_alto)
            
            # Si nuestra caja física toca el obstáculo, avisa que hay choque (True)
            if self.forma.colliderect(rect_obstaculo):
                return True
        return False

    def dibujar(self, ventana):
        # Dibujamos al personaje
        imagen_a_dibujar = self.animaciones[self.direccion][self.frame_actual]
        ventana.blit(imagen_a_dibujar, self.forma.topleft)
        
    #----------Getters y Setters----------
    @property
    def obtener_dinero(self):
        return self.__billetera
