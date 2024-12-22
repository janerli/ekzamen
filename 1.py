import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# универсальная штука можно посмотреть любую таблицу из БД


def connect_to_db(db_name):
    """Connects to the SQLite database."""
    try:
        conn = sqlite3.connect(db_name)
        return conn
    except sqlite3.Error as e:
        messagebox.showerror("Ошибка подключения", f"Не удалось подключиться к базе данных: {e}")
        return None


def fetch_tables(conn):
    """Fetches a list of table names from the database."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        return [table[0] for table in tables]  # Return a list of table names
    except sqlite3.Error as e:
        messagebox.showerror("Ошибка получения списка таблиц", f"Не удалось получить список таблиц: {e}")
        return []


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


class DatabaseViewer:
    def __init__(self, master, db_name):
        self.master = master
        master.title("Просмотр и удаление данных")
        self.db_name = db_name
        self.conn = connect_to_db(db_name)
        self.table_name = ""  # Store the currently selected table name
        self.all_tables = []

        if self.conn:
            self.create_widgets()
            self.load_tables()

    def create_widgets(self):
        # Поле ввода номера строки
        row_id_label = ttk.Label(self.master, text="Введите номер строки (ROWID):")
        row_id_label.grid(row=0, column=0, padx=5, pady=5)
        self.row_id_entry = ttk.Entry(self.master)
        self.row_id_entry.grid(row=0, column=1, padx=5, pady=5)

        # Кнопка удаления
        delete_button = ttk.Button(self.master, text="Удалить строку", command=self.delete_row)
        delete_button.grid(row=0, column=2, padx=5, pady=5)

        # Таблица для отображения данных
        self.tree = ttk.Treeview(self.master, show="headings")
        self.tree.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Список таблиц
        table_list_label = ttk.Label(self.master, text="Выберите таблицу:")
        table_list_label.grid(row=1, column=2, padx=5, pady=5)
        self.table_list = tk.Listbox(self.master, width=20)
        self.table_list.grid(row=2, column=2, padx=5, pady=5)
        self.table_list.bind("<Double-Button-1>", self.load_table_data)

    def load_tables(self):
        """Loads and displays table names in the listbox."""
        if self.conn:
            self.all_tables = fetch_tables(self.conn)
            for table in self.all_tables:
                self.table_list.insert(tk.END, table)

    def load_table_data(self, event):
         """Loads data for the selected table in the treeview."""
         selected_index = self.table_list.curselection()
         if selected_index:
             self.table_name = self.all_tables[selected_index[0]]  # get the selected table name
             self.load_data()

    def load_data(self):
        """Loads and displays data in the treeview."""
        if self.table_name and self.conn: # Make sure the table name is not empty
             data = fetch_data(self.conn, self.table_name)

             # Determine column names dynamically
             if data:
                column_names = [f"column{i+1}" for i in range(len(data[0]))]
                self.tree["columns"] = column_names
                for i, col in enumerate(column_names):
                    self.tree.heading(col, text=f"Column {i+1}")

                self.tree.delete(*self.tree.get_children())
                for row in data:
                    self.tree.insert("", tk.END, values=row)
             else:
                 self.tree["columns"] = () #Clear columns in the case of empty table
                 self.tree.delete(*self.tree.get_children())


    def delete_row(self):
        """Deletes a row from the currently selected table."""
        row_id = self.row_id_entry.get()
        try:
            row_id = int(row_id)
            if self.table_name and delete_row(self.conn, self.table_name, row_id):
                messagebox.showinfo("Успех", "Строка успешно удалена!")
                self.load_data()  # Обновляем таблицу после удаления
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный номер строки. Введите целое число.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

root = tk.Tk()
viewer = DatabaseViewer(root, 'example.db') # Замените на имя вашей БД
root.mainloop()
