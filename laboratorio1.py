import re

class scanner():
    def __init__(self):
        self.LISTARE = []
        self.INICIO = re.compile('(Del|De la)\s')
        self.LUGAR = re.compile('"([a-z]|\s)+"')
        self.DISTANCIA = re.compile('[1-9][0-9]*\s')
        self.MEDIDA = re.compile('(cuadras|metros|kilometros)\s')
        self.CONECTORES = re.compile('(y|hasta|si no|hacia el|hacia la|hasta la)\s')
        self.CARDINALES = re.compile('(norte|sur|este|oeste|arriba|abajo|derecha|izquierda)')
        self.DETALLES = re.compile('([a-z]|\s)+')
        self.PUNTO = re.compile("\.")
        self.TEXTO = ''
        self.TEXTORIGINAL = ''
        self.TOKENS = []

    def agregar(self):
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
        self.LISTARE.append((self.DETALLES,"Detalles"))
        self.LISTARE.append((self.PUNTO,"Punto"))

    def todo(self):
        i = 0
        largo = len(self.LISTARE)
        while(i < largo):
            if(self.LISTARE[i][0].search(self.TEXTO) != None):
                while(self.LISTARE[i][0].search(self.TEXTO) != None):
                    token = self.LISTARE[i][0].search(self.TEXTO)[0]
                    cambio = len(token) * "#"
                    self.TOKENS.append((self.LISTARE[i][1],token))
                    self.TEXTO = self.TEXTO.replace(token,cambio,1)
                i += 1
            else:
                print("Error", self.LISTARE[i][1])
                i += 1
				

    def error(self, detalle):
        print("Error de token",detalle)
        

if(__name__ == '__main__'):
    scanner = scanner()
    scanner.agregar()
    scanner.todo()
    print(scanner.TOKENS)