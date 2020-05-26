import sqlite3

class RecorderData(object):

    def delete(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text']
            self.message['text'] = 'Elemento borrado Satisfactoriamente'
        except IndexError as e:
            self.message['text'] = 'No hay nada seleccionado'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM libreta WHERE id =(?)'
        self.run_query(query, (name,))

        self.get_products()

    def complete(self):
        print('Hola')

    # database
    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_products(self):
        # limpiador de tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # consultando datos
        query = 'SELECT * FROM libreta'
        db_rows = self.run_query(query)
        # rellenando datos
        for row in db_rows:
            self.tree.insert('', 0, text=row[1], values=(row[1], row[3], row[4], row[2]))

    def validation(self):
        return len(self.name.get()) != 0 and len(self.brand.get()) != 0

    # Record data
    def add_product(self):
        if self.validation():
            query = 'INSERT INTO libreta(nombre, marca, modelo, datei) VALUES(?, ?, ?, date())'
            parameters = (
                self.name.get(),
                self.brand.get(),
                self.model.get()
            )

            self.run_query(query, parameters)
            self.message['text'] = 'Guardado Satisfactoriamente'
            self.name.delete(0, END)
            self.brand.delete(0, END)
            self.model.delete(0, END)
        else:
            self.message['text'] = 'El nombre del dueño y la marca del dispositivo son obligatorios!'
        self.get_products()

    def __init__(self):
        db_name = 'database.db'
