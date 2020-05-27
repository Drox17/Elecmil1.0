import sqlite3
import tkinter as tk
from tkinter import ttk, OptionMenu
from tkinter import *


class DatabaseController:
    db_name = 'database.db'

    def SaveChoice(self, work_option):
        idd = self.reference_value
        new_option = self.optionVar.get()
        query = "UPDATE datos SET option_work= ? WHERE unique_id= ?"
        parameters = (
            new_option,
            idd
        )
        self.run_query(query, (new_option, idd))
        self.get_products()

    def updated_choices (self, new_option):
        query = "UPDATE datos SET option_work = ?"
        parameters = (new_option,)
        self.run_query(query, parameters)
        self.get_progress_work()

    def get_option_work(self):
        with sqlite3.connect(self.db_name) as conn:
            id = self.reference_value
            conn.row_factory = lambda cursor, row: row[0]
            cursor = conn.cursor()
            cursor.execute("SELECT option_work FROM datos WHERE unique_id='{}'".format(id))
            result_set = cursor.fetchall()
            self.result_set = result_set





    def get_products (self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        query = 'SELECT * FROM datos'
        db_rows = self.run_query(query)

        for row in db_rows:
            # sort items according to index or unique_id
            self.tree.insert('', 0, text=row[6], values=(row[0], row[1], row[2], row[3], row[4], row[5], row[7]))

    def complete (self):
        if self.validation():
            query = 'INSERT INTO datos(owner_name, phone_number, brand, model, serie) VALUES(?, ?, ?, ?, ?)'
            parameters = (
                self.owner_name.get(),
                self.phone_number.get(),
                self.brand.get(),
                self.model.get(),
                self.serie.get(),
            )
            self.run_query(query, parameters)
            print('Guardado Satisfactoriamente')
            self.owner_name.delete(0, END)
            self.phone_number.delete(0, END)
            self.brand.delete(0, END)
            self.model.delete(0, END)
            self.serie.delete(0, END)
        else:
            print('El nombre del dueño y la marca del dispositivo son obligatorios!')
        self.get_products()

    def validation (self):
        return len(self.owner_name.get()) != 0 and len(self.phone_number.get()) != 0

    def delete (self):
        print()
        try:
            # Get index as reference for delete object
            item = self.tree.selection()[0]
            self.tree.item(item, "text")
        except IndexError as e:
            print('Error')
            return
        idd = self.tree.item(item, "text")
        query = "DELETE FROM datos WHERE unique_id=?"
        self.run_query(query, (idd,))
        self.get_products()
        print('Limpio')

    def run_query (self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

class MainWindow(Frame, DatabaseController):
    work_process: OptionMenu

    def OnDoubleClick (self, event):
        try:
            item = self.tree.selection()[0]
            # self.reference_value have unique_id
            self.reference_value = self.tree.item(item, "text")
            self.popup_bonus()
            if len(self.tree.selection()) > 0:
                self.tree.selection_remove(self.tree.selection()[0])
                self.get_option_work()

        except IndexError as e:
            print('Nada seleccionado')

    def popup_bonus (self):
        self.win = tk.Toplevel()
        self.win.wm_title("Cliente")
        self.win.geometry('350x200')

        button_accept = tk.Label(self.win, text="Tablero")
        button_accept.grid(row=0, column=0)

        self.optionVar = StringVar()

        self.get_option_work()
        option_choosed = self.result_set
        # condicion de estado del trabajo
        if option_choosed == 'None':
            self.optionVar.set("En Espera")
        else:
            self.get_option_work()
            self.optionVar.set(option_choosed)

        option = OptionMenu(self.win, self.optionVar, "En Curso", "En Espera", "Completado", "No Completado")
        option.grid(row=1, column=0, sticky='nswe')

        b = ttk.Button(self.win, text="Okay", command=lambda: [self.win.destroy(),
                                                               self.show()])
        b.grid(row=2, column=0)

    def show (self):
        work_option = self.optionVar.get()
        self.color_item(work_option)
        self.SaveChoice(work_option)
        return work_option

    def color_item (self, work_option):
        if work_option == "En Curso":
            print('Celeste')
        elif work_option == "En Espera":
            print('Amarillo')
        elif work_option == "Completado":
            print('Verde')
        else:
            print('Rojo')

    def Registrator_interfaces (self):

        # Frames
        self.master_frame = LabelFrame(self.priven)
        self.master_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')
        self.registrator_frame = LabelFrame(self.master_frame, text='Registrador', height=200, width=100)
        self.registrator_frame.grid(row=1, column=0, sticky='nswe')

        # Inputs
        self.owner_name = Entry(self.registrator_frame)
        self.phone_number = Entry(self.registrator_frame)
        self.brand = Entry(self.registrator_frame)
        self.model = Entry(self.registrator_frame)
        self.serie = Entry(self.registrator_frame)
        # self.budget = Entry(self.registrator_frame)

        # Labels
        Label(self.registrator_frame, text='Nombre del dueño:', fg="blue4", bg="gray80").grid(row=0, column=0,
                                                                                              sticky='w')
        self.owner_name.focus()
        self.owner_name.grid(row=0, column=1, sticky='w')

        Label(self.registrator_frame, text='Número de telefono:', fg="blue4", bg="gray80").grid(row=0, column=2,
                                                                                                sticky='we')
        self.phone_number.grid(row=0, column=3, sticky='w')

        Label(self.registrator_frame, text='Marca:').grid(row=1, column=0, sticky='we')
        self.brand.grid(row=1, column=1, sticky='w')

        Label(self.registrator_frame, text='Modelo:').grid(row=1, column=2, sticky='we')
        self.model.grid(row=1, column=3, sticky='w')

        Label(self.registrator_frame, text='Serie:', fg="blue4", bg="gray80").grid(row=2, column=0, sticky='we')
        self.serie.grid(row=2, column=1)

        # Label(self.registrator_frame, text='Pago:', fg="blue4", bg="gray80").grid(row=2, column=2, sticky='we')
        # self.budget.grid(row=2, column=3, sticky='w')

    def init_window (self):
        # Interface
        self.Registrator_interfaces()

        # Buttons
        ok = Button(text='Guardar', command=lambda: [self.complete()])
        ok.grid(row=2, column=0, sticky='we')
        delete = Button(text='Borrar', command=self.delete)
        delete.grid(row=2, column=1, sticky='we')

        # List
        self.tree = ttk.Treeview(
            height=10,
            show='headings',
            columns=(
                'owner_name',
                'phone_number',
                'brand',
                'model',
                'serie',
                'option_work'
            ),
            selectmode='extended')
        self.tree.grid_propagate(False)
        self.tree.grid(row=3, column=0, columnspan=4, sticky='nsew', padx=5, pady=10)
        # Headers
        self.tree.heading('option_work', text='Estado', anchor=CENTER)
        self.tree.heading('owner_name', text='Nombre', anchor=CENTER)
        self.tree.heading('phone_number', text='Numero de celular', anchor=CENTER)
        self.tree.heading('brand', text='Marca', anchor=CENTER)
        self.tree.heading('serie', text='Serie', anchor=CENTER)
        self.tree.heading('model', text='Modelo', anchor=CENTER)

        # Headers Size
        self.tree.column('#0', minwidth=20, width=40)
        self.tree.column('#1', minwidth=20, width=130)
        self.tree.column('#2', minwidth=20, width=110)
        self.tree.column('#3', minwidth=20, width=110)
        self.tree.column('#4', minwidth=20, width=110)
        self.tree.column('#5', minwidth=20, width=110)

        self.tree.bind("<Double-1>", self.OnDoubleClick)

        # query
        self.get_products()

    def __init__ (self, priven=None):
        Frame.__init__(self, priven)
        self.value = None
        self.priven = priven
        self.init_window()
        self.priven.title('Elecmil-V (0.1)')
        self.priven.iconbitmap('ico.ico')
        self.priven.configure(background='grey')


root = Tk()
app = MainWindow(root)
root.resizable(0, 0)
root.mainloop()
