import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import *


class DatabaseController:
    db_name = 'database.db'

    def get_products(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        query = 'SELECT * FROM datos'
        db_rows = self.run_query(query)

        for row in db_rows:
            self.tree.insert('', 0, text=row[0], values=(row[0], row[1], row[2]))

    def validation(self):
        return len(self.owner_name.get()) != 0 and len(self.phone_number.get()) != 0

    def complete(self):
        if self.validation():
            query = 'INSERT INTO datos(owner_name, phone_number) VALUES(?, ?)'
            parameters = (self.owner_name.get(), self.phone_number.get())
            self.run_query(query, parameters)
            print('Guardado Satisfactoriamente')
            self.owner_name.delete(0, END)
            self.phone_number.delete(0, END)
        else:
            print('El nombre del dueño y la marca del dispositivo son obligatorios!')
        self.get_products()

    def delete(self):
        print()
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            print('Nada seleccionado')
            return
        name = self.tree.item(self.tree.selection())['values'][0]
        query = "DELETE FROM datos WHERE unique_id=?"
        self.run_query(query, (name,))
        self.get_products()
        print('Limpio')

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result


class MainWindow(Frame, DatabaseController):

    def OnDoubleClick(self, event):
        try:
            item = self.tree.selection()[0]
            print("you clicked on", self.tree.item(item, "text"))
            self.popup_bonus()
            if len(self.tree.selection()) > 0:
                self.tree.selection_remove(self.tree.selection()[0])

        except IndexError as e:
            print('Nada seleccionado')

    def popup_bonus(self):
        self.win = tk.Toplevel()
        self.win.wm_title("Window")

        l = tk.Label(self.win, text="Input")
        l.grid(row=0, column=0)

        b = ttk.Button(self.win, text="Okay", command=self.win.destroy)
        b.grid(row=1, column=0)

    def popup_showinfo(self):
        self.showinfo("Window", "Hello World!")

    def Registrator(self):
        # Labels
        Label(text='Nombre del dueño:', fg="blue4", bg="gray80").grid(row=0, column=0, sticky='w')
        self.owner_name.focus()
        self.owner_name.grid(row=0, column=1, sticky='w')

        Label(text='Número de telefono:', fg="blue4", bg="gray80").grid(row=0, column=2, sticky='w')
        self.phone_number.grid(row=0, column=3, sticky='w')

        Label(text='Marca').grid(row=1, column=0, sticky='w')
        self.brand.grid(row=1, column=1, sticky='w')

        Label(text='Modelo').grid(row=1, column=2, sticky='w')
        self.model.grid(row=1, column=3, sticky='w')

    def init_window(self):
        # Interface
        self.Registrator()

        # Buttons
        ok = Button(text='Guardar', command=lambda: [self.complete()])
        ok.grid(row=2, column=0, columnspan=2, sticky='we')
        delete = Button(text='Borrar', command=self.delete)
        delete.grid(row=2, column=2, columnspan=2, sticky='we')

        # List
        self.tree = ttk.Treeview(
            height=10,
            show='headings',
            columns=(
                'unique_id',
                'owner_name',
                'phone_number'
            ),
            selectmode='extended')
        self.tree.grid_propagate(False)
        self.tree.grid(row=3, column=0, columnspan=4, sticky='nsew', padx=5, pady=10)
        # Headers
        self.tree.heading('unique_id', text='unique_id', anchor=CENTER)
        self.tree.heading('owner_name', text='Nombre', anchor=CENTER)
        self.tree.heading('phone_number', text='Numero de celular', anchor=CENTER)

        # Headers Size
        self.tree.column('#0', minwidth=20, width=40)
        self.tree.column('#1', minwidth=20, width=130)
        self.tree.column('#2', minwidth=20, width=110)

        self.tree.bind("<Double-1>", self.OnDoubleClick)

        # query
        self.get_products()

    def __init__(self, priven=None):
        Frame.__init__(self, priven)
        # Inputs
        self.owner_name = Entry()
        self.phone_number = Entry()
        self.brand = Entry()
        self.model = Entry()

        self.priven = priven
        self.init_window()

root = Tk()
app = MainWindow(root)
root.resizable(0, 0)
root.mainloop()
