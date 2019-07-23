from tkinter import *
from tkinter import ttk
import tkinter as tk
import sqlite3
import os.path
import datetime

# Aqui, crearemos nuestra clase, Window, y heredames del marco
# la clase frame es una clase del modúlo de tkinter(see Lib/tkinter/__init__)

class Window(Frame):

    db_name = 'database.db'


    # define los ajustes antes de que inicie
    def __init__(self, priven=None):
        #parametros que quieres enviar a través de la clase "Frame"
        Frame.__init__(self, priven)
        #refiere al master widget, el cual es tk window
        self.priven = priven
        #con esto, iniciaremos la función "init_window"
        self.init_window()
        self.priven.title('ElecmilV (1.0)')
        self.priven.iconbitmap('ico.ico')
        self.priven.configure(background = 'grey')
        #----------------------------------------_______________________________________#
        global master_frame, f3
        master_frame = LabelFrame(self.priven)
        fr1 = LabelFrame(master_frame, text = 'Finalizados', height = 200, width = 100)
        f1 = LabelFrame(self.priven, text='Agregar', height = 225, width = 500, padx =5)
        f2 = LabelFrame(self.priven, text='Registrador', height = 225, width = 500, padx =5)
        f3 = LabelFrame(master_frame, text = 'Lista')
        void = LabelFrame(self.priven, height = 100, width = 100)

        f1.grid_propagate(False)
        fr1.grid_propagate(False)
        f2.grid_propagate(False)
        void.grid_propagate(False)
        #Frames
        master_frame.grid(row = 0, column = 0, rowspan = 2, pady = 5, padx = 5, sticky = 'nsew')
        fr1.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'nswe')
        f1.grid()
        f2.grid(stick = 'n')
        f3.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'n')
        void.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = 'nsew')

        #cambio dinamico de frame
        #Función cambio de frames
        def raise_frame(frame):
            frame.tkraise()

        for frame in (f1, f2):
            frame.grid(row = 0, column = 1, pady = 5, padx = 5, sticky = 'news')
        #colocando label en grilla
        Label(f1).grid()
        Label(f2).grid()
        #Botones
        add = Button(f1, text='Agregar', command=f2.lift).grid(column = 1, row = 0, pady =170, padx = 215)
        cancel = Button(f2,text = 'Cancelar', command=f1.lift).grid(row = 10, column = 2, columnspan = 2, sticky ='we')
        ok = Button(f2, text = 'Ok', command=self.add_product).grid(row = 10, column = 0, columnspan = 2, sticky = 'we')
        #eliminar = Button(f1, text='Eliminar', command = self.delete_product).grid()
        #editar = Button(f1, text='Editar').grid(row=1)

        #Mensajes de salida
        self.message = Label(void, text = '', fg = 'black', pady = 115, padx = 70)
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = 'nsew')

        #---------------------------Registro---------------------------------------#
        Label(f2, text = 'Nombre del dueño:', fg="blue4", bg ="gray80").grid(row = 1, column = 0, sticky='w')
        Label(f2, text = 'Número de telefono:', fg="blue4", bg ="gray80").grid(row = 1, column = 2, sticky='w')
        Label(f2, text = 'Marca:').grid(row = 2, column = 0)
        Label(f2, text = 'Modelo:').grid(row = 2, column = 2)
        Label(f2, text = 'Serie:', fg="blue4", bg ="gray80").grid(row = 3, column = 0, sticky = 'nsew')
        Label(f2, text = 'Presupuesto:', fg="blue4", bg ="gray80").grid(row = 3, column = 2, sticky = 'nsew')
        Label(f2, text = 'Síntomas:').grid(row = 4, column = 0, columnspan = 4, sticky = 'nsew')
        Label(f2, text = 'Modificaciones:', fg="blue4", bg ="gray80").grid(row = 6, column = 0,columnspan = 4, sticky = 'nsew')

        self.name = Entry(f2)
        self.numberp = Entry(f2)
        self.brand = Entry(f2)
        self.model = Entry(f2)
        self.serie = Entry(f2)
        self.budget = Entry(f2)
        self.symptom = Text(f2, height=6, width=60)
        self.extra = Text(f2, height=6, width=60)

        self.name.focus()
        self.name.grid(row = 1, column = 1, sticky='w')
        self.numberp.grid(row = 1, column = 3, sticky='w', padx = 5)
        self.brand.grid(row = 2, column = 1, sticky='w')
        self.model.grid(row = 2, column = 3, sticky='w', padx = 5)
        self.serie.grid(row = 3, column = 1)
        self.budget.grid(row = 3, column = 3)
        self.symptom.grid(row = 5, column = 0, columnspan = 4,sticky = 'w', pady = 5)
        self.extra.grid(row = 9, column = 0, columnspan = 4,sticky = 'nw', pady = 5)

        #-------------------------------------------------------------------------------#
        raise_frame(f1)
    #------------------------------------#

        #---------------------------------Lista----------------------------------#
        #vista de arbol
        self.tree = ttk.Treeview(f3, height = 20, show='headings', columns=('name', 'brand', 'model', 'datei'), selectmode='extended')
        self.tree.grid_propagate(False)
        self.tree.grid(row = 0, column = 0, sticky='nsew', padx = 5, pady = 10)

        self.tree.heading('name', text = 'Nombre', anchor = CENTER)
        self.tree.heading('datei', text = 'Fecha de registro', anchor = CENTER)
        self.tree.heading('brand', text = 'Marca', anchor = CENTER)
        self.tree.heading('model', text = 'Modelo', anchor = CENTER)


        self.tree.column('#0', minwidth=20, width=40)
        self.tree.column('#1', minwidth=20, width=130)
        self.tree.column('#2', minwidth=20, width=110)
        self.tree.column('#3', minwidth=20, width=120)

        #ejecución consulta
        self.get_products()

    #Creation of init_window
    def init_window(self):
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Exit", command=self.onExit)
        menubar.add_cascade(label="File", menu=fileMenu)

    #base de datos
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    #función para mostrar datos en lista------------------------------------------------------
    def get_products(self):
        #limpiador de tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        #consultando datos
        query = 'SELECT * FROM libreta'
        db_rows = self.run_query(query)
        #rellenando datos
        for row in db_rows:
            self.tree.insert('', 0, text=(),values=(row[1], row[3], row[4], row[2]))
    #----------------------------------------------------------------------------------------------
    #verificador de campos vacios
    def validation(self):
        return len(self.name.get()) != 0 and len(self.brand.get()) !=0

    #Función para guardar en base de datos
    def add_product(self):
        if self.validation():
            query = 'INSERT INTO libreta(nombre, marca, modelo, datei) VALUES(?, ?, ?, date())'
            parameters = (self.name.get(), self.brand.get(), self.model.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Guardado Satisfactoriamente'
            self.name.delete(0, END)
            self.brand.delete(0, END)
            self.model.delete(0, END)
            raise_frame()
        else:
            self.message['text'] = 'El nombre del dueño y la marca del dispositivo son obligatorios!'
        self.get_products()
        #menú contextual

    def onExit(self):
        self.quit()

# root window created. Here, that would be the only window, but
# you can later have windows within windows.
root = Tk()
#creation of an instance
app = Window(root)
#desactiva el maximizar
root.resizable(0, 0)
#mainloop
root.mainloop()
