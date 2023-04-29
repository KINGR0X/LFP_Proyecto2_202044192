from fileinput import filename
from tkinter.filedialog import askopenfilename
from tkinter.tix import Tree
from tkinter import Tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter.filedialog import asksaveasfilename
from analizador_lexico import *
import os


class Pantalla_principal():

    def __init__(self):
        self.pp = Tk()
        self.pp.title("Pantalla Principal | Proyecto 2")
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
        self.textContainer = Frame(self.pp, borderwidth=1, relief="sunken")

        self.text = Text(self.textContainer, font=(
            "Times New Roman", 15), fg='white', bg="#444654", width=45, height=24, wrap="none")

        textVsb = Scrollbar(
            self.textContainer, orient="vertical", command=self.text.yview)
        textHsb = Scrollbar(
            self.textContainer, orient="horizontal", command=self.text.xview)
        self.text.configure(yscrollcommand=textVsb.set,
                            xscrollcommand=textHsb.set)

        self.text.grid(row=0, column=0, sticky="nsew")
        textVsb.grid(row=0, column=1, sticky="ns")
        textHsb.grid(row=1, column=0, sticky="ew")

        self.textContainer.grid_rowconfigure(0, weight=1)
        self.textContainer.grid_columnconfigure(0, weight=1)

        self.textContainer.place(x=28, y=53)

        # cuadro de texto de salida
        self.textContainerSalida = Frame(
            self.pp, borderwidth=1, relief="sunken")

        self.text2 = Text(self.textContainerSalida, font=(
            "Times New Roman", 15), fg='white', bg="#444654", width=45, height=24, wrap="none")

        textVsb2 = Scrollbar(
            self.textContainerSalida, orient="vertical", command=self.text2.yview)
        textHsb2 = Scrollbar(
            self.textContainerSalida, orient="horizontal", command=self.text2.xview)
        self.text2.configure(yscrollcommand=textVsb2.set,
                             xscrollcommand=textHsb2.set)

        self.text2.grid(row=0, column=0, sticky="nsew")
        textVsb2.grid(row=0, column=1, sticky="ns")
        textHsb2.grid(row=1, column=0, sticky="ew")

        self.textContainerSalida.grid_rowconfigure(0, weight=1)
        self.textContainerSalida.grid_columnconfigure(0, weight=1)

        self.textContainerSalida.place(x=650, y=53)

        # Actualizacion del Frame
        self.Frame.mainloop()

    def nuevo(self):

        try:
            self.texto = self.text.get(1.0, "end")

            if len(self.texto) != 1:
                # pregunta si se desea guardar el archivo
                respuesta = messagebox.askquestion(
                    "Guardar", "¿Desea guardar el archivo antes de crear uno nuevo?")

                if respuesta == "yes":
                    # Tomar datos que esta en el cuadro de texto
                    self.extensions = [("Archivos txt", f".txt"),
                                       ("Archivos lfp", f".lfp"), ("All files", "*")]

                    self.archivo_seleccionado = filename = asksaveasfilename(
                        title="Seleccione un archivo", filetypes=[("Archivos txt", f".txt"), ("Archivos lfp", f".lfp"), ("All files", "*")], defaultextension=self.extensions, initialfile="Documento")

                    archivo = open(self.archivo_seleccionado,
                                   'w', encoding="utf-8")
                    archivo.write(self.texto)

                    # mensaje de guardado
                    messagebox.showinfo(
                        "Guardado", "Archivo guardado con exito")
                else:
                    self.text.delete(1.0, "end")

            else:
                self.text.delete(1.0, "end")

        except:
            messagebox.showerror(
                "Error", "No se ha seleccionado ningún archivo")
            return

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

    def guardarComo(self):
        try:
            # Tomar datos que esta en el cuadro de texto
            self.texto = self.text.get(1.0, "end")

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
        # try:
        #     CrearArchivoErrores()
        #     # mensaje de guardado
        #     messagebox.showinfo(
        #         "Guardado", "Archivo de errores generado con exito")
        # except:
        #     messagebox.showerror(
        #         "Error", "No se ha podido generar el archivo de errores")
        #     return

    def analizar(self):
        # variable para saber si ya se presiono el boton de analizar
        self.analizado = True
        # En caso de que despues de analizar un arhivo se analice otro se limpian las listas
        # limpiarListaErrores()
        # limpiarLista()
        try:
            instruccion(self.texto)
            asignarToken()
            analizador_sintactico(lista_lexemas)

            if len(lista_errores) == 0:

                necesarioparaMongo(lista_lexemas)
                transformarMongo()
                # set contenido
                messagebox.showinfo("Analisis completado",
                                    "Analisis completado, No se encontraron errores")

                # Elimina contenido del cuadro
                self.text2.delete(1.0, "end")

                # set contenido
                self.text2.insert(1.0, lista_mongo)

            else:

                messagebox.showerror("Analisis completado",
                                     "Analisis completado, Se encontraron algunos errores")

                # Elimina contenido del cuadro
                self.text2.delete(1.0, "end")

                # set contenido
                self.text2.insert(
                    1.0, "Corrija los errores para poder realizar traducir los comandos a MongoDB")

        except:
            messagebox.showerror(
                "Error", "No se ha seleccionado ningún archivo")
            return

    def tokens(self):

        ventana = Tk()
        ventana.title("Tokens | Proyecto 2")
        self.centrar(ventana, 800, 320)
        ventana.geometry("800x320")
        ventana.configure(bg="#343541")

        tv = ttk.Treeview(ventana, columns=("col1", "col2", "col3"))

        tv.column("#0", width=100, anchor=CENTER)
        tv.column("#1", width=200, anchor=CENTER)
        tv.column("#2", width=200, anchor=CENTER)
        tv.column("#3", width=200, anchor=CENTER)

        tv.heading("#0", text="No.", anchor=CENTER)
        tv.heading("#1", text="Token", anchor=CENTER)
        tv.heading("#2", text="No.Token", anchor=CENTER)
        tv.heading("#3", text="Lexema", anchor=CENTER)

        # Estilos de la tabla
        style = ttk.Style(tv)
        style.theme_use("clam")

        style.configure("Treeview", background="white",
                        fieldbackground="white", foreground="black", font=['Times New Roman', 14, 'normal'])

        style.configure('Treeview.Heading', background="orange", font=[
                        'Times New Roman', 14, 'normal'])

        for i in range(len(lista_lexemas)):
            tv.insert("", END, text=i, values=(
                lista_lexemas[i].getToken(), i, lista_lexemas[i].operar(None)))

        tv.pack()

        ventana.mainloop()

    def errores(self):

        ventana = Tk()
        ventana.title("Tokens | Proyecto 2")
        self.centrar(ventana, 1100, 320)
        ventana.geometry("1100x320")
        ventana.configure(bg="#343541")

        tv = ttk.Treeview(ventana, columns=("col1", "col2", "col3", "col4"))

        tv.column("#0", width=150, anchor=CENTER)
        tv.column("#1", width=100, anchor=CENTER)
        tv.column("#2", width=100, anchor=CENTER)
        tv.column("#3", width=250, anchor=CENTER)
        tv.column("#4", width=500, anchor=CENTER)

        tv.heading("#0", text="Tipo", anchor=CENTER)
        tv.heading("#1", text="Fila", anchor=CENTER)
        tv.heading("#2", text="Columna", anchor=CENTER)
        tv.heading("#3", text="Token o Lexema", anchor=CENTER)
        tv.heading("#4", text="Descripcion", anchor=CENTER)

        # Estilos de la tabla
        style = ttk.Style(tv)
        style.theme_use("clam")

        style.configure("Treeview", background="white",
                        fieldbackground="white", foreground="black", font=['Times New Roman', 14, 'normal'])

        style.configure('Treeview.Heading', background="orange", font=[
                        'Times New Roman', 14, 'normal'])

        for i in range(len(lista_errores)):
            tipo, fila, columna, lex, desc = lista_errores[i].operar(None)

            tv.insert("", END, text=tipo, values=(
                fila, columna, lex, desc))

        tv.pack()

        ventana.mainloop()


# mostrar pantalla
r = Pantalla_principal()
