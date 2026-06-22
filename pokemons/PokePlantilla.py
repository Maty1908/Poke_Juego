import requests,io

from pokemons.Extraer_tipos import Extraer_tabla_tipos

Tabla_completa = Extraer_tabla_tipos()

class Pokemon:
    def __init__(self, id, es_jugador=True):
        url = f"https://pokeapi.co/api/v2/pokemon/{(id)}"
        res = requests.get(url).json()
        
        self.id = res["id"]
        self.nombre = res["name"].capitalize()
        
        self.stats = {
            "vida_max": res["stats"][0]["base_stat"] * 2,
            "ataque": res["stats"][1]["base_stat"],
            "defensa": res["stats"][2]["base_stat"],
            "velocidad": res["stats"][5]["base_stat"]
        }
        self.vida_actual = self.stats["vida_max"]
        self.tipos = [t["type"]["name"] for t in res["types"]]
        
        vista = "back_default" if es_jugador else "front_default"
        try:
            url_gif = res["sprites"]["versions"]["generation-v"]["black-white"]["animated"][vista]
            self.gif_bytes = requests.get(url_gif).content
        except:
            self.gif_bytes = None
        # -----------------------------------------        
        self.ataques = []
        moves = res["moves"][:4]  
        
        for m in moves:
            nombre_ataque = m["move"]["name"].replace("-", " ").capitalize()
            url_ataque = m["move"]["url"]
            
            try:
                res_ataque = requests.get(url_ataque).json()
                tipo_ataque = res_ataque["type"]["name"]
                poder_ataque = res_ataque.get("power")
                if poder_ataque is None:
                    poder_ataque = 40
            except:
                tipo_ataque = "normal"
                poder_ataque = 40
            
            self.ataques.append({
                "nombre": nombre_ataque, 
                "poder": poder_ataque, 
                "tipo": tipo_ataque
            })
            
        if not self.ataques:
            self.ataques = [{"nombre": "Placaje", "poder": 40, "tipo": "normal"}]

    def calcular_daño_base(self, indice_ataque):
        ataque = self.ataques[indice_ataque]
        return (self.stats["ataque"] * ataque["poder"]) // 100 + 5

    def recibir_daño(self, daño_base, tipo_ataque):
        multiplicador = 1.0
        for mi_tipo in self.tipos:
            if mi_tipo in Tabla_completa:
                if tipo_ataque in Tabla_completa[mi_tipo]["Inmune"]:
                    multiplicador *= 0
                elif tipo_ataque in Tabla_completa[mi_tipo]["Daño_mitad"]:
                    multiplicador *= 0.5
                elif tipo_ataque in Tabla_completa[mi_tipo]["Daño_Doble"]:
                    multiplicador *= 2.0
                    
        daño_mitigado = daño_base / (1 + (self.stats["defensa"] / 100))
        daño_final = int(daño_mitigado * multiplicador)
        
        if daño_final == 0 and multiplicador > 0:
            daño_final = 1
            
        self.vida_actual = max(0, self.vida_actual - daño_final)
        return daño_final, multiplicador

    def curar(self):
        self.vida_actual = self.stats["vida_max"]
