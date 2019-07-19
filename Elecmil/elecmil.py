# Simple enough, just import everything from tkinter.
from tkinter import *
from tkinter import ttk
import tkinter as tk
from icons import *
import time
import sqlite3
import os.path
# Here, we are creating our class, Window, and inheriting from the Frame
# class. Frame is a class from the tkinter module. (see Lib/tkinter/__init__)

class Window(Frame):

    db_name = 'database.db'


    # Define settings upon initialization. Here you can specify
    def __init__(self, priven=None):
            # parameters that you want to send through the Frame class.
        Frame.__init__(self, priven)
        def raise_frame(frame):
            frame.tkraise()
        #reference to the master widget, which is the tk window
        self.priven = priven
        #with that, we want to then run init_window, which doesn't yet exist
        self.init_window()
        self.priven.title('ElecmilV (1.0)')
        self.priven.iconbitmap('ico.ico')
        self.priven.configure(background = 'grey')
        #----------------------------------------_______________________________________#
        global master_frame
        master_frame = LabelFrame(self.priven, text = 'más información')
        master_frame.grid(row = 0, column = 0, rowspan = 2, pady = 5, padx = 5)
        #-------------------------------Guia--------------------------------------

        frame1 = LabelFrame(master_frame)
        frame1.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'n')#<------------------------------
        guia = Button(frame1, text = 'Guia')
        guia.grid(padx = 185, pady = 50)
        #---------------------------------Lista----------------------------------#
        frame3 = LabelFrame(master_frame, text = 'Lista')
        frame3.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = 'n')#<---------------
        self.tree = ttk.Treeview(frame3, selectmode='extended', height = 20, columns = '0, 1, 2, 3')
        self.tree.grid_propagate(False)
        self.tree.grid(row = 0, column = 0, sticky='nsew', padx = 5, pady = 10)
        self.tree.heading('#0', text = 'Estado', anchor = CENTER)
        self.tree.column('#0', width=90, stretch=False)
        self.tree.heading('#1', text = 'Nombre', anchor = CENTER)
        self.tree.column('#1', width=175, stretch=False)
        self.tree.heading('#2', text = 'Fecha', anchor = CENTER)
        self.tree.column('#2', width=150)
        self.tree.heading('#3', text = 'Marca', anchor = CENTER)
        self.tree.column('#3', width=150)
        self.tree.heading('#4', text = 'Modelo', anchor = CENTER)
        self.tree.column('#4', width=150)

        void = LabelFrame(self.priven, height = 100, width = 100, text = 'Hola')
        void.grid_propagate(False)
        void.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = 'nsew')

        #ejecución consulta
        self.get_products()


        #Frames
        f1 = LabelFrame(self.priven, text='Agregar', height = 225, width = 500, padx =5)
        f1.grid_propagate(False)
        f1.grid()
        global frame2
        frame2 = LabelFrame(self.priven, text='Registrador', height = 225, width = 500, padx =5)
        frame2.grid_propagate(False)
        frame2.grid(stick = 'n')
        #cambio dinamico de frame--------------------------------------------
        #cambio dinamico de frame2----------------------------------------------
        for frame in (f1, frame2):
            frame.grid(row = 0, column = 1, pady = 5, padx = 5, sticky = 'news')
        #Boton agregar
        add = Button(f1, text='Agregar', command=frame2.lift).grid(column = 1, row = 0, pady =170, padx = 215)
        #colocando label en grilla
        Label(f1).grid()
        #boton cancelar
        cancel = Button(frame2,text = 'Cancelar', command=f1.lift).grid(row = 10, column = 2, columnspan = 2, sticky ='we')
        #colocando label en grilla
        Label(frame2).grid()
        #Boton ok
        ok = Button(frame2, text = 'Ok', command =self.add_product).grid(row = 10, column = 0, columnspan = 2, sticky = 'we')
        #Mensajes de salida
        self.message = Label(void, text = '', fg = 'red')
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = 'nsew')
        #función
        raise_frame(f1)


        #---------------------------Registro---------------------------------------#
        Label(frame2, text = 'Nombre del dueño:', fg="blue4", bg ="gray80").grid(row = 1, column = 0, sticky='w')
        self.name = Entry(frame2)
        self.name.focus()
        self.name.grid(row = 1, column = 1, sticky='w')
        #-----------------------------------------------------------------------------#
        Label(frame2, text = 'Número de telefono:', fg="blue4", bg ="gray80").grid(row = 1, column = 2, sticky='w')
        self.numberp = Entry(frame2)
        self.numberp.grid(row = 1, column = 3, sticky='w', padx = 5)
        #-------------------------------------------------------------------------------#
        Label(frame2, text = 'Presupuesto:').grid(row = 2, column = 0)
        self.budget = Entry(frame2)
        self.budget.grid(row = 2, column = 1, sticky='w')
        #--------------------------------------------------------------------------------#
        Label(frame2, text = 'Precio:').grid(row = 2, column = 2)
        self.price = Entry(frame2)
        self.price.grid(row = 2, column = 3, sticky='w', padx = 5)
        #Marca
        Label(frame2, text = 'Marca:', fg="blue4", bg ="gray80").grid(row = 3, column = 0, sticky = 'nsew')
        self.marca = Entry(frame2)
        self.marca.grid(row = 3, column = 1)
        #Modelo
        Label(frame2, text = 'Modelo:', fg="blue4", bg ="gray80").grid(row = 3, column = 2, sticky = 'nsew')
        self.modelo = Entry(frame2)
        self.modelo.grid(row = 3, column = 3)
        #-------------------------------------------------------------------------------#
        Label(frame2, text = 'Síntomas:').grid(row = 4, column = 0, columnspan = 4, sticky = 'nsew')
        self.symptom = Text(frame2, height=6, width=60)
        self.symptom.grid(row = 5, column = 0, columnspan = 4,sticky = 'w', pady = 5)
        #---------------------------------------------------------------------
        #modificaciones
        Label(frame2, text = 'Modificaciones:', fg="blue4", bg ="gray80").grid(row = 6, column = 0,columnspan = 4, sticky = 'nsew')
        self.extra = Text(frame2, height=6, width=60)
        self.extra.grid(row = 9, column = 0, columnspan = 4,sticky = 'nw', pady = 5)
        #------------------------------------------------------------------------------#

        Label(frame2, text = 'Diagnóstico:')
        self.diag = Text(frame2, height=6, width=60, fg="blue4", bg ="gray80")
        self.diag.grid(row = 9, column = 0, columnspan = 4,sticky = 'nw', pady = 5)
        #---------------------------------------------------------------------#


    def dateii(self):
        datet = time.strftime("%d/%m/%y")
        return datet

    def onExit(self):
        self.quit()
        #_____________________________________________________________________________________#
    #Creation of init_window
    def init_window(self):
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Exit", command=self.onExit)
        menubar.add_cascade(label="File", menu=fileMenu)
        #------------------------------------------------------------------------------#

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

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
            self.tree.insert('',0, values=(row[1], row[2], row[3], row[4]))

    def validation(self):
        return len(self.name.get()) != 0 and len(self.marca.get()) !=0

    def add_product(self):
        if self.validation():
            query = 'INSERT INTO libreta(nombre, marca, modelo) VALUES(?, ?, ?)'
            parameters = (self.name.get(), self.marca.get(), self.modelo.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Guardado Satisfactoriamente'
            self.name.delete(0, END)
            self.marca.delete(0, END)
            self.modelo.delete(0, END)
        else:
            self.message['text'] = 'El nombre del dueño y la marca del dispositivo son obligatorios!'
        self.get_products()
# root window created. Here, that would be the only window, but
# you can later have windows within windows.
root = Tk()
#creation of an instance
app = Window(root)
#mainloop
root.mainloop()
