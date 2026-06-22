import pygame


#para musica usar .mp3 y para sonido .wav 

def reproducir_musica(musica,bucle):

    nombre_archivo = f"Sonido/Musica/{musica}"

    try:
        pygame.mixer.music.load(nombre_archivo)

        #-1 significa bucle infinito, y 0 significa reproducir solo 1 vez.
        repeticiones = -1 if bucle else 0

        pygame.mixer.music.set_volume(0.2) #volumen se regula entre 0 y 1

        pygame.mixer.music.play(repeticiones)

    except pygame.error:
        print("error en archivo de audio")



def reproducir_sonido(sonido):
   
    nombre_archivo = f"Sonido/Efectos/{sonido}"  
    
    try:
        # 1. Cargamos el sonido en la memoria RAM para acceso instantáneo
        efecto = pygame.mixer.Sound(nombre_archivo)
        
        # 2. Regulamos su volumen (0.0 a 1.0)
        efecto.set_volume(0.6)
        
        # 3. Lo reproducimos. play() sin argumentos lo reproduce una sola vez
        efecto.play()
        
    except pygame.error:
        print(f"error en archivo de sonido: {nombre_archivo}")
