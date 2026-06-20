import requests
from pokemons.Extraer_tipos import Tabla_completa

#en cada tipo se esperan atributos unicos (tipo,resistencias,debilidades, efectividades,inmunidades)
#la tabla de tipos en la variable "Tabla_completa" se encuentra en el archivo "Extraer_tipos.py"

class Pokemon:
    def __init__(self, id_or_name):
        # 1. Buscamos los datos en la PokeAPI de forma automática al crearlo
        url = f"https://pokeapi.co/api/v2/pokemon/{str(id_or_name).lower()}"
        res = requests.get(url).json()
        
        self.id = res["id"]
        self.nombre = res["name"].capitalize()
        
        # 2. Extraer Estadísticas Base
        self.stats = {
            "vida_max": res["stats"][0]["base_stat"] * 2, # Escalado simple para el juego
            "ataque": res["stats"][1]["base_stat"],
            "defensa": res["stats"][2]["base_stat"],
            "velocidad": res["stats"][5]["base_stat"]
        }
        self.vida_actual = self.stats["vida_max"]
        
        
        self.tipos = [t["type"]["name"] for t in res["types"]]
        
        # 4. Asignar 2 ataques aleatorios simples para el combate
        self.ataques = []
        moves = res["moves"][:4] # Tomamos los primeros por simplicidad, o al azar
        for m in moves:
            # Obtenemos info del ataque (suponiendo daño estándar)
            self.ataques.append({"nombre": m["move"]["name"].capitalize(), "poder": 40})
        if not self.ataques:
            self.ataques = [{"nombre": "Placaje", "poder": 40}]

    def recibir_daño(self, daño_base, tipo_ataque):
        # Buscamos el multiplicador en tu "Tabla_completa"
        multiplicador = 1.0
        
        # Evaluamos el tipo del ataque contra cada tipo del defensor
        for mi_tipo in self.tipos:
            if mi_tipo in Tabla_completa:
                # Comprobamos Inmunidad
                if tipo_ataque in Tabla_completa[mi_tipo]["Inmune"]:
                    multiplicador *= 0
                # Comprobamos Resistencia
                elif tipo_ataque in Tabla_completa[mi_tipo]["Daño_mitad"]:
                    multiplicador *= 0.5
                # Comprobamos Debilidad
                elif tipo_ataque in Tabla_completa[mi_tipo]["Daño_Doble"]:
                    multiplicador *= 2.0
                    
        
        daño_final = int(daño_base * multiplicador)
        self.vida_actual = max(0, self.vida_actual - daño_final)
        return daño_final, multiplicador

    def curar(self):
        self.vida_actual = self.stats["vida_max"]
