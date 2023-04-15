from Abstract.abstract import Expression


class Lexema(Expression):

    def __init__(self, lexema, fila, columna, token):
        self.lexema = lexema
        super().__init__(fila, columna, token)

    # es practicamente un get
    def operar(self, arbol):
        return self.lexema

    def getFila(self):
        return super().getFila()

    def getColumna(self):
        return super().getColumna()

    def getToken(self):
        return super().getToken()
