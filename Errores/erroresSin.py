from Abstract.abstract import Expression


class ErrorSintac(Expression):

    def __init__(self, lexema, fila, columna, token):
        self.lexema = lexema
        super().__init__(fila, columna, token)

    def operar(self, no):
        tipo = 'Tipo: Error Sintactico\n'
        fila = f'Fila: {self.fila}\n'
        columna = f'Columna: {self.columna}\n'
        token = f'Token: {self.token}\n'
        desc = f'Descripcion: Falta el token {self.token}'

        return '\n' + tipo + fila + columna + token + desc + "\n"

    def getColumna(self):
        return super().getColumna()

    def getFila(self):
        return super().getFila()

    def getToken(self):
        return super().getToken()

    def setToken(self, token):
        super().setToken(token)
