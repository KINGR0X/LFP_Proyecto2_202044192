from Abstract.abstract import Expression


class Errores(Expression):

    def __init__(self, lexema, fila, columna, token):
        self.lexema = lexema
        super().__init__(fila, columna, token)

    def operar(self, no):
        tipo = 'Error Lexico'
        fila = f'{self.fila}'
        columna = f'{self.columna}'
        lex = f'{self.lexema}'
        desc = f'no se reconoce el lexema'

        return tipo, fila, columna, lex, desc

    def getColumna(self):
        return super().getColumna()

    def getFila(self):
        return super().getFila()

    def getToken(self):
        return super().getToken()

    def setToken(self, token):
        super().setToken("Error")
