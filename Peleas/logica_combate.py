import random
from pokemons.PokePlantilla import Pokemon

def generar_equipo_rival(cantidad):
    """Genera una lista de objetos Pokemon aleatorios para el rival"""
    equipo_rival = []
    for _ in range(cantidad):
        id_aleatorio = random.randint(1, 151)
        
        equipo_rival.append(Pokemon(id_aleatorio, es_jugador=False))
    return equipo_rival

def procesar_turno_logico(pkmn_atacante, pkmn_defensor, indice_ataque):
    """Conecta la acción del atacante con la reacción del defensor"""
    ataque = pkmn_atacante.ataques[indice_ataque]
    
    # 1. El atacante nos dice su daño base
    daño_base = pkmn_atacante.calcular_daño_base(indice_ataque)
    
    # 2. El defensor procesa el daño usando sus stats y tipos
    daño_final, mult = pkmn_defensor.recibir_daño(daño_base, ataque["tipo"])
    
    return {
        "nombre_ataque": ataque["nombre"],
        "daño": daño_final,
        "multiplicador": mult,
        "debilitado": pkmn_defensor.vida_actual <= 0
    }

def aplicar_consecuencias_billetera(jugador, gano_jugador):
    if gano_jugador:
        jugador.billetera += 25
    else:
        jugador.billetera = max(0, jugador.billetera - 50)
        # Curamos a todos los pokemons del jugador usando su método propio
        for p in jugador.pokemons:
            p.curar()
