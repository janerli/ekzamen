"""в текстовом файле записаны имена, вывести их на форму,
отсортировать и записать в другой файл"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class NameApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Работа с именами")
        self.window.geometry("600x400")

        self.names = []  # Список для хранения имен
        self.file_path = None  # Переменная для хранения пути к файлу

        # Кнопка выбора файла
        self.select_file_button = ttk.Button(window, text="Выбрать файл", command=self.select_file)
        self.select_file_button.pack(pady=10)

        # Текстовое поле для отображения имен
        self.names_text = tk.Text(window, height=15, width=70)
        self.names_text.pack(pady=10)

        # Кнопка сортировки
        self.sort_button = ttk.Button(window, text="Отсортировать", command=self.sort_names)
        self.sort_button.pack(pady=5)

        # Кнопка сохранения
        self.save_button = ttk.Button(window, text="Сохранить отсортированные имена", command=self.save_names)
        self.save_button.pack(pady=5)

    def select_file(self):
        """Открывает файл и считывает имена."""
        self.file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if self.file_path:
            try:
                with open(self.file_path, 'r', encoding='utf-8') as file:
                    self.names = [line.strip() for line in file if line.strip()]
                    self.display_names(self.names)
            except Exception as e:
                messagebox.showerror("Ошибка чтения файла", f"Не удалось прочитать файл: {e}")
                self.names = []
        else:
            self.names = []

    def display_names(self, names):
        """Отображает имена в текстовом поле."""
        self.names_text.delete(1.0, tk.END)
        for name in names:
            self.names_text.insert(tk.END, name + '\n')

    def sort_names(self):
        """Сортирует имена и отображает их."""
        if self.names:
            sorted_names = sorted(self.names)
            self.display_names(sorted_names)
            self.names = sorted_names
        else:
            messagebox.showerror("Ошибка", "Сначала выберите файл")

    def save_names(self):
        """Сохраняет отсортированные имена в файл."""
        if self.names:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
            if file_path:
                try:
                    with open(file_path, 'w', encoding='utf-8') as file:
                        for name in self.names:
                            file.write(name + '\n')
                    messagebox.showinfo("Успех", "Имена успешно сохранены.")
                except Exception as e:
                    messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить имена: {e}")
        else:
            messagebox.showerror("Ошибка", "Сначала выберите файл")


# Создание главного окна
window = tk.Tk()
app = NameApp(window)
window.mainloop()
