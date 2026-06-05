import io
import sys
import paygame
import requests 

# Inicialisamos paygame 
paygame.init()

# Configuracion ventana 
ancho_ventana = 1064
alto_ventana = 582
ventana = paygame.display.set_mode((ancho_ventana, alto_ventana))

# Definimos un reloj para los movimientos fluidos 
reloj = paygame.time.clock()