from Extraer_tipos import Tabla_completa

#en cada tipo se esperan atributos unicos (tipo,resistencias,debilidades, efectividades,inmunidades)
#la tabla de tipos en la variable "Tabla_completa" se encuentra en el archivo "Extraer_tipos.py"


class Tipo:
    def __init__(self,nombre,relaciones_de_daño):
        self.nombre = nombre
        self.relaciones_de_daño = relaciones_de_daño.items()  #es un diccionario con el nombre del tipo y sus multiplicadores

#cada pokemon  tiene [vida,ataque,defensa,ataque especial,defensa especial,velocidad]

class Pokemon():

    def __init__(self,nombre,stats_base,ataques,tipo1,tipo2=None):
        self.nombre = nombre
        self.ataques = ataques
        self.stats = stats_base  #diccionario con stats sacado de pokeAPI
        self.tipo1 = tipo1       
        self.tipo2 = tipo2   
        
           
        self.__vida_actual = stats_base['vida']     #atributo para manejo de vida


    def Recibir_daño(self):    #forma de manejar calculos de daño
        pass



