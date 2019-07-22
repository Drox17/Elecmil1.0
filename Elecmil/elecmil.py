from tkinter import *
from tkinter import ttk
import tkinter as tk
import sqlite3
import os.path
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
        global master_frame
        master_frame = LabelFrame(self.priven)
        frame1 = LabelFrame(master_frame, text = 'Upper', height = 200, width = 100)
        void = LabelFrame(self.priven, height = 100, width = 100)
        frame3 = LabelFrame(master_frame, text = 'Lista')

        frame1.grid_propagate(False)
        void.grid_propagate(False)

        master_frame.grid(row = 0, column = 0, rowspan = 2, pady = 5, padx = 5, sticky = 'nsew')
        void.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = 'nsew')
        frame1.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'nswe')
        frame3.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'n')


        #Frames
        f1 = LabelFrame(self.priven, text='Agregar', height = 225, width = 500, padx =5)
        frame2 = LabelFrame(self.priven, text='Registrador', height = 225, width = 500, padx =5)
        f1.grid_propagate(False)
        frame2.grid_propagate(False)
        f1.grid()
        frame2.grid(stick = 'n')

        #cambio dinamico de frame
        #Función cambio de frames
        def raise_frame(frame):
            frame.tkraise()

        for frame in (f1, frame2):
            frame.grid(row = 0, column = 1, pady = 5, padx = 5, sticky = 'news')
        #colocando label en grilla
        Label(f1).grid()
        Label(frame2).grid()
        #Botones
        add = Button(f1, text='Agregar', command=frame2.lift).grid(column = 1, row = 0, pady =170, padx = 215)
        cancel = Button(frame2,text = 'Cancelar', command=f1.lift).grid(row = 10, column = 2, columnspan = 2, sticky ='we')
        ok = Button(frame2, text = 'Ok', command=self.add_product).grid(row = 10, column = 0, columnspan = 2, sticky = 'we')

        #eliminar = Button(frame1, text='Eliminar', command = self.delete_product).grid()
        #editar = Button(frame1, text='Editar').grid(row=1)
        #función cambio de frame

        #Mensajes de salida
        self.message = Label(void, text = '', fg = 'black', pady = 115, padx = 70)
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = 'nsew')

        #---------------------------Registro---------------------------------------#
        Label(frame2, text = 'Nombre del dueño:', fg="blue4", bg ="gray80").grid(row = 1, column = 0, sticky='w')
        Label(frame2, text = 'Número de telefono:', fg="blue4", bg ="gray80").grid(row = 1, column = 2, sticky='w')
        Label(frame2, text = 'Presupuesto:').grid(row = 2, column = 0)
        Label(frame2, text = 'Precio:').grid(row = 2, column = 2)
        Label(frame2, text = 'Marca:', fg="blue4", bg ="gray80").grid(row = 3, column = 0, sticky = 'nsew')
        Label(frame2, text = 'Modelo:', fg="blue4", bg ="gray80").grid(row = 3, column = 2, sticky = 'nsew')
        Label(frame2, text = 'Síntomas:').grid(row = 4, column = 0, columnspan = 4, sticky = 'nsew')
        Label(frame2, text = 'Modificaciones:', fg="blue4", bg ="gray80").grid(row = 6, column = 0,columnspan = 4, sticky = 'nsew')
        Label(frame2, text = 'Diagnóstico:')

        self.name = Entry(frame2)
        self.numberp = Entry(frame2)
        self.budget = Entry(frame2)
        self.price = Entry(frame2)
        self.brand = Entry(frame2)
        self.model = Entry(frame2)
        self.symptom = Text(frame2, height=6, width=60)
        self.extra = Text(frame2, height=6, width=60)
        self.diag = Text(frame2, height=6, width=60, fg="blue4")

        self.name.focus()
        self.name.grid(row = 1, column = 1, sticky='w')
        self.numberp.grid(row = 1, column = 3, sticky='w', padx = 5)
        self.budget.grid(row = 2, column = 1, sticky='w')
        self.price.grid(row = 2, column = 3, sticky='w', padx = 5)
        self.brand.grid(row = 3, column = 1)
        self.model.grid(row = 3, column = 3)
        self.symptom.grid(row = 5, column = 0, columnspan = 4,sticky = 'w', pady = 5)
        self.extra.grid(row = 9, column = 0, columnspan = 4,sticky = 'nw', pady = 5)
        self.diag.grid(row = 9, column = 0, columnspan = 4,sticky = 'nw', pady = 5)
        #-------------------------------------------------------------------------------#
        raise_frame(f1)
    #------------------------------------#

        #---------------------------------Lista----------------------------------#
        #vista de arbol
        self.tree = ttk.Treeview(frame3, height = 20, show='headings', columns=('id', 'name', 'brand', 'model', 'date'), selectmode='extended')
        self.tree.grid_propagate(False)
        self.tree.grid(row = 0, column = 0, sticky='nsew', padx = 5, pady = 10)

        self.tree.heading('id', text = 'Estado', anchor = CENTER)
        self.tree.heading('name', text = 'Nombre', anchor = CENTER)
        self.tree.heading('date', text = 'Fecha', anchor = CENTER)
        self.tree.heading('brand', text = 'Marca', anchor = CENTER)
        self.tree.heading('model', text = 'Modelo', anchor = CENTER)
        self.tree.heading('date', text = 'Fecha', anchor = CENTER)

        self.tree.column('#0', minwidth=20, width=40)
        self.tree.column('#1', minwidth=20, width=130)
        self.tree.column('#2', minwidth=20, width=110)
        self.tree.column('#3', minwidth=20, width=120)
        self.tree.column('#4', minwidth=20, width=100)

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
            self.tree.insert('', 0, text=(),values=(row[1], row[2], row[3], row[4]))
    #----------------------------------------------------------------------------------------------
    #verificador de campos vacios
    def validation(self):
        return len(self.name.get()) != 0 and len(self.brand.get()) !=0
    #Función para guardar en base de datos
    def add_product(self):
        if self.validation():
            query = 'INSERT INTO libreta(nombre, marca, modelo) VALUES(?, ?, ?)'
            parameters = (self.name.get(), self.brand.get(), self.model.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Guardado Satisfactoriamente'
            self.name.delete(0, END)
            self.brand.delete(0, END)
            self.model.delete(0, END)
        else:
            self.message['text'] = 'El nombre del dueño y la marca del dispositivo son obligatorios!'
        self.get_products()

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
