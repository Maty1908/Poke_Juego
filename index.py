import pygame,os
pygame.init()

from Menu.MENU import menu_inicial
import Personaje
import estilo
from funciones import cargar_partida,reproducir_musica

from Seleccion.seleccion_personaje import menu_seleccion
from Mundo_libre.Escenario_mundo import escenario_mundo
from TIENDA.tienda import Tienda
from TIENDA.escenario_tienda import escenario_tienda 
from TIENDA.mostrador import mostrador
from Peleas.sprite_combate import batalla

ventana = pygame.display.set_mode((1064, 704))
estado = "MENU"
reproducir_musica("menu.mp3",bucle=True)
profe_elegido = None
ejecutar = True

while ejecutar:
    
    if estado == "MENU":
        eleccion_menu = menu_inicial(ventana)
        estado = eleccion_menu

    elif estado == "CONTINUAR": 
       
        ruta_defecto = os.path.join(estilo.DIRECTORIO_BASE, "img/skins/profe1/OV.png")
        jugador_cargado = cargar_partida(ruta_defecto)
        
        if jugador_cargado is not None:
            jugador = jugador_cargado
            tienda = Tienda()
            
            pygame.mixer.music.stop()
            reproducir_musica("mundo.mp3", bucle=True)
            estado = "MUNDO_LIBRE"
            
        else:
            estado = "SELECCION"

    elif estado == "SELECCION":
        profe_elegido = menu_seleccion(ventana)
        jugador = Personaje.personaje(os.path.join(estilo.DIRECTORIO_BASE, f"img/skins/{profe_elegido}/OV.png"))
        tienda = Tienda()
        
        pygame.mixer.music.stop()
        reproducir_musica("mundo.mp3",bucle=True)
        estado = "MUNDO_LIBRE"
        
    elif estado == "MUNDO_LIBRE":
        accion_jugador = escenario_mundo(ventana,jugador)
        estado = accion_jugador
        
    elif estado == "TIENDA":
        pygame.mixer.music.stop()
        reproducir_musica("tienda.mp3",bucle=True)
        accion_jugador = escenario_tienda(ventana,jugador)
        
        if accion_jugador == "SALIR":
            pygame.mixer.music.stop()
            reproducir_musica("mundo.mp3",bucle=True)
            estado = "MUNDO_LIBRE"
            
        elif accion_jugador == "COMPRAR":
            estado = mostrador(ventana,jugador,tienda)
            
    elif estado == "PELEANDO":
            pygame.mixer.music.stop()
            reproducir_musica("pelea.mp3", bucle=True) 
            
            accion_retorno = batalla(ventana, jugador)
            
            pygame.mixer.music.stop()
            reproducir_musica("mundo.mp3", bucle=True)
            
            estado = accion_retorno
pygame.quit()
