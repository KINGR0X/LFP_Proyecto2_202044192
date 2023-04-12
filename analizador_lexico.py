from Abstract.lexema import *
from Errores.errores import *

global n_linea
global n_columna
global lista_lexemas
global lista_errores

n_linea = 1
n_columna = 1
lista_lexemas = []
lista_errores = []


def instruccion(cadena):
    global n_linea
    global n_columna
    global lista_lexemas
    lexema = ""
    puntero = 0

    while cadena:
        char = cadena[puntero]
        puntero += 1

        if char.isalpha():

            # se envia al metodo la cadena desde el puntero hasta el final
            lexema, cadena = armar_lexema(cadena[puntero-1:])

            # si no es None lexema entonces
            if lexema:

                # Armado de lexema como clase
                l = Lexema(lexema, n_linea, n_columna)

                # se guarda el lexema en la lista
                lista_lexemas.append(l)

                n_columna += len(lexema)
                puntero = 0

        elif char == "=":
            # Armado de lexema como clase
            c = Lexema(char, n_linea, n_columna)

            n_columna += 1
            lista_lexemas.append(c)
            cadena = cadena[1:]
            puntero = 0

        elif char == '(':
            # se envia al metodo la cadena sin la comilla inicial
            lexema, cadena = armar_data(cadena[puntero:])
            # si no es None ninguna de las dos condiciones entonces
            if lexema and cadena:
                # +1 por el parentesis
                n_columna += 1

                # Armado de lexema como clase
                l = Lexema(lexema, n_linea, n_columna)

                # se guarda el lexema en la lista
                lista_lexemas.append(l)

                # por el parentesis
                n_columna += len(lexema)+1
                puntero = 0

        elif char == ',':
            # se envia al metodo la cadena sin la comilla inicial
            lexema, cadena = armar_json(cadena[puntero:])
            # si no es None ninguna de las dos condiciones entonces
            if lexema and cadena:

                # Armado de lexema como clase
                l = Lexema(lexema, n_linea, n_columna)

                # se guarda el lexema en la lista
                lista_lexemas.append(l)

                n_columna += len(lexema)
                puntero = 0

        elif char == '{':
            # Armado de lexema como clase
            c = Lexema(char, n_linea, n_columna)

            n_columna += 1
            lista_lexemas.append(c)
            cadena = cadena[1:]
            puntero = 0

        elif char == '}':
            # Armado de lexema como clase
            c = Lexema(char, n_linea, n_columna)

            n_columna += 1
            lista_lexemas.append(c)
            cadena = cadena[1:]
            puntero = 0

        # simbolos a ignorara
        elif char == "\t":
            cadena = cadena[4:]
            n_columna += 4
            puntero = 0

        elif char == "\n":
            cadena = cadena[1:]
            n_columna = 0
            n_linea += 1
            puntero = 0

        elif char == ";":
            cadena = cadena[1:]
            n_columna = 0
            n_linea += 1
            puntero = 0

        elif char == ' ' or char == '\r' or char == ':' or char == '.':
            cadena = cadena[1:]
            n_columna += 1
            puntero = 0

        else:
            cadena = cadena[1:]
            puntero = 0
            n_columna += 1
            lista_errores.append(Errores(char, n_linea, n_columna))

    i = 0

    # for lexema in lista_lexemas:
    #     i = i+1
    #     print(i, lexema.operar(None))

    return lista_lexemas


def armar_lexema(cadena):
    global n_linea
    global n_columna
    global lista_lexemas
    lexema = ""
    puntero = ""
    # se recorre toda la cadena con el puntero hasta encontrar un espacio en blanco
    for char in cadena:
        puntero += char
        if char == ' ' or char == ';' or char == "(":
            # en cadena el slicing devuelce desde uno antes del puntero hasta el final
            return lexema, cadena[len(puntero)-1:]
        else:
            # se va agregando letra por letra al lexema
            lexema += char
    # para evitar que se detenga el problema en caso de un error
    return None, None


def armar_data(cadena):
    global n_linea
    global n_columna
    global lista_lexemas
    lexema = ""
    puntero = ""
    # se recorre toda la cadena con el puntero hasta encontrar un espacio en blanco
    for char in cadena:
        puntero += char

        if char == '{' or char == "\n":
            n_linea += 1

        if char == ')' or char == ',':
            # en cadena el slicing devuelce desde uno antes del puntero hasta el final
            return lexema, cadena[len(puntero)-1:]

        else:
            # se va agregando letra por letra al lexema
            lexema += char
    # para evitar que se detenga el problema en caso de un error
    return None, None


def armar_json(cadena):
    global n_linea
    global n_columna
    global lista_lexemas
    lexema = ""
    puntero = ""
    # se recorre toda la cadena con el puntero hasta encontrar un espacio en blanco
    for char in cadena:
        puntero += char
        if char == ')':
            # en cadena el slicing devuelce desde uno antes del puntero hasta el final
            return lexema, cadena[len(puntero)-1:]

        else:
            # se va agregando letra por letra al lexema
            lexema += char
    # para evitar que se detenga el problema en caso de un error
    return None, None

# === Es una prueba, aun esta muy verde===


def TablaTokens():

    global lista_lexemas

    for i in range(len(lista_lexemas)):
        print("=====================================")
        print("Lexema ==>", lista_lexemas[i].operar(None))
        print("Fila ==>", lista_lexemas[i].getFila())
        print("Columna ==>", lista_lexemas[i].getColumna())


cadenaP = '''

CrearBD ejemplo = nueva CrearBD("Data");

EliminarBD elimina = nueva EliminarBD("Data");

CrearColeccion colec = nueva CrearColeccion(“NombreColeccion”);

InsertarUnico insertadoc = nueva InsertarUnico(“NombreColeccion” ,
“
    { 
        "nombre" : "Obra Literaria", 
        "autor" : "Jorge Luis" 
    } 
”); 

ActualizarUnico actualizadoc = nueva ActualizarUnico(“NombreColeccion”, 
“
    { 
        "nombre" : "Obra Literaria" 
    }, 
    { 
        $set: {"autor" : "Mario Vargas"} 
    } 
”);

'''


entrada = '''

CrearBD ejemplo = nueva CrearBD(); 

EliminarBD elimina = nueva EliminarBD(); 

CrearColeccion colec = nueva CrearColeccion(“NombreColeccion”); 

InsertarUnico insertadoc = nueva InsertarUnico(“NombreColeccion” ,
“
    { 
        "nombre" : "Obra Literaria", 
        "autor" : "Jorge Luis" 
    } 
”); 

ActualizarUnico actualizadoc = nueva ActualizarUnico(“NombreColeccion”, 
“
    { 
        "nombre" : "Obra Literaria" 
    }, 
    { 
        $set: {"autor" : "Mario Vargas"} 
    } 
”);

EliminarUnico eliminadoc = nueva EliminarUnico(“NombreColeccion”,
“
    { 
        "nombre" : "Obra Literaria" 
    } 
”);

BuscarTodo todo = nueva BuscarTodo (“NombreColeccion”); 

BuscarUnico todo = nueva BuscarUnico (“NombreColeccion”); 
'''

instruccion(cadenaP)

TablaTokens()
