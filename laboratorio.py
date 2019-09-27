import re

# Función para ordenar los tokens
def takeThird(elem):
    return elem[2]

# Clase scanner
class scanner():
    """

        Esta clase recibe como entrada un archivo de texto y permite obtener los tokens utlizando expresiones regulares.
        Retorna error en caso de no poder analizar texto de entrada
        
    """
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
                #archivo = open("prueba.txt")
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


# Clase arbol
class arbol():
    """

        Esta clase tiene la función de crear un arbol de sintaxis abtracta (AST).
        Permite agregar hijos, valor e imprimir el árbol visualmente.
        
    """
    def __init__(self, valor = ""):
        self.elemento = valor
        self.hijos = []
        self.elehijos = []
            
    def agregar(self, elemento, elemento2):
        self.hijos.append(elemento)
        self.elehijos.append(elemento2)

    def setValor(self, valor):
        self.elemento = valor

    def limpiar(self):
        self.elemento = ""
        self.hijos = []

    def ver(self):
        print(self.elemento)
        for hijos in self.hijos:
            print("---->")
            i = 0
            largo = len(hijos)
            while(i < largo):
                if(i == 0):
                    print("    ", hijos[i])
                else:
                    print("    "*2,"---->", hijos[i], "   ---->  ", self.elehijos[0][i])
                i += 1


# Clase parser
class parser():
    """

        Esta clase verifica que los tokens sean recibidos de la manera correcta.
        Retorna error en caso de no recibir el token esperado mostrando el detalle.

    """
    def __init__(self, TOKENS, ARBOL): 
        self.AST = ARBOL
        self.FALLO = True
        self.ASTLIST = []
        self.TOKENLIST = []
        self.TOKENS = TOKENS
        self.TOKEN = TOKENS[0][0]
        self.TOKENVALUE = TOKENS[0][1]
        self.CONTADOR = -1
        self.EXIST = len(self.TOKENS)-1
        
    def nextt(self): # Método que retorna el siguiente token en la lista
        self.CONTADOR += 1
        self.TOKEN = self.TOKENS[self.CONTADOR][0]
        self.TOKENVALUE = self.TOKENS[self.CONTADOR][1]

    def nexte(self): # Método que verifica si existe un siguiente token
        return self.CONTADOR < self.EXIST

    #def direccion(self):
    #    pass

    def direccionTica(self):
        """

            Este método se encarga de iniciar el proceso de Parsing

        """
        while(self.nexte() and self.FALLO):
            self.nextt()
            self.ASTLIST = []
            self.TOKENLIST = [""]
            self.ASTLIST.append("Direccion")
            self.inicio()
            if(self.FALLO):
                self.AST.agregar(self.ASTLIST, self.TOKENLIST)
        self.AST.ver()
            
        
    def inicio(self): # Comienza el recorrido de clase tipo token Inicio
        if(self.TOKEN == "Inicio"):
            self.ASTLIST.append("Inicio")
            self.TOKENLIST.append(self.TOKENVALUE)
            self.nextt()
            self.lugar()
        else:
            self.error("Se esperaba recibir el Token 'Inicio',", self.TOKEN)
            
    def lugar(self): # Comienza el recorrido de clase tipo token Lugar
        if(self.TOKEN == "Lugar"):
            self.ASTLIST.append("Lugar")
            self.TOKENLIST.append(self.TOKENVALUE)
            self.nextt()
            self.detalles()
        else:
            self.error("Se esperaba recibir el Token 'Lugar',", self.TOKEN)

    def detalles(self): # Comienza el recorrido de clase tipo token Detalles
        if(self.TOKEN == "Detalles"):
            self.ASTLIST.append("Detalles")
            self.TOKENLIST.append(self.TOKENVALUE)
            self.nextt()
            self.distancia()
        else:
            self.error("Se esperaba recibir el Token 'Detalles',", self.TOKEN)

    def distancia(self): # Comienza el recorrido de clase tipo token Distancia
        if(self.TOKEN == "Distancia"):
            self.ASTLIST.append("Distancia")
            self.TOKENLIST.append(self.TOKENVALUE)
            self.nextt()
            self.medida()
        else:
            self.error("Se esperaba recibir el Token 'Distancia',", self.TOKEN)

    def medida(self): # Comienza el recorrido de clase tipo token Medida
        if(self.TOKEN == "Medida"):
            self.ASTLIST.append("Medida")
            self.TOKENLIST.append(self.TOKENVALUE)
            self.nextt()
            self.conectores()
        else:
            self.error("Se esperaba recibir el Token 'Medida',", self.TOKEN)

    def conectores(self): # Comienza el recorrido de clase tipo token Conectores
        if(self.TOKEN == "Conectores"):
            self.ASTLIST.append("Conectores")
            self.TOKENLIST.append(self.TOKENVALUE)
            self.nextt()
            self.cardinales()
        else:
            self.error("Se esperaba recibir el Token 'Conectores',", self.TOKEN)

    def cardinales(self): # Comienza el recorrido de clase tipo token Cardinales
        if(self.TOKEN == "Cardinales"):
            self.ASTLIST.append("Cardinales")
            self.TOKENLIST.append(self.TOKENVALUE)
            self.nextt()
            self.fin()
        else:
            self.error("Se esperaba recibir el Token 'Cardinales',", self.TOKEN)

    def fin(self): # Comienza el recorrido de clase tipo token Fin
        if(self.TOKEN == "Fin"):
            self.ASTLIST.append("Fin")
            self.TOKENLIST.append(self.TOKENVALUE)
        else:
            self.error("Se esperaba recibir el Token 'Fin',", self.TOKEN)

    def error(self, error, esperado):# En caso de que el recorrido no encuentre equivalencia de tipo dará error
        print("ERROR:", error, "se recibió el token '"+esperado+"'")
        print()
        self.FALLO = False
        self.AST.agregar(self.ASTLIST, self.TOKENLIST)


# Función principal
if(__name__ == '__main__'):
    """

        En función principal se crean los objetos de las clases para ejecutar el programa.
        Se crea el Scanner, AST y Parser.

    """
    scanner = scanner()
    scanner.agregar()
    scanner.generador_tokens()
    scanner.imprimir_tokens()
    arbol = arbol("DireccionTica")
    parser = parser(scanner.TOKENS, arbol)
    parser.direccionTica()
