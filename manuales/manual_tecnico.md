# Manual tecnico

## Requisitos del sistema

### Sistemas operativos compatibles

- Windows 10,11

### Memporia Ram

- Minimo 4gb de Ram

### Lenguajes de programación

- Python

## Archivo analizador.py

### Funcion instruccion(cadena), armarlexema(cadena), armarparametro(cadena), armar_dato_json(cadena)

La función instrucción recibe como parámetro una cadena de caracteres, archivo de entrada, y analiza cada carácter de la cadena para determinar si es un lexema aceptado por el programa o no. Si es un lexema aceptado se guarda en lista_lexemas y se continua analizando la cadena, si no es un lexema aceptado se guarda en lista_errores y se continua analizando la cadena. Trozo del codigo:

```python
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

```

si el carácter que se esta leyendo es una **letra** o un simbolo **$** se llama a la función armar_lexema para recorrer la cadena hasta que se encuentre un espacio en blanco, un parentesis de apertura, una comilla, dos puntos, una coma o un salto de linea. Esto debido a que pueden haber errores sintacticos que hagan dificil armar el lexema. Al encontrar uno de los anteriores caracteres se devuelce el lexema y la cadena "cortada" si el lexema guardado.

```python
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
        if char == ' '  or char == "(" or char == '“' or char=='"' or char==':' or char==',' or char=='\n':
            # en cadena el slicing devuelce desde uno antes del puntero hasta el final
            return lexema, cadena[len(puntero)-1:]
        else:
            # se va agregando letra por letra al lexema
            lexema += char
    # para evitar que se detenga el problema en caso de un error
    return None, None

```

Si el caracter que se esta leyendo es una comilla, entonces se llama a la función armar_parameetro, como su nombre indica armar paramtro es utilizado para armar el parametro que va dentro de los parentesis de la función, alencontrar un parentesis derecho, un punto y coma, una coma, un espacio en blanco, o un salto de linea devuelve el lexema y la cadena "cortada" si el lexema guardado.

```python
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
```

La función armar_dato_json relaiza los mismo que la función armar_parametro, la diferencia radica en que la función se detiene solo cuando encuentra un cierre de comillas, esto debido a que la comilla usada en el Json es diferente a la de los parametros de la función.

```python
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

```

### Función armarComentario

Cuando el caracter que se esta leyendo es un guíon (-), se llama a la función armarComentario(). La función antes indicada leé la cantidad de guiones que hay, ya que para que sea un comentario se necesitan 3 guiones, si al encontrar un salto de línea no hay 3 guiones al inicio eso quiere decir que hay un error en el comentario, por lo cual se guarda como un error y se indica que faltan guiones.

```python
def armarComentario(cadena):
    global n_linea
    global n_columna
    global lista_lexemas
    lexema = ""
    puntero = ""
    no_guion= 0
    # se recorre toda la cadena con el puntero hasta encontrar un espacio en blanco
    for char in cadena:

        puntero += char

        if char== '-':
            no_guion+=1


        # Como las mismas comillas se usan para los argumentos de la funcion y para abrir el Json coloque el espacio en blanco y el salto
        if char=='\n' :
            if no_guion==3:
                # en cadena el slicing devuelce desde uno antes del puntero hasta el final
                return lexema, cadena[len(puntero)-1:]
            else:
                lista_errores.append(ErrorSintac(lexema,n_linea, n_columna,"Guion"))
                return lexema, cadena[len(puntero)-1:]
        else:
            # se va agregando letra por letra al lexema
            lexema += char
    # para evitar que se detenga el problema en caso de un error
    return None, None

```

### Función armarComentarioLargo

Cuando el caracter que ese esta leyendo es una barra (/), se llama a la función armarComentarioLargo, si el siguiente caracter es un asterisco (\*) entonces se continua,de lo contrario se guarda como un error. Luego de que se haya leido el asterisco se siguen leyendo los caracteres hata que se encuentra una barra (/), al encontrar la barra se verifica que el caracter anterior sea un asteriso, si no lo es se guarda como un error, de lo contrario se devuelve el lexema y la cadena "cortada" sin el lexema.

```python
def armarComentarioLargo(cadena):
    global n_linea
    global n_columna
    global lista_lexemas
    lexema = ""
    puntero = ""
    estadoC= "*"
    # se recorre toda la cadena con el puntero hasta encontrar un espacio en blanco
    for char in cadena:

        puntero += char
        # si se llego al final de la cadena es porque no esta la barra, por lo cual es un error
        if len(cadena)== len(puntero):
            lista_errores.append(ErrorSintac(lexema,n_linea, n_columna,"Barra"))
            return lexema, cadena[len(puntero)-1:]

        # comienza con astericos porque la cadena mandada corta el "/"
        if estadoC=='*':
            if char=='*':
                lexema += char
                estadoC='texto'
                continue
            else:
                print("Error")
                lista_errores.append(ErrorSintac(lexema,n_linea, n_columna,"Asterisco"))
                return lexema, cadena[len(puntero)-1:]

        if estadoC=='texto':
            if char=='\n':
                lexema += char
                n_linea+=1
                continue
            elif char=='/':
                estadoC='fin'
                lexema += char
                continue
            else:
                lexema += char
                continue

        if estadoC=='fin':
            # se revisa si antes de la barras hay asteriscos
            if lexema[-2]=='*':
                # en cadena el slicing devuelce desde uno antes del puntero hasta el final
                return lexema, cadena[len(puntero)-1:]
            else:
                lista_errores.append(ErrorSintac(lexema,n_linea, n_columna,"Asterisco"))
                return lexema, cadena[len(puntero)-1:]

    # para evitar que se detenga el problema en caso de un error
    return None, None

```

### Función asignarToken()

La función asignarToken se encarga de asignar los tokens a los lexemas, para esto se recorre la lista de lexemas y se verifica si el lexema esta en la lista de palabras reservadas, si esta en la lista de palabras reservadas se le asigna el token correspondiente, si no esta se verifica en los otros if, que tokense le debe asignar, si su primer y ultimo caracter es una comillas "fina" se le asigna el token de argumento, si su primer y ultimo caracter es una comillas normal, se le asigna el token parte_json, y si su primer y ultimo caracter es una letra o un numero, se le asigna el token de identificador.

```python
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
        elif lista_solo_lexemas[i][0] == '“' and lista_solo_lexemas[i][-1] == '”' :
            lista_lexemas[i].setToken("Argumento")

        # se asigna el token "Parte_json" a los lexemas que empiezan y terminan con comillas de JSon, porque se supone que siempre van a venir con ellas
        elif lista_solo_lexemas[i][0] == '"' and lista_solo_lexemas[i][-1] == '"':
            lista_lexemas[i].setToken("Parte_json")

        # si es un numero su token es "parte_json"
        elif lista_solo_lexemas[i].isdigit()==True:
            lista_lexemas[i].setToken("Parte_json")

        elif (lista_solo_lexemas[i][0].isalpha()==True and lista_solo_lexemas[i][-1].isalpha()==True) or (lista_solo_lexemas[i][0].isalpha()==True and lista_solo_lexemas[i][-1].isdigit()==True):
            lista_lexemas[i].setToken("Identificador")

```

### Analizador Sintáctico

El analziador sintactico es el que tiene más lineas de codigo, esto debido aque utilizando estados recorre todos los tokens, verificando que se cumpla el orden que deberian llevar las instrucciones.

El funcionamiento de los estadoes se basa en comprobar si el token que se esta ñeyendo es el que deberia de ir en ese estado, si no lo es se guarda como error y se pasa al estado siguiente estado del token que deberia de ir despeus, si es el token que deberia de ir se pasa al siguiente estado, y se usa **continue**, para que el ciclo for pase al siguiente token. Se puede dar el caso de que el token que se esta leyendo sea el ultimo en ese caso se guarda como error ya que deberian de ir tokens luego de el token actual, y se le indica el error "A la derecha del Token".

En cada estado el funcionamiento es practicamente el mismo, con más o menos condiciones dependiendo de que es lo que podria venir despues del token que se esta leyendo.
Parte del codigo:

```python

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

```

### verificarTokenN(token)

Esta función se utiliza para verificar que el token no sea **None**, ya que si es none eso indicaria de que el token del lexema no fue actualizado, y por lo cual el lexema tiene un error sintactico.

```python
def verificarTokenN(token):
    if token.getToken() == None:
        return True
    else:
        return False

```

### UnirJson(cadena)

Esta función se utilzia para unir los Json que se utilzaran en la traducción a mongoDB, ya que los Json pueden venir en varios lexemas, y se necesita unirlos para poder traducirlos.

```python
def unirJson(cadena):
    global n_linea
    global n_columna
    global lista_lexemas
    lexema = ""
    puntero = ""
    # se recorre toda la cadena con el puntero hasta encontrar un espacio en blanco
    for char in cadena:
        puntero += char.operar(None)

        # Como las mismas comillas se usan para los argumentos de la funcion y para abrir el Json coloque el espacio en blanco y el salto
        if char.operar(None) == ')':
            # en cadena el slicing devuelce desde uno antes del puntero hasta el final
            return lexema

        else:
            # se va agregando letra por letra al lexema
            lexema += char.operar(None)
    # para evitar que se detenga el problema en caso de un error
    return None, None

```

### Función necesarioparaMongo(lista)

Con esta función se guarda en la lista **lista_mongo** los lexemas que se necesitan para la traducción a mongoDB, ya que no todos los lexemas son necesarios para la traducción. Parte del codigo:

```python
def necesarioparaMongo(lista):
    global lista_mongo

    # lista de solo los lexemas, sin columna ni nada
    for i in range(len(lista)):

        if lista[i].operar(None)== 'CrearBD' :
            if  lista[i+2].getToken() == 'Argumento':
                # se necesita la función y el nombre de la Base de datos
                lista_mongo.append(lista[i].operar(None))
                lista_mongo.append(lista[i+2].operar(None))

        if lista[i].operar(None)== 'EliminarBD' :
            if  lista[i+2].getToken() == 'Argumento':
                # solo se necesita la función
                lista_mongo.append(lista[i].operar(None))

        if lista[i].operar(None)== 'CrearColeccion':
            if  lista[i+2].getToken() == 'Argumento':
                # se necesita la función y el nombre de la Base de datos
                lista_mongo.append(lista[i].operar(None))
                lista_mongo.append(lista[i+2].operar(None))
```

### función trandormarMongo()

Con esta función se transforma la lista **lista_mongo** a las codenas traducidas para utilziar en MongoDb, para ello se guardan las instrucciones en la lista **lista_instrucciones**. Parte del codigo:

```python
def transformarMongo():
    global lista_mongo
    global lista_intrucciones

    # lista de solo los lexemas, sin columna ni nada
    for i in range(len(lista_mongo)):


        if lista_mongo[i]== 'CrearBD':
            # se necesita la función y el nombre de la Base de datos
            lista_intrucciones.append(f"use({lista_mongo[i+1]});")

        if lista_mongo[i]== 'EliminarBD':
            lista_intrucciones.append(f"db.dropDatabase();")

```

### Función armarInstrucciones()

Esta dunción es simplemente para colocarle un salto de linea entre los valores de la lista, para asi al momento de crear el archivo de salida no queden todas las instruccione pegadas entre si.

```python
def armarInstrucciones():
    instrucciones= ""
    for i in range(len(lista_intrucciones)):
        instrucciones+= lista_intrucciones[i]
        instrucciones+="\n"

    return instrucciones

```

### limpiarListas()

Fución usada para limpiar las listas, y variables en el caso de que se vuelva a realizar otro analisis.

```python
def limpiarListas():
    global n_columna
    global n_linea
    lista_intrucciones.clear()
    lista_errores.clear()
    lista_lexemas.clear()
    lista_mongo.clear()
    lista_intrucciones.clear()
    n_linea = 1
    n_columna = 1

```

### Función generarArchivo(nombreArchivo)

Como su nombre indica en esta función se genera elarchivo de salida con las sentencias de MongoDb traducidas.

```pyhton
def generarArchivo(nombreGrafica):

    nombre = nombreGrafica+".txt"

    # Creación del dot
    with open(nombre, 'w') as f:
        f.write(armarInstrucciones())

    # creamos la imagen
    os.system(
        f'dot -Tpdf {nombre} -o {nombreGrafica}.txt')

    # obtener direccion actual
    ruta = os.path.dirname(os.path.abspath(f"{nombreGrafica}.txt"))

    # reta del pdf
    archivo_pdf = ruta+f"\{nombreGrafica}.txt"

    path = f'{archivo_pdf}'

    print(path)

    # Abrir pdf en el navegador
    os.system(f'start notepad {path}')
```

## Clases abstractas

El archivo abstractas.py como su nombre indica es una clase abstracta donde se definen diferentes métodos que son utilizados por otros archivo, es una clase abstracta ya que cada archivo que implementa la clase abstracta hace uso de los métodos que se definen en esta clase de una manera diferente, los archivo **lexema.py**, **erroresLex.py**, y **ErroresSin.py** utilizan las clases abstractas.

```python
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

```

## Archivos de errores

Los archivos **erroresLex.py**, **ErroresSin.py** son archivos que se encargan de guardar los errores que se encuentran en el analisis lexico y sintactico respectivamente, con la función operar() se obtiene el tipo, fila, columna, token y descripción del error.

```python
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

```

## Archivo interfaz.py

Como su nombre indica en este archivo se crea la interfaz grafica de la aplicación haciendo uso de Tkinter. Se crean las pantallas, los botones, labels, y cuadros de texto.

Fragmento del codigo:

```python
class Pantalla_principal():

    def __init__(self):
        self.pp = Tk()
        self.pp.title("Pantalla Principal | Proyecto 2")
        self.centrar(self.pp, 1400, 630)
        self.pp.configure(bg="#343541")
        self.pantalla_1()

    def centrar(self, r, ancho, alto):
        altura_pantalla = r.winfo_screenheight()
        anchura_pantalla = r.winfo_screenwidth()
        x = (anchura_pantalla//2)-(ancho//2)
        y = (altura_pantalla//2)-(alto//2)
        r.geometry(f"+{x}+{y}")

    def pantalla_1(self):
        self.Frame = Frame(height=630, width=1400)
        self.Frame.config(bg="#343541")
        self.Frame.pack(padx=25, pady=25)
        self.text = ''
        posicionx1 = 480
        self.analizado = False

        # encabezado de cuadro de texto de entrada
        Label(self.Frame, text="Entrada", font=(
            "Roboto Mono", 18), fg="white",
            bg="#343541", width=10, justify="left", anchor="w").place(x=0, y=0)

        # encabezado de cuadro de texto de salida
        Label(self.Frame, text="Salida", font=(
            "Roboto Mono", 18), fg="white",
            bg="#343541", width=10, justify="left", anchor="w").place(x=752, y=0)


```

Para llamar las funciones al presionar los botones se utilizan diferentes funciones.

Las diferentes funciones siguen la misma logica, llaman a funciones del archivo analizador_lexico.py para realizar las operaciones.

Si la operación se realiza correctamente se ejecutan las funciones definidas, en caso de que ocurra un error se muestra una ventana de error.

### Función abrirArchivo(self)

La función abrirArchivo(self) se encarga de abrir un archivo de texto y mostrarlo en el cuadro de texto de entrada.

```python
 def abrirArchivo(self):
        self.analizado = False
        x = ""
        self.archivo_seleccionado = ''
        Tk().withdraw()

        try:
            self.archivo_seleccionado = filename = askopenfilename(
                title="Seleccione un archivo", filetypes=[("Archivos txt", f"*.txt"), ("Archivos lfp", f"*.lfp"), ("All files", "*")])

            with open(filename, encoding="utf-8") as infile:
                x = infile.read()

            self.texto = x

            # se separa el nombre del archivo en directorio y nombre
            os.path.split(filename)
            # se obtiene el nombre del archivo con la extension
            self.filename = os.path.split(filename)[1]
            # se obtiene el nombre del archivo sin la extension
            self.filename = os.path.splitext(self.filename)[0]

            # Elimina contenido del cuadro
            self.text.delete(1.0, "end")

            # set contenido
            self.text.insert(1.0, self.texto)

        except:
            messagebox.showerror(
                "Error", "Archivo no soportado")
            return

    def guardar(self):
        try:
            # Tomar datos que esta en el cuadro de texto
            self.texto = self.text.get(1.0, "end")

            archivo = open(self.archivo_seleccionado, 'w', encoding="utf-8")
            archivo.write(self.texto)

            # mensaje de guardado
            messagebox.showinfo("Guardado", "Archivo guardado con exito")

        except:
            messagebox.showerror(
                "Error", "No se ha seleccionado ningún archivo")
            return

```

El resto de funciones dentro del archivo Interfaz siguen la misma logica.

## Gramática libre de contexto

La gramatica libre de contexto utilizada para el analisis sintactico es la siguiente:

```
LEXICO:
CrearDB
EliminarDB
CrearColeccion
EliminarColeccion
InsertarUnico
ActualizarUnico
EliminarUnico
BuscarTodo
BuscarUnico
nueva
(
)
;
=
ID -> [a-z*A-Z*][a-z_A-Z_0-9]_
NUMERO -> [0-9]+
STRING -> "[^"]_"
IGNORE -> \t\r
COMENTARIOS -> //._
| /\*([^_]|\*+[^*/])\*\*+/
"

SINTACTICO:
init : instrucciones

    instrucciones : instruccion instrucciones
                | instruccion

    instruccion : crearDB ;
                | eliminarDB ;
                | crearColeccion ;
                | eliminarColeccion ;
                | insertarUnico ;
                | actualizarUnico ;
                | eliminarUnico ;
                | buscarTodo ;
                | buscarUnico ;

    crearDB : CrearDB ID = nueva CrearDB ( )

    eliminarDB : EliminarDB ID = nueva EliminarDB ( )

    crearColeccion : CrearColeccion ID = nueva CrearColeccion ( STRING )

    eliminarColeccion : EliminarColeccion ID = nueva EliminarColeccion ( STRING )

    insertarUnico : InsertarUnico ID = nueva InsertarUnico ( STRING , STRING )

    actualizarUnico : ActualizarUnico ID = nueva ActualizarUnico ( STRING , STRING )

    eliminarUnico : EliminarUnico ID = nueva EliminarUnico ( STRING )

    buscarTodo : BuscarTodo ID = nueva BuscarTodo ( STRING )

    buscarUnico : BuscarUnico ID = nueva BuscarUnico ( STRING )

```
