from Abstract.abstract import Expression


class ErrorSintac(Expression):

    def __init__(self, lexema, fila, columna, token):
        self.lexema = lexema
        super().__init__(fila, columna, token)

    def operar(self, no):
        tipo = 'Error Sintactico'
        fila = f'{self.fila}'
        columna = f'{self.columna}'
        token = f'{self.token}'
        desc = f'Falta el token {self.token}'

        return tipo, fila, columna, token, desc

    def getColumna(self):
        return super().getColumna()

    def getFila(self):
        return super().getFila()

    def getToken(self):
        return super().getToken()

    def setToken(self, token):
        super().setToken(token)

    # def getDescripcion(token):
    #     return f "Error: falta el token{self.token}"
