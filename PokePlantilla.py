from abc import ABC,abstractmethod


#en cada tipo se esperan atributos unicos (tipo,resistencias,debilidades, efectividades,inmunidades)
#lista de tipos:
#(gen1): ["Acero","Agua","Bicho","Dragón", "Eléctrico","Fantasma","Fuego","Hielo","Lucha", 
# "Normal","Planta","Psíquico", "Roca","Siniestro","Tierra","Veneno","Volador"]

class Tipo:
    def __init__(self,nombre,relaciones_de_daño):
        self.nombre = nombre
        self.relaciones_de_daño = relaciones_de_daño  #un diccionario con debilidades, resistencias e inmunidades(multiplicadores)


#cada pokemon  tiene [vida,ataque,defensa,ataque especial,defensa especial,velocidad]

class Pokemon():

    def __init__(self,nombre,stats_base,tipo1,tipo2=None):
        self.nombre = nombre
        self.stats = stats_base  #diccionario con stats
        self.tipo1 = tipo1       
        self.tipo2 = tipo2      
        self.__vida_actual = stats_base['vida']


    def Recibir_daño(self):    #forma de manejar calculos de daño
        pass

