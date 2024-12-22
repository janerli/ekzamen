import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def connect_to_db(db_name):
    """Connects to the SQLite database."""
    try:
        conn = sqlite3.connect(db_name)
        return conn
    except sqlite3.Error as e:
        messagebox.showerror("Ошибка подключения", f"Не удалось подключиться к базе данных: {e}")
        return None

def fetch_data(conn, table_name):
    """Fetches data from the specified table."""
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()
        return data
    except sqlite3.Error as e:
        messagebox.showerror("Ошибка выборки данных", f"Не удалось получить данные: {e}")
        return []

def delete_row(conn, table_name, row_id):
    """Deletes a row from the specified table."""
    try:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {table_name} WHERE ROWID = ?", (row_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        messagebox.showerror("Ошибка удаления", f"Не удалось удалить строку: {e}")
        return False

def get_tables(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_sequence")
    tables = cursor.fetchall()
    return tables

tables = get_tables(connect_to_db('example.db'))
print(tables)

class DatabaseViewer:
    def __init__(self, master, db_name):
        self.master = master
        master.title("Просмотр и удаление данных")
        self.db_name = db_name
        self.conn = connect_to_db(db_name)

        if self.conn:
            self.tables = get_tables(self.conn)
            print(self.tables)
            self.create_widgets()

    def create_widgets(self):
        # Поле ввода номера строки
        row_id_label = ttk.Label(self.master, text="Введите номер строки (ROWID):")
        row_id_label.grid(row=0, column=0, padx=5, pady=5)
        self.row_id_entry = ttk.Entry(self.master)
        self.row_id_entry.grid(row=0, column=1, padx=5, pady=5)

        # Кнопка удаления
        delete_button = ttk.Button(self.master, text="Удалить строку", command=self.delete_row)
        delete_button.grid(row=0, column=2, padx=5, pady=5)
        table_list = tk.Listbox(self.master, listvariable=self.tables, selectmode='single')
        table_list.grid(row=0, column=3, padx=5, pady=5)

        # Таблица для отображения данных
        self.tree = ttk.Treeview(self.master, show="headings")
        self.tree.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Заголовки столбцов (замените на ваши названия столбцов)
        self.tree["columns"] = ("column1", "column2") #replace with your column names
        self.tree.heading("column1", text="Column 1")
        self.tree.heading("column2", text="Column 2") #replace with your column names

        self.load_data()

    def load_data(self):
        data = fetch_data(self.conn, self.table_name)
        self.tree.delete(*self.tree.get_children()) # Очищаем таблицу перед обновлением
        for row in data:
            self.tree.insert("", tk.END, values=row)


    def delete_row(self):
        row_id = self.row_id_entry.get()
        try:
            row_id = int(row_id)
            if delete_row(self.conn, self.table_name, row_id):
                messagebox.showinfo("Успех", "Строка успешно удалена!")
                self.load_data()  # Обновляем таблицу после удаления
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный номер строки. Введите целое число.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")


root = tk.Tk()
viewer = DatabaseViewer(root, 'example.db')
root.mainloop()



