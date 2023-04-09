# LFP_Proyecto2_202044192

## 1. DESCRIPCIÓN GENERAL

### OBJETIVO GENERAL

Combinar los conocimientos adquiridos en el curso y en los otros cursos de sistemas, para
crear un compilador que traduzca el lenguaje especificado y lo transforme en Sentencias de
Bases de Datos No Relacionales.

### OBJETIVOS ESPECÍFICOS

- Crear una herramienta que permita el diseño de sentencias de base de datos no
  relacionales de una forma sencilla para el usuario.
- Diseñar y construir un compilador que permita compilar archivos de entrada y
  visualizar el resultado en un entorno externo.
- Desarrollar la habilidad del estudiante para elaborar proyectos en base a una adecuada
  planificación para que aprendan la manera en la que tienen que trabajar.

### DESCRIPCIÓN

El proyecto consiste en la elaboración de una herramienta que permita el diseño y creación
de sentencias de bases de datos no relacionales de una forma sencilla. La aplicación tendrá
un área de edición de código y un área de visualización de la sentencia final generada.

Cuando ya se cuente con las sentencias creadas inicialmente, se procederá a realizar la
compilación respectiva lo que generar las sentencias de MongoDB que serán mostradas en el
espacio de resultados que posteriormente se podrán aplicar a un entorno adecuado a
MongoDb.

## 2. CARACTERÍSTICAS DE LA SOLUCIÓN

Para poder responder a las necesidades expuestas anteriormente, se ha pensado en el
desarrollo de una aplicación en lenguaje Python que permitirá la creación de las sentencias
básicas para ejecutar código de MongoDB.

Con la ayuda de métodos como: Árbol y parser descendente de llamadas recursivas, se deberá
implementar una solución que reconozca archivos de texto que contendrán la definición de
las sentencias que se usaran en MongoDb, así como sus características particulares de cada
sentencia.

La aplicación deberá mostrar los errores que puedan existir en el archivo de entrada que se
esté analizando, se deben visualizar de manera agradable y con la suficiente información para
saber dónde ocurre el error. Al no encontrarse errores se procede a traducir lo que el archivo
de entrada requiere que se haga.

En cualquier momento se pueden colocar comentarios dentro de cada bloque de código del
programa, estos son de la manera cómo funciona en las bases de datos
