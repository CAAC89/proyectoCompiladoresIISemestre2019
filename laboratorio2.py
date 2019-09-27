import re

# Función para ordenar los tokens
def takeThird(elem):
    return elem[2]

# Clase scanner
class scanner():
    def __init__(self):
        # Se definen las expresiones regulares de los tokens y variables
        self.LISTARE = []
        self.INICIO = re.compile('(Del|De la)\s')
        self.LUGAR = re.compile('"([a-z]|\s)+"')
        self.DISTANCIA = re.compile('[1-9][0-9]*\s')
        self.MEDIDA = re.compile('(cuadras|metros|kilometros)\s')
        self.CONECTORES = re.compile('(y|hasta|si no|hacia el|hacia la|hasta la)\s')
        self.CARDINALES = re.compile('(norte|sur|este|oeste|arriba|abajo|derecha|izquierda)')
        self.DETALLES = re.compile('([a-z]|\s)+')
        self.FIN = re.compile("(\.|\n)+")
        self.TEXTO = ''
        self.TEXTORIGINAL = ''
        self.TOKENS = []

    # Método agregar, agrega las expresiones regulares a una lista
    def agregar(self):
        # Se lee el archivo de entrada
        archivo = ""
        while(archivo == ""):
            try:
                archivo = open(input("Ingrese el archivo: "))
                self.TEXTO = archivo.read()
            except:
                pass
        self.TEXTORIGINAL = self.TEXTO
        self.LISTARE.append((self.INICIO,"Inicio"))
        self.LISTARE.append((self.LUGAR,"Lugar"))
        self.LISTARE.append((self.DISTANCIA,"Distancia"))
        self.LISTARE.append((self.MEDIDA,"Medida"))
        self.LISTARE.append((self.CONECTORES,"Conectores"))
        self.LISTARE.append((self.CARDINALES,"Cardinales"))
        self.LISTARE.append((self.FIN,"Fin"))
        self.LISTARE.append((self.DETALLES,"Detalles"))

    # Método que genera los tokens a partir de las expresiones regulares
    def generador_tokens(self):
        i = 0
        largo = len(self.LISTARE)
        # Se buscan coincidencias de las expresiones regulares 
        while(i < largo):
            if(self.LISTARE[i][0].search(self.TEXTO) != None):
                while(self.LISTARE[i][0].search(self.TEXTO) != None):
                    token = self.LISTARE[i][0].search(self.TEXTO)[0]
                    cambio = len(token) * "#"
                    self.TOKENS.append((self.LISTARE[i][1],token,self.LISTARE[i][0].search(self.TEXTO).start()))
                    self.TEXTO = self.TEXTO.replace(token,cambio,1)
                i += 1
            else:
                #print("Error: No se encuentra ningún token de tipo <", self.LISTARE[i][1],">")
                i += 1
        # Se verifica si en el texto quedan caracteres inválidos 
        patron = re.compile('.+')
        self.TEXTO = self.TEXTO.replace("#","\n")
        for m in patron.finditer(self.TEXTO):
            print("Error: El caracter <",m.group(),"> no es válido. Posición inicial:",m.start(),"- Posición final:",m.end())

    # Función que imprime los tokens en pantalla
    def imprimir_tokens(self):
        print()
        print("Lista de TOKENS")
        print()
        self.TOKENS.sort(key=takeThird)
        for token in self.TOKENS:
            
            print('<"'+token[0]+'", "'+token[1],'">')
        print()

# Clase parser
class parser():#Estas son las variables que inicializan el parser, los tokens que vienen del scanner son enviados aca al parser
    def __init__(self, TOKENS):
        self.TOKENS = TOKENS   #token
        self.TOKEN = TOKENS[0][0]  # cabecera de token
        self.TOKENVALUE = TOKENS[0][1] # valor de token
        self.CONTADOR = -1  # contador
        self.EXIST = len(self.TOKENS)-1  #contador verifica si existe
        
    def nextt(self):# función que aumenta en 1 para seguir recorriendo
        self.CONTADOR += 1
        self.TOKEN = self.TOKENS[self.CONTADOR][0]

    def nexte(self):#verifica si hay existencia o sea exist debe ser mayor a contador
        return self.CONTADOR < self.EXIST

    def direccion(self):
        pass

    def direccionTica(self):# hace el recorrido de inicio hasta fin finalizar
        while(self.nexte()):
            self.nextt()
            self.inicio()
        
    def inicio(self): # comienza el recorrido de clase tipo token inicio
        if(self.TOKEN == "Inicio"):
            self.nextt()
            self.lugar()
        else:
            self.error("Se esperaba recibir el Token 'Inicio',", self.TOKEN)
            
    def lugar(self):# comienza el recorrido de clase tipo token lugar
        if(self.TOKEN == "Lugar"):
            self.nextt()
            self.detalles()
        else:
            self.error("Se esperaba recibir el Token 'Lugar',", self.TOKEN)

    def detalles(self):# comienza el recorrido de clase tipo token detalles
        if(self.TOKEN == "Detalles"):
            self.nextt()
            self.distancia()
        else:
            self.error("Se esperaba recibir el Token 'Detalles',", self.TOKEN)

    def distancia(self):# comienza el recorrido de clase tipo token distancia
        if(self.TOKEN == "Distancia"):
            self.nextt()
            self.medida()
        else:
            self.error("Se esperaba recibir el Token 'Distancia',", self.TOKEN)

    def medida(self): # comienza el recorrido de clase tipo token medida
        if(self.TOKEN == "Medida"):
            self.nextt()
            self.conectores()
        else:
            self.error("Se esperaba recibir el Token 'Medida',", self.TOKEN)

    def conectores(self): # comienza el recorrido de clase tipo token conectores
        if(self.TOKEN == "Conectores"):
            self.nextt()
            self.cardinales()
        else:
            self.error("Se esperaba recibir el Token 'Conectores',", self.TOKEN)

    def cardinales(self):# comienza el recorrido de clase tipo token cardinales
        if(self.TOKEN == "Cardinales"):
            self.nextt()
            self.fin()
        else:
            self.error("Se esperaba recibir el Token 'Cardinales',", self.TOKEN)

    def fin(self):# comienza el recorrido de clase tipo token fin
        if(self.TOKEN == "Fin"):
            pass
        else:
            self.error("Se esperaba recibir el Token 'Fin',", self.TOKEN)

    def error(self, error, esperado):#en caso de que el recorrido no encuentre equivalencia de tipo dará error
        print(error, "se recibió el token '"+esperado+"'")


# Función principal
if(__name__ == '__main__'):
    scanner = scanner()
    scanner.agregar()
    scanner.generador_tokens()
    scanner.imprimir_tokens()
    parser = parser(scanner.TOKENS)# se envían los tokens
    parser.direccionTica() # se hace recorrido y se va imprimiendo el parser
