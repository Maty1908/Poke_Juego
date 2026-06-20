import pygame,os


pygame.init()   #se pone esto primero ya que al importar las funciones con los escenarios
#                tiene que estar iniciado

from Seleccion.seleccion_personaje import menu_seleccion
from TIENDA.escenario_tienda import escenario_tienda
from Menu.MENU import menu_inicial
from Peleas.sprite_combate import batalla
from Mundo_libre.Escenario_mundo import escenario_mundo
import Personaje
import estilo
from TIENDA.tienda import Tienda
from TIENDA.mostrador import mostrador

ventana = pygame.display.set_mode((1064, 704))


estado = "MENU"

profe_elegido = None

ejecutar = True

while ejecutar:
    
    if estado == "MENU":
        eleccion_menu = menu_inicial(ventana,profe_elegido)
        estado = eleccion_menu
        
    elif estado == "SELECCION":

        profe_elegido = menu_seleccion(ventana)
        jugador = Personaje.personaje(os.path.join(estilo.DIRECTORIO_BASE, f"img/skins/{profe_elegido}/OV.png")) #creamos al jugador
        tienda = Tienda() #creamos a la tienda


        estado = "MUNDO_LIBRE"


    elif estado == "MUNDO_LIBRE":

        accion_jugador = escenario_mundo(ventana,jugador)
        estado = accion_jugador


    elif estado == "TIENDA":
        
        accion_jugador = escenario_tienda(ventana,jugador)

        if accion_jugador == "SALIR":
            estado = "MUNDO_LIBRE"

        elif accion_jugador == "COMPRAR":
            estado = mostrador(ventana,jugador,tienda)
           
 

    elif estado == "PELEANDO":

        resultado_pelea = batalla()
        if resultado_pelea == "ganaste":
            billetera = None #aca sumar plata al jugador instanciado o hacerlo dentro de batalla()
        estado = resultado_pelea


pygame.quit()
