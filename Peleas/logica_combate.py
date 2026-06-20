import random
import requests
# Importamos tu función original
from pokemons.Extraer_tipos import Extraer_tabla_tipos

# Ejecutamos tu función para generar el diccionario de debilidades/resistencias
Tabla_completa = Extraer_tabla_tipos()

def inicializar_equipo_combate(lista_pokemons_guardados):
    """
    Toma la lista de pokémons del jugador (sean diccionarios o instancias) 
    y extrae de forma segura el ID para consultar a la PokeAPI.
    """
    equipo_combate = []
    for p in lista_pokemons_guardados:
        # --- SOLUCIÓN AQUÍ ---
        # Si es un diccionario, usa p["id"]. Si es un objeto, usa p.id.
        if isinstance(p, dict):
            pokemon_id = p.get("id")
        else:
            pokemon_id = p.id if hasattr(p, 'id') else random.randint(1, 151)
            
        # Si por alguna razón el ID vino vacío, saltamos al siguiente
        if not pokemon_id:
            continue
        
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        try:
            res = requests.get(url).json()
            stats_base = {
                "id": res["id"],
                "nombre": res["name"].capitalize(),
                "vida_max": res["stats"][0]["base_stat"] * 2,
                "vida_actual": res["stats"][0]["base_stat"] * 2,
                "ataque": res["stats"][1]["base_stat"],
                "defense": res["stats"][2]["base_stat"],   
                "speed": res["stats"][5]["base_stat"],     
                "tipos": [t["type"]["name"] for t in res["types"]],
                "ataques": [{"nombre": m["move"]["name"].replace("-", " ").capitalize(), "tipo": "normal"} for m in res["moves"][:4]]
            }
            if not stats_base["ataques"]:
                stats_base["ataques"] = [{"nombre": "Placaje", "tipo": "normal"}]
            equipo_combate.append(stats_base)
        except Exception as e:
            print(f"Error al cargar pokémon lógico {pokemon_id}: {e}")
            
    return equipo_combate

def generar_equipo_rival(cantidad):
    rival_falso = []
    for _ in range(cantidad):
        # Creamos un objeto genérico simulando tener la propiedad 'id'
        rival_falso.append(type('PokemonDummy', (object,), {'id': random.randint(1, 151)}))
    return inicializar_equipo_combate(rival_falso)

def calcular_daño_recibido(pokemon_defensor, daño_base, tipo_ataque):
    multiplicador = 1.0
    # Validamos usando la tabla que generó tu script
    if Tabla_completa:
        for mi_tipo in pokemon_defensor["tipos"]:
            if mi_tipo in Tabla_completa:
                if tipo_ataque in Tabla_completa[mi_tipo].get("Inmune", {}):
                    multiplicador *= 0
                elif tipo_ataque in Tabla_completa[mi_tipo].get("Daño_mitad", {}):
                    multiplicador *= 0.5
                elif tipo_ataque in Tabla_completa[mi_tipo].get("Daño_Doble", {}):
                    multiplicador *= 2.0
                
    daño_final = int(daño_base * multiplicador)
    pokemon_defensor["vida_actual"] = max(0, pokemon_defensor["vida_actual"] - daño_final)
    return daño_final, multiplicador

def procesar_turno_logico(pkmn_atacante, pkmn_defensor, indice_ataque):
    """Esta es la función que calcula el golpe de cada turno"""
    ataque = pkmn_atacante["ataques"][indice_ataque]
    daño_base = pkmn_atacante["ataque"] // 2
    daño_final, mult = calcular_daño_recibido(pkmn_defensor, daño_base, ataque["tipo"])
    
    return {
        "nombre_ataque": ataque["nombre"],
        "daño": daño_final,
        "multiplicador": mult,
        "debilitado": pkmn_defensor["vida_actual"] <= 0}

def aplicar_consecuencias_billetera(jugador, gano_jugador):
    if gano_jugador:
        jugador.billetera += 25
    else:
        jugador.billetera = max(0, jugador.billetera - 50)
        for p in jugador.pokemons:
            if hasattr(p, 'curar'):
                p.curar()