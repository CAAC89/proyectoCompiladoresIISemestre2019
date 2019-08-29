import re

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
        self.LISTARE.append((self.CARDINALES,"cardinales"))
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
                    self.TOKENS.append((self.LISTARE[i][1],token))
                    self.TEXTO = self.TEXTO.replace(token,cambio,1)
                i += 1
            else:
                print("Error: No se encuentra ningún token de tipo <", self.LISTARE[i][1],">")
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
        for token in self.TOKENS:
            print('<"'+token[0]+'", "'+token[1]+'">')
        
# Función principal
if(__name__ == '__main__'):
    scanner = scanner()
    scanner.agregar()
    scanner.generador_tokens()
    scanner.imprimir_tokens()
