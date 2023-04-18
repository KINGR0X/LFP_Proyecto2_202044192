from Abstract.lexema import *
from Errores.errores import *

#  token | lexema
reserved = {
    "Funcion_CrearBD": "CrearBD",
    "Funcion_EliminarBD": "EliminarBD",
    "Funcion_CrearColeccion": "CrearColeccion",
    "Funcion_EliminarColeccion": "EliminarColeccion",
    "Funcion_insertarUnico": "InsertarUnico",
    "Funcion_ActualizarUnico": "ActualizarUnico",
    "Funcion_EliminarUnico": "EliminarUnico",
    "Funcion_BuscarTodo": "BuscarTodo",
    "Funcion_BuscarUnico": "BuscarUnico",
    "Reservada_nueva": "nueva",
    "Argumento": "argumento",
    "Parte_json": "parte_json",
    "Igual": "=",
    "Parentesis_izquierdo": "(",
    "Parentesis_derecho": ")",
    "DosPuntos": ":",
    "PuntoComa": ";",
    "Coma": ",",
    "Llave_izquierda": "{",
    "Llave_derecha": "}",
    "Funcion_$set": "$set:"
    # NOTA: las comillas no son Tokens
}

global n_linea
global n_columna
global lista_lexemas
global lista_errores
global lista_tokens


n_linea = 1
n_columna = 1
lista_lexemas = []
lista_errores = []

lista_tokens=[]



def instruccion(cadena):
    global n_linea
    global n_columna
    global lista_lexemas
    lexema = ""
    puntero = 0

    while cadena:
        char = cadena[puntero]
        puntero += 1

        if char.isalpha() or char== '$':

            # se envia al metodo la cadena desde el puntero hasta el final
            lexema, cadena = armar_lexema(cadena[puntero-1:])

            # si no es None lexema entonces
            if lexema:

                # Armado de lexema como clase
                l = Lexema(lexema, n_linea, n_columna,None)

                # se guarda el lexema en la lista
                lista_lexemas.append(l)

                n_columna += len(lexema)
                puntero = 0

        elif char == "=":
            # Armado de lexema como clase
            c = Lexema(char, n_linea, n_columna,None)

            n_columna += 1
            lista_lexemas.append(c)
            cadena = cadena[1:]
            puntero = 0

        elif char == '(':
            # Armado de lexema como clase
            c = Lexema(char, n_linea, n_columna,None)

            n_columna += 1
            lista_lexemas.append(c)
            cadena = cadena[1:]
            puntero = 0

        # comillas que usa argumento de la funcion 
        elif char == '“':
            # se envia al metodo la cadena Con la comilla inicial
            lexema, cadena = armar_parametro(cadena[puntero-1:])
            # si no es None ninguna de las dos condiciones entonces
            if lexema and cadena:

                # Armado de lexema como clase
                l = Lexema(lexema, n_linea, n_columna,None)

                # se guarda el lexema en la lista
                lista_lexemas.append(l)

                # por el parentesis
                n_columna += len(lexema)
                puntero = 0

        # Comillas que usan los valores del Json, es la misma de apertura y de cierre
        elif char == '"':
            # si no es None ninguna de las dos condiciones entonces
            lexema, cadena = armar_dato_json(cadena[puntero:])
            # si no es None ninguna de las dos condiciones entonces
            if lexema and cadena:


                # Armado de lexema como clase
                l = Lexema(lexema, n_linea, n_columna,None)

                # se guarda el lexema en la lista
                lista_lexemas.append(l)


                n_columna += len(lexema)
                puntero = 0

        elif char == ',':
            # Armado de lexema como clase
            c = Lexema(char, n_linea, n_columna,None)

            n_columna += 1
            lista_lexemas.append(c)
            cadena = cadena[1:]
            puntero = 0

        elif char == '{':
            # Armado de lexema como clase
            c = Lexema(char, n_linea, n_columna,None)

            n_columna += 1
            lista_lexemas.append(c)
            cadena = cadena[1:]
            puntero = 0

        elif char == '}':
            # Armado de lexema como clase
            c = Lexema(char, n_linea, n_columna,None)

            n_columna += 1
            lista_lexemas.append(c)
            cadena = cadena[1:]
            puntero = 0

        elif char == ':':
            # Armado de lexema como clase
            c = Lexema(char, n_linea, n_columna,None)

            n_columna += 1
            lista_lexemas.append(c)
            cadena = cadena[1:]
            puntero = 0

        elif char == ")":
           # Armado de lexema como clase
            c = Lexema(char, n_linea, n_columna,None)

            n_columna += 1
            lista_lexemas.append(c)
            cadena = cadena[1:]
            puntero = 0

        elif char == ";":
            # Armado de lexema como clase
            c = Lexema(char, n_linea, n_columna,None)

            n_columna += 1
            lista_lexemas.append(c)
            cadena = cadena[1:]
            puntero = 0

        elif char == "\t":
            cadena = cadena[4:]
            n_columna += 4
            puntero = 0

        elif char == "\n":
            cadena = cadena[1:]
            n_columna = 1
            n_linea += 1
            puntero = 0

        elif char == ' ' or char == '\r' or char == '”':
            cadena = cadena[1:]
            n_columna += 1
            puntero = 0

        else:
            cadena = cadena[1:]
            puntero = 0
            lista_errores.append(Errores(char, n_linea, n_columna,None))
            n_columna += 1
    

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
        # Coloque las comillas en caso de que falte el parentesis 
        if char == ' '  or char == "(" or char == '“' or char=='"':
            # en cadena el slicing devuelce desde uno antes del puntero hasta el final
            return lexema, cadena[len(puntero)-1:]
        else:
            # se va agregando letra por letra al lexema
            lexema += char
    # para evitar que se detenga el problema en caso de un error
    return None, None


def armar_parametro(cadena):
    global n_linea
    global n_columna
    global lista_lexemas
    lexema = ""
    puntero = ""
    # se recorre toda la cadena con el puntero hasta encontrar un espacio en blanco
    for char in cadena:
        puntero += char

        # Como las mismas comillas se usan para los argumentos de la funcion y para abrir el Json coloque el espacio en blanco y el salto
        if char == ')' or char == ';' or char == ',' or char== ' ' or char=='\n' :
            # en cadena el slicing devuelce desde uno antes del puntero hasta el final
            return lexema, cadena[len(puntero)-1:]

        else:
            # se va agregando letra por letra al lexema
            lexema += char
    # para evitar que se detenga el problema en caso de un error
    return None, None

def armar_dato_json(cadena):
    global n_linea
    global n_columna
    global lista_lexemas
    lexema = ""
    puntero = ""

    # se recorre toda la cadena con el puntero hasta encontrar un espacio en blanco
    for char in cadena:
        puntero += char

        if char == '"':
            # Se le colocan las comillas al inicio y al final, porque se supone que eso siempre va a venir
            return  char+lexema+char,cadena[len(puntero):]

        else:
            # se va agregando letra por letra al lexema
            lexema += char
    # para evitar que se detenga el problema en caso de un error
    return None, None


def asignarToken():


    lista_solo_lexemas = []

    # lista de solo los lexemas, sin columna ni nada
    for i in range(len(lista_lexemas)):
        lista_solo_lexemas.append(lista_lexemas[i].operar(None))


    for i, lexema in enumerate(lista_solo_lexemas):
        
        # se se asignan a las palabras reservadas los tokens correspondientes
        if lexema in reserved.values():
           lista_lexemas[i].setToken(list(reserved.keys())[list(reserved.values()).index(lista_solo_lexemas[i])])

        # se asigna el token "Argumento" a los lexemas que empiezan y terminan con comillas, porque se supone que siempre van a venir con ellas
        elif lista_solo_lexemas[i][0] == '“' and lista_solo_lexemas[i][-1] == '”':  
            lista_lexemas[i].setToken("Argumento")

        # se asigna el token "Parte_json" a los lexemas que empiezan y terminan con comillas de JSon, porque se supone que siempre van a venir con ellas
        elif lista_solo_lexemas[i][0] == '"' and lista_solo_lexemas[i][-1] == '"':  
            lista_lexemas[i].setToken("Parte_json")

        elif lista_solo_lexemas[i][0].isalpha()==True and lista_solo_lexemas[i][-1].isalpha()==True:
            lista_lexemas[i].setToken("Identificador")

        # === Este else es para los errores que ocurren cuando las palabras reservadas tienen un caracter que no es valido, pero creo que ese es un error sintectico por lo cual lo dejo de momento comentado ===
        # else:
        #     lista_errores.append(Errores(lexema, n_linea, n_columna,None))





    

def TablaTokens():

    global lista_lexemas

    for i in range(len(lista_lexemas)):
        print("=====================================")
        print("Lexema ==>", lista_lexemas[i].operar(None))
        print("Token ==>", lista_lexemas[i].getToken())
        print("Fila ==>", lista_lexemas[i].getFila())
        print("Columna ==>", lista_lexemas[i].getColumna())

entrada = '''

CrearBD ejemplo = nueva CrearBD(“Data”); 

EliminarBD elimina = nueva EliminarBD(“Data”); 

CrearColeccion colec = nueva CrearColeccion(“NombreColeccion”);

EliminarColeccion eliminacolec = nueva EliminarColeccion(“NombreColeccion”); 

InsertarUnico insertadoc = nueva InsertarUnico(“NombreColeccion” ,
{
{ 
 "nombre" : "Obra Literaria", 
 "autor" : "Jorge Luis" 
 } 
});

ActualizarUnico actualizadoc = nueva ActualizarUnico(“NombreColeccion”, 
{
    { 
    "nombre" : "Obra Literaria" 
    }, 
    { 
    $set: {"autor" : "Mario Vargas"} 
    } 
});

EliminarUnico eliminadoc = nueva EliminarUnico(“NombreColeccion”,
{
    { 
    "nombre" : "Obra Literaria" 
    } 
});

BuscarTodo todo = nueva BuscarTodo (“NombreColeccion”); *

BuscarUnico todo = nueva BuscarUnico (“NombreColeccion”); 
@
'''

instruccion(entrada)

asignarToken()

TablaTokens()


print(" ")
print("==== ERRORES ====")
for error in lista_errores:
    print("ERROR: ", error.operar(None))
