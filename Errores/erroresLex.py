from Abstract.abstract import Expression


class Errores(Expression):

    def __init__(self, lexema, fila, columna, token):
        self.lexema = lexema
        super().__init__(fila, columna, token)

    def operar(self, no):
        tipo = 'Tipo: Error Lexico\n'
        fila = f'Fila: {self.fila}\n'
        columna = f'Columna: {self.columna}\n'
        lex = f'Lexema: {self.lexema}\n'
        desc = f'Descripcion: Error Lexico, no se reconoce el lexema\n'

        return '\n' + tipo + fila + columna + lex + desc

    def getColumna(self):
        return super().getColumna()

    def getFila(self):
        return super().getFila()

    def getToken(self):
        return super().getToken()

    def setToken(self, token):
        super().setToken("Error")
