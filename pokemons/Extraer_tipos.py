import requests

#usamos este script para obtener las debilidades,resistencias,inmunidades y efectividades de todos los tipos
#preferimos armar este codigo antes que cargar a mano un diccionario con todos los valores uno por uno

#El diccionario que retorna contiene una diccionarios dentro
#cada uno de ellos tiene como KEY el nombre del tipo y el VALUE es otro diccionario
#con sus debilidades, resistencias e inmunidades en valores numericos
#esto para luego a la hora de recibir el daño se le aplique este multiplicador

Tipos_Gen3 = ["normal", "fire", "water", "electric", "grass", "ice",
        "fighting", "poison", "ground", "flying", "psychic",
        "bug", "rock", "ghost", "dragon", "steel", "dark"]      #iterable



def Extraer_tabla_tipos():

    Tabla_de_tipos = {}    # diccionario con todos los tipos


    for tipo in Tipos_Gen3:

        Tabla_de_tipos[tipo] = {
            "Daño_Doble" :{},
            "Daño_mitad":{},
            "Inmune":{} }      #variable local para agregar a "Tabla_de_tipos"


        try:
            url = f"https://pokeapi.co/api/v2/type/{tipo}"

            respuesta = requests.get(url)

            if respuesta.status_code == 200:
                json = respuesta.json()
                relaciones_daños = json["damage_relations"]

                #INMUNIDADES
            
                for t in relaciones_daños["no_damage_from"]:
                    Nombre_tipo = t["name"]

                    if Nombre_tipo in Tipos_Gen3:
                        Tabla_de_tipos[tipo]["Inmune"][Nombre_tipo] = 0


                #RESISTENCIAS

                for t in relaciones_daños["half_damage_from"]:
                    Nombre_tipo = t["name"]

                    if Nombre_tipo in Tipos_Gen3:
                        Tabla_de_tipos[tipo]["Daño_mitad"][Nombre_tipo] = 0.5


                #DAÑO DOBLE

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


Tabla_completa = Extraer_tabla_tipos() #datos

