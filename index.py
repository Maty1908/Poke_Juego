import pygame
import sys

pygame.init()

from Seleccion.seleccion_personaje import menu_seleccion
from TIENDA.escenario_tienda import escenario_tienda
from Menu.MENU import menu_inicial

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

        estado = "MUNDO_LIBRE"


    elif estado == "MUNDO_LIBRE":

        variable_estado = "FUNCION DE MUNDO LIBRE"
        estado = variable_estado


    elif estado == "TIENDA":
        escenario_tienda(ventana, profe_elegido)

    elif estado == "PELEANDO":
        resultado_pelea = "FUNCION DE PELEA"
        estado = resultado_pelea


pygame.quit()