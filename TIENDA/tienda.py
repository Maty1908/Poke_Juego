import random
import personaje

class Tienda(personaje):   #heredamos de la clase jugador para poder acceder a su dinero inicial

    @staticmethod
    def pokemons_caja(tipo_caja):

        pokedex = {"PNormales": {22:"zubat",66:"sandshrew"},
                   "PEspeciales": {1:"bulbasour",4:"charmander",7:"squirtle"},
                   "PRaros": {3:"venusaur",6:"charizard",9:"blastoise"},
                   "PLegendarios": {147:"articuno",148:"zapdos",149:"moltres",150:"mewtwo"}} #ID : pokemon 

        if tipo_caja in pokedex:
            id_aleatorio = random.choice(list(pokedex[tipo_caja].keys())) 
            return pokedex[tipo_caja][id_aleatorio]   # random.choice elige un elemento al azar de una lista.
        else:
            return "Lista vacía"
        

    #---------------------------INICIADOR---------------------------------

    def __init__(self,billetera):


        super().__init__(billetera)


        self.cajas = {"normal":50,"especial":75,"rara":125,"legendaria":250}


        self.__billetera = billetera        #ACA MANEJAMOS TODO EL DINERO DEL JUGADOR


        self.objetos = {"pocion":30,"revivir":50} #Objeto:Valor




    #-----------------SETTERS & GETTERS------------------------------

    @property
    def actualizar_billetera(self):
        return self.__billetera
    
    @actualizar_billetera.setter
    def actualizar_billetera(self,valor):
        self.__billetera = valor   



    #-----------------METODOS------------------------------------

    def abrir_caja(self, tipo_de_caja):
            # Verificamos si la caja existe en nuestro catálogo
            if tipo_de_caja in self.cajas:
                costo = self.cajas[tipo_de_caja]
                
                
                if self.__billetera >= costo:
                    self.actualizar_billetera -= costo 
                    
                    # Mapeamos el nombre de la caja a la categoria en la Pokedex
                    categorias = {
                        "normal": "PNormales",
                        "especial": "PEspeciales",
                        "rara": "PRaros",
                        "legendaria": "PLegendarios"
                    }
                    
                    categoria = categorias[tipo_de_caja]
                    pokemon_obtenido = Tienda.pokemons_caja(categoria)
                    print(f"¡Felicidades! Te ha tocado un: {pokemon_obtenido.upper()}")
                else:
                    print("¡Saldo insuficiente!!!!!")

    def consultar_saldo(self):
        print(f"Hola tu saldo es de: {self.__billetera}")

