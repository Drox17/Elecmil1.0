from tkinter import ttk
import tkinter as tk
from tkinter import *
import datetime
import sqlite3

class Window(Frame):
    global con, cursorObj
    #conexión a base de datos
    con = sqlite3.connect('database.db')
    #objeto cursor
    cursorObj = con.cursor()

    def __init__(self, priven = None):
        Frame.__init__(self, priven)
        self.priven = priven
        self.priven.title('Test')
        self.priven.configure(background='grey')
        #Frame principal
        self.main_frame=Label(self.priven, height=20, width=95)
        self.main_frame.grid_propagate(False)
        self.main_frame.grid(padx=1, pady=1, rowspan=5)
        #Frame Izq
        self.main_table=Label(self.main_frame)
        self.main_table.grid(row=0, column=0, columnspan=2, rowspan=5)
        #Frame lista
        self.frame_lista=Label(self.main_table, text='Lista')
        self.frame_lista.grid()
        #Frames de relleno
        self.upper_frame=Label(self.main_table, text='Upper', height=15, width=30)
        self.lower_frame=Label(self.priven, text='Lower', height=20, width=30)
        self.upper_frame.grid_propagate(False)
        self.lower_frame.grid_propagate(False)
        self.upper_frame.grid(row=0, column=0, padx=1, pady=1, sticky='n')
        self.lower_frame.grid(row=1, column=1, columnspan=2, rowspan=2, pady=1, padx=1, sticky='new')
        #Boton de relleno
        botonup = Button(self.upper_frame)
        #-w-w-w----------------------------------------------w-w-w-#
        #Tabla
        self.lista = ttk.Treeview(frame3, height = 20, show='headings', columns=('id', 'name', 'brand', 'model', 'date'), selectmode='extended')
        #Encabezado de tabla "Lista"
        self.lista.heading('id', text = 'Item', anchor=CENTER)
        self.lista.heading('name', text = 'Nombre', anchor=CENTER)
        self.lista.heading('brand', text = 'Marca', anchor=CENTER)
        self.lista.heading('model', text = 'Modelo', anchor=CENTER)
        self.lista.heading('date', text = 'Fecha', anchor=CENTER)
        #configuracion de encabezados
        self.lista.column('#0', minwidth=20, width=40)
        self.lista.column('#1', minwidth=20, width=130)
        self.lista.column('#2', minwidth=20, width=110)
        self.lista.column('#3', minwidth=20, width=120)
        self.lista.column('#4', minwidth=20, width=100)
        #Las siguientes 2 lineas harán que la lista ocupe la ventana horizontalmente
        #self.lista.grid(row=1, column = 0)
        #self.priven.grid_columnconfigure(0, weight=1)
        #-R-R-R-----------------------------------------------R-R-R-#
        #función de cambio dínamico
        def raise_frame(frame):
            frame.tkraise()
        #Frames dínamicos
        self.frame_top = LabelFrame(self.priven, text='Agregar', height=400, width=500, padx=5)
        self.frame_both = LabelFrame(self.priven, text='Registrador', height=400, width=500, padx=5)
        #configuración de frames
        self.frame_top.grid_propagate(False)
        self.frame_both.grid_propagate(False)
        self.frame_top.grid(sticky='n')
        self.frame_both.grid(sticky='n')
        #cambio de frames
        for frame in (self.frame_both, self.frame_top):
            frame.grid(row=0, column=1, columnspan=2, rowspan=3, pady=1, padx=1, sticky='new')
        #interacción tabla_registro
        Label(self.frame_top).grid()
        Label(self.frame_both).grid()
        add = Button(self.frame_top, text='Agregar', command=self.frame_both.lift).grid(column=1, row=0, pady=170, padx=215)
        ok = Button(self.frame_both, text='Ok').grid(row=10, column=0, columnspan=2, sticky='we')
        cancel = Button(self.frame_both, text='Cancelar', command=self.frame_top.lift).grid(row=10, column=2, columnspan=2, sticky='we')
        #llamando función de cambio dínamico
        raise_frame(self.frame_top)

        #mensaje de salida
        self.message = Label(self.lower_frame)
        self.message.grid(row=3, column=0)

        #Etiquetas-Labels
        Label(self.frame_both, text='Nombre del dueño:', fg='blue4', bg='gray80').grid(row=1, column=0, sticky='nsew')
        Label(self.frame_both, text='Marca:', fg='blue4', bg='gray80').grid(row=1, column=2, sticky='nsew')
        Label(self.frame_both, text='Modelo').grid(row=2, column=0)
        Label(self.frame_both, text='Número de celular:').grid(row=2, column=2)
        Label(self.frame_both, text='Precio:', fg='blue4', bg='gray80').grid(row=3, column=0, sticky='nsew')
        Label(self.frame_both, text='Presupuesto', fg='blue4', bg='gray80').grid(row=3, column=2, sticky='nsew')
        Label(self.frame_both, text='Síntomas:').grid(row=4, column=0, columnspan=4, sticky='w')
        Label(self.frame_both, text='Modificaciones:').grid(row=6, column=0, columnspan=4, sticky='w')
        #Label().grid()
        #Entradas
        self.name = Entry(self.frame_both)
        self.number = Entry(self.frame_both)
        self.budget = Entry(self.frame_both)
        self.price = Entry(self.frame_both)
        self.marca = Entry(self.frame_both)
        self.modelo = Entry(self.frame_both)
        self.symptom = Text(self.frame_both, height=6, width=60)
        self.extra = Text(self.frame_both, height=6, width=60)
        #self.diag = Entry(frame_both)
        #configuración de entradas
        self.name.focus()
        self.name.grid(row=1, column=1, sticky='we')
        self.number.grid(row=1, column=3, sticky='we')
        self.budget.grid(row=2, column=1, sticky='we')
        self.price.grid(row=2, column=3, sticky='we')
        self.marca.grid(row=3, column=1, sticky='we')
        self.modelo.grid(row=3, column=3, sticky='we')
        self.symptom.grid(row = 5, column = 0, columnspan = 4,sticky = 'w', pady = 5)
        self.extra.grid(row = 9, column = 0, columnspan = 4,sticky = 'nw', pady = 5)


#crea una instancia
root = Tk()
app = Window(root)
#Desactiva el maximizar ventana
#root.resizable(0, 0)
#inicia la interfaz
root.mainloop()
