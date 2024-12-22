"""в двух текстовых файлах содержатся наборы чисел.
Считать эти значения, отсортировать. В первом списке найти наибольшее,
во втором списке найти наименьшее и перенести их в противоположные списки,
вставив их без нарушения сортировки и записать обратно в файлы"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class FileProcessor:
    def __init__(self, master):
        self.master = master
        master.title("Обработка числовых файлов")

        # Фрейм для первого файла
        frame1 = ttk.LabelFrame(master, text="Первый файл")
        frame1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.file1_label = ttk.Label(frame1, text="Файл не выбран")
        self.file1_label.pack(pady=5)
        self.file1_button = ttk.Button(frame1, text="Выбрать файл", command=lambda: self.select_file(1))
        self.file1_button.pack(pady=5)

        # Фрейм для второго файла
        frame2 = ttk.LabelFrame(master, text="Второй файл")
        frame2.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.file2_label = ttk.Label(frame2, text="Файл не выбран")
        self.file2_label.pack(pady=5)
        self.file2_button = ttk.Button(frame2, text="Выбрать файл", command=lambda: self.select_file(2))
        self.file2_button.pack(pady=5)

         # Кнопка запуска обработки
        self.process_button = ttk.Button(master, text="Обработать файлы", command=self.process_files, state="disabled")
        self.process_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Файловые пути
        self.file1_path = None
        self.file2_path = None

    def select_file(self, file_num):
        """Открывает диалог выбора файла и сохраняет путь."""
        file_path = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if file_path:
            if file_num == 1:
                self.file1_path = file_path
                self.file1_label.config(text=os.path.basename(file_path))
            elif file_num == 2:
                self.file2_path = file_path
                self.file2_label.config(text=os.path.basename(file_path))

            if self.file1_path and self.file2_path:
                self.process_button.config(state="normal")

    def read_and_sort_numbers(self, file_path):
      """Считывает числа из файла, сортирует и возвращает список."""
      try:
        with open(file_path, 'r') as file:
            numbers = [int(line.strip()) for line in file if line.strip().isdigit()] # Фильтруем только числа
            numbers.sort()
            return numbers
      except Exception as e:
         messagebox.showerror("Ошибка чтения файла", f"Не удалось прочитать файл {file_path}: {e}")
         return None
    def process_files(self):
        """Основная функция обработки файлов."""
        if not self.file1_path or not self.file2_path:
            messagebox.showerror("Ошибка", "Выберите оба файла.")
            return

        numbers1 = self.read_and_sort_numbers(self.file1_path)
        numbers2 = self.read_and_sort_numbers(self.file2_path)

        if not numbers1 or not numbers2:
           return # Возвращаемся, если есть ошибка чтения


        try:

            max1 = numbers1[-1] #  Самое большое число в первом списке
            min2 = numbers2[0] # Самое маленькое число во втором списке

            numbers1.remove(max1) # удаляем максимальное из первого
            numbers2.remove(min2) # удаляем минимальное из второго

            self.insert_sorted(numbers1, min2) # Добавляем минимальное из 2го в 1й
            self.insert_sorted(numbers2, max1) # Добавляем максимальное из 1го во 2й

            self.write_to_file(self.file1_path, numbers1) # записываем первый список в файл
            self.write_to_file(self.file2_path, numbers2) # записываем второй список в файл

            messagebox.showinfo("Успех", "Файлы успешно обработаны.")

        except Exception as e:
            messagebox.showerror("Ошибка обработки", f"Не удалось обработать файлы: {e}")

    def insert_sorted(self, numbers, number):
        """Вставляет число в отсортированный список с сохранением сортировки."""
        i = 0
        while i < len(numbers) and numbers[i] < number:
            i += 1
        numbers.insert(i, number)

    def write_to_file(self, file_path, numbers):
        """Записывает список чисел в файл."""
        try:
            with open(file_path, 'w') as file:
                for number in numbers:
                  file.write(str(number) + '\n')
        except Exception as e:
            messagebox.showerror("Ошибка записи файла", f"Не удалось записать в файл {file_path}: {e}")


root = tk.Tk()
processor = FileProcessor(root)
root.mainloop()
