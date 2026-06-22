import requests


Tipos_Gen3 = ["normal", "fire", "water", "electric", "grass", "ice",
        "fighting", "poison", "ground", "flying", "psychic",
        "bug", "rock", "ghost", "dragon", "steel", "dark"] 



def Extraer_tabla_tipos():

    Tabla_de_tipos = {}


    for tipo in Tipos_Gen3:

        Tabla_de_tipos[tipo] = {
            "Daño_Doble" :{},
            "Daño_mitad":{},
            "Inmune":{} }


        try:
            url = f"https://pokeapi.co/api/v2/type/{tipo}"

            respuesta = requests.get(url)

            if respuesta.status_code == 200:
                json = respuesta.json()
                relaciones_daños = json["damage_relations"]
            
                for t in relaciones_daños["no_damage_from"]:
                    Nombre_tipo = t["name"]

                    if Nombre_tipo in Tipos_Gen3:
                        Tabla_de_tipos[tipo]["Inmune"][Nombre_tipo] = 0

                for t in relaciones_daños["half_damage_from"]:
                    Nombre_tipo = t["name"]

                    if Nombre_tipo in Tipos_Gen3:
                        Tabla_de_tipos[tipo]["Daño_mitad"][Nombre_tipo] = 0.5

                    
                for t in relaciones_daños["double_damage_from"]:
                    Nombre_tipo = t["name"]

                    if Nombre_tipo in Tipos_Gen3:
                        Tabla_de_tipos[tipo]["Daño_Doble"][Nombre_tipo] = 2.0



            elif respuesta.status_code == 404:
                return None
            
            elif respuesta.status_code == 500:
                print("Error en el servidor")

        except requests.exceptions.RequestException: 
            print(f"Error en el tipo: {tipo}")
            return None
        
    return Tabla_de_tipos
