from abc import ABC, abstractmethod


class Expression(ABC):

    def __init__(self, fila, columna, token):
        self.fila = fila
        self.columna = columna
        self.token = token

    @abstractmethod
    def operar(self, arbol):
        pass

    @abstractmethod
    def getFila(self):
        return self.fila

    @abstractmethod
    def getColumna(self):
        return self.columna

    @abstractmethod
    def getToken(self):
        return self.token

    @abstractmethod
    def setToken(self, token):
        self.token = token
