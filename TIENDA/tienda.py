import random,sys,os
import Personaje

class Tienda():   

    #clasificacion de pokemons por rareza (inventada por nosotros)
    POKEDEX = {
        "normal": {
            16: "Pidgey", 17: "Pidgeotto", 19: "Rattata", 20: "Raticate", 21: "Spearow", 22: "Fearow",
            23: "Ekans", 24: "Arbok", 27: "Sandshrew", 28: "Sandslash", 29: "Nidoran♀", 30: "Nidorina",
            32: "Nidoran♂", 33: "Nidorino", 41: "Zubat", 42: "Golbat", 43: "Oddish", 44: "Gloom",
            46: "Paras", 47: "Parasect", 48: "Venonat", 49: "Venomoth", 50: "Diglett", 51: "Dugtrio",
            52: "Meowth", 53: "Persian", 54: "Psyduck", 56: "Mankey", 57: "Primeape", 60: "Poliwag",
            61: "Poliwhirl", 66: "Machop", 69: "Bellsprout", 70: "Weepinbell", 72: "Tentacool",
            74: "Geodude", 75: "Graveler", 77: "Ponyta", 79: "Slowpoke", 81: "Magnemite",
            83: "Farfetch'd", 84: "Doduo", 85: "Dodrio", 86: "Seel", 88: "Grimer", 90: "Shellder",
            92: "Gastly", 93: "Haunter", 96: "Drowzee", 98: "Krabby", 99: "Kingler", 100: "Voltorb",
            102: "Exeggcute", 104: "Cubone", 109: "Koffing", 111: "Rhyhorn", 114: "Tangela",
            116: "Horsea", 117: "Seadra", 118: "Goldeen", 119: "Seaking", 120: "Staryu", 129: "Magikarp"
        },
        "especial": {
            1: "Bulbasaur", 2: "Ivysaur", 4: "Charmander", 5: "Charmeleon", 7: "Squirtle", 8: "Wartortle",
            10: "Caterpie", 11: "Metapod", 12: "Butterfree", 13: "Weedle", 14: "Kakuna", 15: "Beedrill",
            25: "Pikachu", 26: "Raichu", 35: "Clefairy", 37: "Vulpix", 39: "Jigglypuff", 55: "Golduck",
            58: "Growlithe", 62: "Poliwrath", 63: "Abra", 64: "Kadabra", 67: "Machoke", 73: "Tentacruel",
            78: "Rapidash", 80: "Slowbro", 82: "Magneton", 87: "Dewgong", 89: "Muk", 91: "Cloyster",
            97: "Hypno", 101: "Electrode", 105: "Marowak", 108: "Lickitung", 110: "Weezing",
            112: "Rhydon", 122: "Mr. Mime", 124: "Jynx", 128: "Tauros", 132: "Ditto", 133: "Eevee",
            147: "Dratini"
        },
        "rara": {
            3: "Venusaur", 6: "Charizard", 9: "Blastoise", 31: "Nidoqueen", 34: "Nidoking", 36: "Clefable",
            38: "Ninetales", 40: "Wigglytuff", 45: "Vileplume", 59: "Arcanine", 65: "Alakazam", 68: "Machamp",
            71: "Victreebel", 76: "Golem", 94: "Gengar", 95: "Onix", 103: "Exeggutor", 106: "Hitmonlee",
            107: "Hitmonchan", 113: "Chansey", 115: "Kangaskhan", 121: "Starmie", 123: "Scyther",
            125: "Electabuzz", 126: "Magmar", 127: "Pinsir", 130: "Gyarados", 131: "Lapras",
            134: "Vaporeon", 135: "Jolteon", 136: "Flareon", 137: "Porygon", 138: "Omanyte",
            139: "Omastar", 140: "Kabuto", 141: "Kabutops", 142: "Aerodactyl", 143: "Snorlax",
            148: "Dragonair", 149: "Dragonite"
        },
        "legendaria": {
            144: "Articuno", 145: "Zapdos", 146: "Moltres", 150: "Mewtwo", 151: "Mew"
        }
    }

    #---------------------------INICIADOR---------------------------------
    def __init__(self):
        self.cajas = {"normal": 50, "especial": 75, "rara": 125, "legendaria": 250} #cajas y precios
        self.objetos_tienda = {"pocion": 30, "revivir": 50} #objetos a vender

    #-----------------METODOS------------------------------------
    @staticmethod
    def pokemons_caja(tipo_caja):
        id_aleatorio = random.choice(list(Tienda.POKEDEX[tipo_caja].keys()))
        return id_aleatorio, Tienda.POKEDEX[tipo_caja][id_aleatorio]    
        # Elige una ID al azar de las llaves del tipo de caja y devuelve (ID, Nombre)
        #.keys() devuelve los ID de pokemones en la categoria seleccionada
        #Y antes metemos un list() asi podemos usar la funcion random.choice
        #que elige un elemento al azar de una LISTA

    def abrir_caja(self, jugador, tipo_de_caja):
    
            costo = self.cajas[tipo_de_caja]
            
            if jugador.billetera < costo:
                print("¡Saldo insuficiente!")
                return

            jugador.billetera -= costo  
            id_p, nombre_p = Tienda.pokemons_caja(tipo_de_caja) #guardamos ID y nombre del pokemon
            nuevo_pokemon = {"id": id_p, "nombre": nombre_p}    #de aca lo mandamos a otro lado y llamamos a la API
            
            #aca meter animacion de apertura con una llamada a otra funcion

            print(f"\n¡Te ha tocado un: {nombre_p.upper()}!")

            # --- CASO 1: Hay espacio libre en el equipo ---
            if len(jugador.pokemons) < 6:
                jugador.pokemons.append(nuevo_pokemon)
                print(f"¡{nombre_p.upper()} se ha añadido a tu equipo! ({len(jugador.pokemons)}/6)")
            
            # --- CASO 2: El equipo está lleno (Mecánica de Reemplazo) ---
            else:
                mecanica = None
                #meter mecanica de reemplazo
                
    def consultar_saldo(self):
        print(f"Hola tu saldo es de: {self.billetera}")

    def comprar_objeto(self, jugador, nombre_objeto):
            
            costo = self.objetos_tienda[nombre_objeto]

            if jugador.billetera >= costo:
                jugador.billetera -= costo
                jugador.inventario[nombre_objeto] += 1
                print(f"Compraste {nombre_objeto.upper()}.")
            else:
                print("¡No tienes suficiente dinero!")


tienda = Tienda()

nahu = Personaje.personaje()    #poner Personaje. para entrar al archivo

print(f"saldo: {nahu.billetera}")

print(f"inventario: {nahu.inventario}")

tienda.comprar_objeto(nahu,"pocion")

print(f"inventario: {nahu.inventario}")

print(f"saldo: {nahu.billetera}")

