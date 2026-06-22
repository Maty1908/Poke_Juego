import json
import os

ARCHIVO_PARTIDA = "partida.json"

def guardar_partida(jugador):

    datos = {
        "billetera": jugador.billetera,
        "inventario": jugador.inventario,
        "posicion": {"x": jugador.forma.x, "y": jugador.forma.y},
        "ruta_skin": jugador.ruta_spritesheet # Guarda la skin
    }
    with open(ARCHIVO_PARTIDA, "w") as archivo:
        json.dump(datos, archivo, indent=4)
    print("Partida guardada exitosamente.")

def cargar_partida():
    if os.path.exists(ARCHIVO_PARTIDA):
        with open(ARCHIVO_PARTIDA, "r") as archivo:
            return json.load(archivo)
    return None