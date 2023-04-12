from fileinput import filename
from tkinter.filedialog import askopenfilename
from tkinter.tix import Tree
from tkinter import Tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter.filedialog import asksaveasfilename
from analizador_lexico import instruccion, operar_, generarGrafica, limpiarLista,  CrearArchivoErrores, limpiarListaErrores, lexemas_grafico
import os


class Pantalla_principal():

    def __init__(self):
        self.pp = Tk()
        self.pp.title("Pantalla Principal | Proyecto 1")
        self.centrar(self.pp, 1000, 800)
        self.pp.configure(bg="#343541")
        self.pantalla_1()

    def centrar(self, r, ancho, alto):
        altura_pantalla = r.winfo_screenheight()
        anchura_pantalla = r.winfo_screenwidth()
        x = (anchura_pantalla//2)-(ancho//2)
        y = (altura_pantalla//2)-(alto//2)
        r.geometry(f"+{x}+{y}")

    def pantalla_1(self):
        self.Frame = Frame(height=600, width=1100)
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
            bg="#343541", width=10, justify="left", anchor="w").place(x=623, y=0)

        # menu archivo
        self.menubar = Menu(self.pp)

        # === Opciones del menu Archivo ===
        archivoMenu = Menu(self.menubar, tearoff=0)

        archivoMenu .add_command(
            label="Nuevo", command=self.nuevo, font=("Roboto Mono", 13))
        archivoMenu .add_command(
            label="Abrir", command=self.abrirArchivo, font=("Roboto Mono", 13))
        archivoMenu .add_command(
            label="Guardar", command=self.guardar, font=("Roboto Mono", 13))
        archivoMenu .add_command(label="Guardar Como",
                                 command=self.guardarComo, font=("Roboto Mono", 13))
        archivoMenu.add_separator()
        archivoMenu .add_command(
            label="Salir", command=self.pp.destroy, font=("Roboto Mono", 13))
        self.menubar.add_cascade(
            label="Archivo", menu=archivoMenu, font=("Roboto Mono", 13))

        # === Menu analizar ===

        analizarMenu = Menu(self.menubar, tearoff=0)

        analizarMenu .add_command(
            label="Analizar", command=self.analizar, font=("Roboto Mono", 13))

        self.menubar.add_cascade(
            label="Analizar", menu=analizarMenu, font=("Roboto Mono", 13))

        # === Menu Tokens ===

        TokensMenu = Menu(self.menubar, tearoff=0)

        TokensMenu.add_command(
            label="Tokens", command=self.tokens, font=("Roboto Mono", 13))

        self.menubar.add_cascade(
            label="Tokens", menu=TokensMenu, font=("Roboto Mono", 13))

        # === Menu Errores ===

        erroresMenu = Menu(self.menubar, tearoff=0)

        erroresMenu.add_command(
            label="Errores", command=self.errores, font=("Roboto Mono", 13))

        self.menubar.add_cascade(
            label="Errores", menu=erroresMenu, font=("Roboto Mono", 13))

        # confiuracion del menubar

        self.pp.config(menu=self.menubar)

        # cuadro de texto de entrada
        textContainer = Frame(self.pp, borderwidth=1, relief="sunken")

        text = Text(textContainer, font=(
            "Times New Roman", 15), fg='white', bg="#444654", width=45, height=24, wrap="none")

        textVsb = Scrollbar(
            textContainer, orient="vertical", command=text.yview)
        textHsb = Scrollbar(
            textContainer, orient="horizontal", command=text.xview)
        text.configure(yscrollcommand=textVsb.set, xscrollcommand=textHsb.set)

        text.grid(row=0, column=0, sticky="nsew")
        textVsb.grid(row=0, column=1, sticky="ns")
        textHsb.grid(row=1, column=0, sticky="ew")

        textContainer.grid_rowconfigure(0, weight=1)
        textContainer.grid_columnconfigure(0, weight=1)

        textContainer.place(x=28, y=53)

        # cuadro de texto de salida
        textContainerSalida = Frame(self.pp, borderwidth=1, relief="sunken")

        text = Text(textContainerSalida, font=(
            "Times New Roman", 15), fg='white', bg="#444654", width=45, height=24, wrap="none", state=DISABLED)

        textVsb = Scrollbar(
            textContainerSalida, orient="vertical", command=text.yview)
        textHsb = Scrollbar(
            textContainerSalida, orient="horizontal", command=text.xview)
        text.configure(yscrollcommand=textVsb.set, xscrollcommand=textHsb.set)

        text.grid(row=0, column=0, sticky="nsew")
        textVsb.grid(row=0, column=1, sticky="ns")
        textHsb.grid(row=1, column=0, sticky="ew")

        textContainerSalida.grid_rowconfigure(0, weight=1)
        textContainerSalida.grid_columnconfigure(0, weight=1)

        textContainerSalida.place(x=650, y=53)

        # Actualizacion del Frame
        self.Frame.mainloop()

    def nuevo(self):
        messagebox.showinfo("Nuevo", "Boton de Nuevo presionado")

    def analizar(self):
        messagebox.showinfo("Analizar", "Boton de Analizar presionado")

    def tokens(self):
        messagebox.showinfo("Tokens", "Boton de Tokens presionado")

    def errores(self):
        messagebox.showinfo("Errores", "Boton de Errores presionado")

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

            # # se separa el nombre del archivo en directorio y nombre
            # os.path.split(filename)
            # # se obtiene el nombre del archivo con la extension
            # self.filename = os.path.split(filename)[1]
            # # se obtiene el nombre del archivo sin la extension
            # self.filename = os.path.splitext(self.filename)[0]

            # Elimina contenido del cuadro
            self.cuadroTexto.delete(1.0, "end")

            # set contenido
            self.cuadroTexto.insert(1.0, self.texto)

        except:
            messagebox.showerror(
                "Error", "Archivo no soportado")
            return

    def ejecutar(self):
        # variable para saber si ya se presiono el boton de analizar
        self.analizado = True
        # En caso de que despues de analizar un arhivo se analice otro se limpian las listas
        limpiarListaErrores()
        limpiarLista()
        try:
            instruccion(self.texto)
            lexemas_grafico()
            operar_()
            generarGrafica(str("RESULTADOS_202044192"))

            # set contenido
            messagebox.showinfo("Analisis completado",
                                "Analisis realizado con exito, archivo .dot y .pdf generados")

        except:
            messagebox.showerror(
                "Error", "No se ha seleccionado ningún archivo")
            return

    def guardar(self):
        try:
            # Tomar datos que esta en el cuadro de texto
            self.texto = self.cuadroTexto.get(1.0, "end")

            archivo = open(self.archivo_seleccionado, 'w', encoding="utf-8")
            archivo.write(self.texto)

            # mensaje de guardado
            messagebox.showinfo("Guardado", "Archivo guardado con exito")

        except:
            messagebox.showerror(
                "Error", "No se ha seleccionado ningún archivo")
            return

    def guardarComo(self):
        try:
            # Tomar datos que esta en el cuadro de texto
            self.texto = self.cuadroTexto.get(1.0, "end")

            self.extensions = [("Archivos txt", f".txt"),
                               ("Archivos lfp", f".lfp"), ("All files", "*")]

            self.archivo_seleccionado = filename = asksaveasfilename(
                title="Seleccione un archivo", filetypes=[("Archivos txt", f".txt"), ("Archivos lfp", f".lfp"), ("All files", "*")], defaultextension=self.extensions, initialfile="Documento")

            archivo = open(self.archivo_seleccionado, 'w', encoding="utf-8")
            archivo.write(self.texto)

            # mensaje de guardado
            messagebox.showinfo("Guardado", "Archivo guardado con exito")

        except:
            messagebox.showerror(
                "Error", "No se ha seleccionado ningún archivo")
            return

    def getErrores(self):
        # Solo generamos los errores si ya se ha presionado el boton de analizar, porque si se presiona guardar sin analizar no se generan errores
        if (self.analizado == False):
            messagebox.showerror(
                "Error", "Para generar el archivo de errores primero debe de analizar el archivo")
            return
        try:
            CrearArchivoErrores()
            # mensaje de guardado
            messagebox.showinfo(
                "Guardado", "Archivo de errores generado con exito")
        except:
            messagebox.showerror(
                "Error", "No se ha podido generar el archivo de errores")
            return


# mostrar pantalla
r = Pantalla_principal()
