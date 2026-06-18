import pygame
import sys

class AnimacionCaja:
    def __init__(self, ruta_imagen):
        # Cargamos el sprite sheet desde tu ruta exacta
        self.sheet = pygame.image.load(ruta_imagen).convert_alpha()
        
        # Medidas basadas en tu archivo de Paint
        self.frame_width = 299  
        self.frame_height = 448  
        
        self.frames = []
        
        # Recorte Fila 1 (Frames 0 al 3)
        for i in range(4):
            x = i * self.frame_width
            y = 0
            cuadro = self.sheet.subsurface(pygame.Rect(x, y, self.frame_width, self.frame_height))
            self.frames.append(cuadro)
            
        # Recorte Fila 2 (Frames 4 al 7)
        for i in range(4):
            x = i * self.frame_width
            y = self.frame_height
            cuadro = self.sheet.subsurface(pygame.Rect(x, y, self.frame_width, self.frame_height))
            self.frames.append(cuadro)


# =====================================================================
# --- CÓDIGO DE TESTEO (Solo se ejecuta si corres este archivo) ---
# =====================================================================
if __name__ == '__main__':
    # Inicializamos Pygame para el test
    pygame.init()
    
    # Creamos una ventana cómoda para ver las dos filas de frames
    ANCHO_VENTANA = 1250
    ALTO_VENTANA = 950
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Test de Recorte de Frames - Caja Pokémon")
    
    # Tu ruta específica para compilar directo
    RUTA_TU_IMAGEN = "img/Cajas_Frames/Poke_N.png"

    try:
        animacion = AnimacionCaja(RUTA_TU_IMAGEN)
    except FileNotFoundError:
        print(f"\n[ERROR] No se encontró la imagen en: '{RUTA_TU_IMAGEN}'")
        print("Asegúrate de estar ejecutando el script desde la carpeta raíz del proyecto (donde está 'Poke_Juego').")
        sys.exit()

    # Bucle del test
    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
        
        # Fondo gris oscuro para contrastar el sprite
        pantalla.fill((40, 40, 40)) 
        
        # Dibujamos Fila 1 en la pantalla
        for i in range(4):
            x_pos = 10 + (i * 305) # 305 deja un margen de 6px entre cuadros
            y_pos = 10
            # Rectángulo guía gris de fondo
            pygame.draw.rect(pantalla, (100, 100, 100), (x_pos, y_pos, animacion.frame_width, animacion.frame_height), 1)
            pantalla.blit(animacion.frames[i], (x_pos, y_pos))
            
        # Dibujamos Fila 2 en la pantalla (Corregido 'pantalla')
        for i in range(4):
            x_pos = 10 + (i * 305)
            y_pos = 480 
            pygame.draw.rect(pantalla, (100, 100, 100), (x_pos, y_pos, animacion.frame_width, animacion.frame_height), 1)
            # Los frames de la segunda fila van del índice 4 al 7
            pantalla.blit(animacion.frames[i + 4], (x_pos, y_pos))
            
        pygame.display.flip()

    pygame.quit()