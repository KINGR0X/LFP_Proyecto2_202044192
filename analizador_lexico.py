from Abstract.lexema import *
from Errores.erroresLex import *
from Errores.erroresSin import *

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
    "Funcion_$set": "$set"
    # NOTA: las comillas no son Tokens
}

global n_linea
global n_columna
global lista_lexemas
global lista_errores
global lista_tokens
global needJson

n_linea = 1
n_columna = 1
lista_lexemas = []
lista_errores = []
needJson=False


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
        if char == ' '  or char == "(" or char == '“' or char=='"' or char==':':
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



def analizador_sintactico(tokens):

    global needJson

    isSet= False
    estado=0

    for i in range(len(tokens)):    

            if estado==0:                
                    
                if tokens[i].getToken() == 'Funcion_CrearBD' or tokens[i].getToken() == 'Funcion_EliminarBD' or tokens[i].getToken() == 'Funcion_CrearColeccion' or tokens[i].getToken() =='Funcion_EliminarColeccion' or tokens[i].getToken() =='Funcion_BuscarTodo' or tokens[i].getToken() =='Funcion_BuscarUnico' or tokens[i].getToken() =='Funcion_insertarUnico' or tokens[i].getToken() =='Funcion_ActualizarUnico' or tokens[i].getToken() == 'Funcion_EliminarUnico':

                    estado=1

                    # si se llego al ultimo token, significa que faltan tokens a la derecha
                    if i == len(tokens) - 1:
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"a la derecha de Funcion"))

                    continue
                else:
                    if verificarTokenN(tokens[i]) == True:
                        estado=1
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Funcion"))
                        continue
                    else:
                        estado=1
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Funcion"))
                    

            if estado==1:
                if tokens[i].getToken() == 'Identificador':

                    estado=2
                    # si se llego al ultimo token, significa que faltan tokens a la derecha
                    if i == len(tokens) - 1:
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"a la derecha de Identificador"))

                    continue
                else:
                    if verificarTokenN(tokens[i]) == True:
                        estado=2
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Identificador"))
                        continue
                    else:
                        estado=2
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Identificador"))
                    

            if estado==2:
                if tokens[i].getToken() == 'Igual':

                    estado=3

                    # si se llego al ultimo token, significa que faltan tokens a la derecha
                    if i == len(tokens) - 1:
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"a la derecha de Igual"))

                    continue
                else:
                    if verificarTokenN(tokens[i]) == True:
                        estado=3
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Igual"))
                        continue
                    else:
                        estado=3
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Igual"))
                    

            if estado==3:
                if tokens[i].getToken() == 'Reservada_nueva':

                    estado=4

                    # si se llego al ultimo token, significa que faltan tokens a la derecha
                    if i == len(tokens) - 1:
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"a la derecha de Reservada_nueva"))

                    continue
                else:
                    if verificarTokenN(tokens[i]) == True:
                        estado=4
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Reservada_nueva"))
                        continue
                    else:
                        estado=4
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Reservada_nueva"))
                    

            if estado==4:

                # se comprueba que la funcion sea insertarUnico, ActualizarUnico o EliminarUnico, ya que estas funciones necesitan una coma
                if tokens[i].getToken() =='Funcion_insertarUnico' or tokens[i].getToken() =='Funcion_ActualizarUnico' or tokens[i].getToken() == 'Funcion_EliminarUnico':
                        needJson = True
                
                if tokens[i].getToken() == 'Funcion_CrearBD' or tokens[i].getToken() == 'Funcion_EliminarBD' or tokens[i].getToken() == 'Funcion_CrearColeccion' or tokens[i].getToken() =='Funcion_EliminarColeccion' or tokens[i].getToken() =='Funcion_BuscarTodo' or tokens[i].getToken() =='Funcion_BuscarUnico' or tokens[i].getToken() =='Funcion_insertarUnico' or tokens[i].getToken() =='Funcion_ActualizarUnico' or tokens[i].getToken() == 'Funcion_EliminarUnico':

                    # Se comprueba que la funcion de la izquierda sea igual a la de la derecha
                    if tokens[i-4].getToken() != tokens[i].getToken():
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Las Funciones no coinciden"))

                    estado=5
                    # si se llego al ultimo token, significa que faltan tokens a la derecha
                    if i == len(tokens) - 1:
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"a la derecha de Funcion"))

                    continue
                else:
                    if verificarTokenN(tokens[i]) == True:
                        estado=5
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Funcion"))
                        continue
                    else:
                        estado=5
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Funcion"))
                    
            
            if estado==5:
                if tokens[i].getToken() == 'Parentesis_izquierdo':

                    estado=6

                    # si se llego al ultimo token, significa que faltan tokens a la derecha
                    if i == len(tokens) - 1:
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"a la derecha de Parentesis_izquierdo"))

                    continue
                else:
                    if verificarTokenN(tokens[i]) == True:
                        estado=6
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Parentesis_izquierdo"))
                        continue
                    else:
                        estado=6
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Parentesis_izquierdo"))
                    
            
            if estado==6:

                if tokens[i].getToken() == 'Argumento' and needJson== True:
                    needJson=False
                    estado=6.5

                    # si se llego al ultimo token, significa que faltan tokens a la derecha
                    if i == len(tokens) - 1:
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"a la derecha de Argumento"))

                    continue
        
                elif tokens[i].getToken() == 'Argumento':

                    estado=7

                    # si se llego al ultimo token, significa que faltan tokens a la derecha
                    if i == len(tokens) - 1:
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"a la derecha de Argumento"))

                    continue
                else:
                    if verificarTokenN(tokens[i]) == True:
                        estado=7
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Argumento"))
                        continue
                    else:
                        estado=7
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Argumento"))


            if estado==6.5:
                needJson==False

                if tokens[i].getToken() == 'Coma':

                    estado=6.9

                    # si se llego al ultimo token, significa que faltan tokens a la derecha
                    if i == len(tokens) - 1:
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"a la derecha de coma"))

                    continue

                else:
                    if verificarTokenN(tokens[i]) == True:
                        estado=6.9
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Coma"))
                        continue
                    else:
                        estado=6.9
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Coma")) 


            if estado==6.9:
                estado='Llave_izquierda_1'


            # === Inicio de Json ===

            if estado=='Llave_izquierda_1':                
                    
                if tokens[i].getToken() == 'Llave_izquierda':

                    estado='Llave_izquierda_2'

                    # si se llego al ultimo token, significa que faltan tokens a la derecha
                    if i == len(tokens) - 1:
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"a la derecha de Llave_izquierda"))

                    continue

                else:
            
                    if verificarTokenN(tokens[i]) == True:
                        estado='Llave_izquierda_2'
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Llave_izquierda"))
                        continue
                    else:
                        estado='Llave_izquierda_2'
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Llave_izquierda")) 

            # llave izquierda que va dentro del Json
            if estado=='Llave_izquierda_2':                
                    
                if tokens[i].getToken() == 'Llave_izquierda':

                    if tokens[i+1].getToken() == 'Funcion_$set' or tokens[i+1].getToken() == 'DosPuntos' or tokens[i+1].getToken() == 'Llave_izquierda':
                        estado= 'Funcion_$set'
                    else:
                        estado='Parte_json_1'

                    # si se llego al ultimo token, significa que faltan tokens a la derecha
                    if i == len(tokens) - 1:
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"a la derecha de Llave_izquierda"))

                    continue

                else:
                    if verificarTokenN(tokens[i]) == True:
                        estado='Parte_json_1'
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Llave_izquierda"))
                        continue
                    elif tokens[i].getToken() == 'Funcion_$set':
                        estado='Funcion_$set'
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Llave_izquierda"))
                        continue
                    else:
                        estado='Parte_json_1'
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Llave_izquierda")) 

            if estado=='Parte_json_1':

                if tokens[i].getToken() == 'Parte_json':
                        
                    estado='DosPuntos'

                    # si se llego al ultimo token, significa que faltan tokens a la derecha
                    if i == len(tokens) - 1:
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"a la derecha de parte Json"))

                    continue
                else:

                    if verificarTokenN(tokens[i]) == True:
                        estado='DosPuntos'
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Parte_json"))
                        continue
                    else:
                        estado='DosPuntos'
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Parte_json"))

            if estado=='Funcion_$set':
                isSet= True

                if tokens[i].getToken() == 'Funcion_$set':
                    
                        
                    estado='DosPuntos'

                    # si se llego al ultimo token, significa que faltan tokens a la derecha
                    if i == len(tokens) - 1:
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"a la derecha de $set"))

                    continue
                else:

                    if verificarTokenN(tokens[i]) == True:
                        estado='DosPuntos'
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"$set"))
                        continue
                    else:
                        estado='DosPuntos'
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"$set"))



            if estado=='DosPuntos':
                if tokens[i].getToken() == 'DosPuntos':
                    # como siempre lleva comillas el token de key y valor se llaman igual, entonces regresa al estado de Parte_json

                    if tokens[i-1].getToken() == 'Funcion_$set':
                        estado='Llave_izquierda_2'
                    else:
                        estado='Parte_json_2'

                    # si se llego al ultimo token, significa que faltan tokens a la derecha
                    if i == len(tokens) - 1:
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"a la derecha de DosPuntos"))

                    continue
                else:
                    if verificarTokenN(tokens[i]) == True:
                        estado='Parte_json_2'
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"DosPuntos"))
                        continue
                    elif tokens[i-1].getToken() == 'Funcion_$set':
                        estado='Llave_izquierda_2'
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"DosPuntos"))
                        continue
                    else:
                        estado='Parte_json_2'
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"DosPuntos"))


            if estado=='Parte_json_2': 

                if tokens[i].getToken() == 'Parte_json':

                    if (tokens[i+1].getToken() == 'Coma' and tokens[i+2].getToken() == 'Parte_json') or tokens[i+1].getToken() == 'Parte_json':
                        estado= 'Coma'
                    elif tokens[i+1].getToken() == 'Llave_izquierda':
                        estado='Llave_derecha_1'
                    elif tokens[i+1].getToken() == 'Coma':
                        estado='Llave_derecha_1'
                    else:
                        estado='Llave_derecha_1'

                    # si se llego al ultimo token, significa que faltan tokens a la derecha
                    if i == len(tokens) - 1:
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"a la derecha de parte Json"))

                    continue
                else:

                    if verificarTokenN(tokens[i]) == True:
                        estado='Llave_derecha_1'
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Parte_json"))
                        continue
                    else:
                        estado='Llave_derecha_1'
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Parte_json"))

            
            if estado=='Coma':                 
                    
                if tokens[i].getToken() == 'Coma':

                    if tokens[i+1].getToken() == 'Llave_izquierda':
                        estado='Llave_izquierda_2' 
                    # si falta la llave del siguiente Json 
                    elif tokens[i-1].getToken() == 'Llave_derecha':
                        estado='Llave_izquierda_2'
                    else:     
                        estado='Parte_json_1'

                    # si se llego al ultimo token, significa que faltan tokens a la derecha
                    if i == len(tokens) - 1:
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"a la derecha de Coma"))

                    continue

                else:
            
                    if verificarTokenN(tokens[i]) == True:
                        estado='Parte_json_1'
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Coma"))
                        continue
                    elif tokens[i].getToken() == 'Llave_izquierda':
                        estado='Llave_izquierda_2'
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Coma"))
                        continue
                    else:
                        estado='Parte_json_1'
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Coma")) 
           
            # llaves derechas dentro del Json
            if estado=='Llave_derecha_1':                
                    
                if tokens[i].getToken() == 'Llave_derecha':   

                    if tokens[i+1].getToken() == 'Coma':
                        estado= 'Coma'
                    elif tokens[i+1].getToken() == 'Llave_izquierda':
                        estado= 'Coma'
                    # este es en caso del $set, ya que tiene que ahce que queden dos llaves derechas juntas
                    elif isSet == True:
                        estado='Llave_derecha_1'
                        isSet = False
                    else:
                        estado='Llave_derecha_2'

                    # si se llego al ultimo token, significa que faltan tokens a la derecha
                    if i == len(tokens) - 1:
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"a la derecha de Llave_derecha"))

                    continue

                else:
            
                    if verificarTokenN(tokens[i]) == True:
                        estado='Llave_derecha_2'
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Llave_derecha"))
                        continue
                    elif tokens[i].getToken() == 'Coma' or tokens[i].getToken() == 'Llave_izquierda':
                        estado='Coma'
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Llave_derecha"))
                        continue
                    else:
                        estado='Llave_derecha_2'
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Llave_derecha")) 


            if estado=='Llave_derecha_2':   
   
                if tokens[i].getToken() == 'Llave_derecha':
                        
                    estado=7

                    # si se llego al ultimo token, significa que faltan tokens a la derecha
                    if i == len(tokens) - 1:
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"a la derecha de Llave_derecha"))

                    continue

                else:
            
                    if verificarTokenN(tokens[i]) == True:
                        estado=7
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Llave_derecha"))
                        continue
                    else:
                        estado=7
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Llave_derecha")) 

            # === Fin de Json ===

            
            if estado==7:

                if tokens[i].getToken() == 'Parentesis_derecho':

                    estado=8

                    # si se llego al ultimo token, significa que faltan tokens a la derecha
                    if i == len(tokens) - 1:
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"PuntoComa"))

                    continue

                else:
                    if verificarTokenN(tokens[i]) == True:
                        estado=8
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Parentesis_derecho"))
                        continue
                    else:
                        estado=8
                        lista_errores.append(ErrorSintac(tokens[i].operar(None),tokens[i].getFila(), tokens[i].getColumna(),"Parentesis_derecho")) 
                    


            if estado==8:

                if tokens[i].getToken() == 'PuntoComa':
                    estado=9
                    continue
                else:
                    estado=9
                    # se le resta uno a i, para que se imprima la fila correcta 
                    lista_errores.append(ErrorSintac(tokens[i-1].operar(None),tokens[i-1].getFila(), tokens[i-1].getColumna(),"PuntoComa"))

            if estado==9:
                analizador_sintactico(tokens[i:])
                break
                    
            

#Se verifica si el Token es NONE, si es None es porque el lexema tiene algun error sintactico
def verificarTokenN(token):
    if token.getToken() == None:
        return True
    else:
        return False
    

# armar JSON, creé un metodo especifico para eso porque si no se me hacia muy largo el codigo


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

BuscarTodo todo = nueva BuscarTodo (“NombreColeccion”); 

BuscarUnico todo = nueva BuscarUnico (“NombreColeccion”); 

'''





instruccion(entrada)

asignarToken()



analizador_sintactico(lista_lexemas)


#TablaTokens()


print(" ")
print("==== ERRORES ====")
for error in lista_errores:
    print("ERROR: ", error.operar(None))

