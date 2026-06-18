import pygame
import sys

class AnimacionCaja:
    def __init__(self, ruta_imagen):
        # convert_alpha() y subsurface mantienen la misma referencia de memoria
        sheet = pygame.image.load(ruta_imagen).convert_alpha()
        
        # Guardamos dimensiones fijas resumidas
        self.w, self.h = 299, 448  
        ancho_exacto = 1197 / 4  
        
        # Generamos los 8 frames en un solo ciclo (List Comprehension)
        self.frames = [
            sheet.subsurface(pygame.Rect(int((i % 4) * ancho_exacto), (i // 4) * self.h, self.w, self.h))
            for i in range(8)
        ]

        # Variables de control
        self.frame_actual = 0
        self.ultimo_cambio = pygame.time.get_ticks()
        self.velocidad = 250 
        
        self.esperando_enter = False
        self.terminada = False

    def actualizar(self):
        if self.terminada: return

        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_cambio > self.velocidad:
            if self.frame_actual == 5 and self.esperando_enter:
                return # Bloqueo en el destello
            
            if self.frame_actual < 7:
                self.frame_actual += 1
                self.ultimo_cambio = ahora
                if self.frame_actual == 5: 
                    self.esperando_enter = True
            else:
                self.terminada = True

    def dibujar(self, pantalla, x, y):
        pantalla.blit(self.frames[self.frame_actual], (x, y))
        
        if self.esperando_enter:
            fuente = pygame.font.SysFont("Arial", 24, bold=True)
            texto = fuente.render("¡Presiona ENTER para continuar!", True, (255, 255, 255))
            pantalla.blit(texto, ((pantalla.get_width() - texto.get_width()) // 2, y + self.h + 20))


# =====================================================================
# --- CÓDIGO DE TESTEO (Compila directo) ---
# =====================================================================
if __name__ == '__main__':
    pygame.init()
    
    ANCHO_VENTANA = 600
    ALTO_VENTANA = 650 
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Test - Caja Optimizada")
    
    reloj = pygame.time.Clock()
    RUTA_TU_IMAGEN = "img/Cajas_Frames/Poke_N.png"

    try:
        animacion = AnimacionCaja(RUTA_TU_IMAGEN)
    except FileNotFoundError:
        print(f"\n[ERROR] No se encontró la imagen en: '{RUTA_TU_IMAGEN}'")
        sys.exit()

    ejecutando = True
    while ejecutando:
        reloj.tick(60)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
                
            if evento.type == pygame.KEYDOWN:
                if animacion.esperando_enter and evento.key == pygame.K_RETURN:
                    animacion.esperando_enter = False
                    animacion.ultimo_cambio = pygame.time.get_ticks() # Reset para el frame 6
        
        animacion.actualizar()
        
        if animacion.terminada:
            print("Secuencia ultra-optimizada finalizada con éxito.")
            ejecutando = False
        
        pantalla.fill((30, 30, 30)) 
        
        # Centrado utilizando los nombres de variables optimizados (w y h)
        x_centro = (ANCHO_VENTANA - animacion.w) // 2
        y_centro = (ALTO_VENTANA - animacion.h) // 2 - 30 
        
        animacion.dibujar(pantalla, x_centro, y_centro)
        
        pygame.display.flip()

    pygame.quit()