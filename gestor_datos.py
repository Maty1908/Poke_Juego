import json
import os
import Personaje
# Importamos la clase real desde tu archivo PokePlantilla.py
from pokemons.PokePlantilla import Pokemon 

def guardar_partida(jugador):
    """Convierte los datos complejos del objeto jugador a texto JSON."""
    lista_pokemons_serializada = []
    
    for poke in jugador.pokemons:

        lista_pokemons_serializada.append({
            "nombre": poke.nombre.lower() 
        })

    datos_a_guardar = {
        "billetera": jugador.billetera,
        "inventario": jugador.inventario,
        "ruta_spritesheet": jugador.ruta_spritesheet,
        "pokemons": lista_pokemons_serializada
    }
    
    with open("partida.json", "w") as archivo:
        json.dump(datos_a_guardar, archivo, indent=4)


def cargar_partida(ruta_defecto=None):
    
    if not os.path.exists("partida.json"):
        return None
        
    with open("partida.json", "r") as archivo:
        datos = json.load(archivo)
        
    ruta_skin = datos.get("ruta_spritesheet", ruta_defecto)
    
    # 1. Instanciamos al personaje real de Python
    nuevo_jugador = Personaje.personaje(ruta_skin)
    nuevo_jugador.billetera = datos.get("billetera", 100)
    nuevo_jugador.inventario = datos.get("inventario", {"pocion": 0, "revivir": 0})
    
    # 2. Reconstruimos los objetos Pokémon usando la clase real de PokePlantilla
    datos_pokes = datos.get("pokemons", [])
    lista_objetos_pokemon = []
    
    for datos_poke in datos_pokes:
        nombre_pokemon = datos_poke["nombre"]
        
        try:
            nuevo_poke = Pokemon(id=nombre_pokemon, es_jugador=True)
            lista_objetos_pokemon.append(nuevo_poke)
        except Exception as e:
            print(f"Error al conectar con la API para cargar a {nombre_pokemon}: {e}")
        
    nuevo_jugador.pokemons = lista_objetos_pokemon
    return nuevo_jugador
