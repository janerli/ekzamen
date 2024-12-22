"""дана последовательность n чисел, заданных случайным образом.
Поменять местами элементы стоящие на соседних позициях
(элементы стоящие на четных позициях с элементами стоящими на нечетных позициях)"""
import tkinter as tk
from tkinter import ttk, messagebox
import random


def swap_pairs(numbers):
    """Меняет местами элементы на четных и нечетных позициях."""
    for i in range(0, len(numbers) - 1, 2):
        numbers[i], numbers[i + 1] = numbers[i + 1], numbers[i]
    return numbers


def generate_numbers():
    """Генерирует случайную последовательность чисел."""
    try:
        n = int(num_entries.get())
        if n <= 0:
            messagebox.showerror("Ошибка", "Количество чисел должно быть положительным")
            return

        min_val = int(min_entry.get())
        max_val = int(max_entry.get())

        if min_val >= max_val:
            messagebox.showerror("Ошибка", "Минимальное значение должно быть меньше максимального")
            return

        numbers = [random.randint(min_val, max_val) for _ in range(n)]
        original_numbers_label.config(text=f"Исходные числа: {numbers}")

        swapped_numbers = swap_pairs(numbers.copy())  # Важно: делаем копию, чтобы не менять исходный массив
        swapped_numbers_label.config(text=f"После замены: {swapped_numbers}")
    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите целые числа в поля")


# Создание главного окна
window = tk.Tk()
window.title("Перестановка чисел")
window.geometry("500x300")

# Фрейм для ввода количества чисел
input_frame = ttk.Frame(window)
input_frame.pack(pady=10)

ttk.Label(input_frame, text="Количество чисел:").grid(row=0, column=0, padx=5, pady=5)
num_entries = ttk.Entry(input_frame)
num_entries.grid(row=0, column=1, padx=5, pady=5)
num_entries.insert(0, "10")  # Пример значения

# Фрейм для ввода диапазона
range_frame = ttk.Frame(window)
range_frame.pack(pady=10)

ttk.Label(range_frame, text="Минимальное значение:").grid(row=0, column=0, padx=5, pady=5)
min_entry = ttk.Entry(range_frame)
min_entry.grid(row=0, column=1, padx=5, pady=5)
min_entry.insert(0, "1")  # Пример значения

ttk.Label(range_frame, text="Максимальное значение:").grid(row=1, column=0, padx=5, pady=5)
max_entry = ttk.Entry(range_frame)
max_entry.grid(row=1, column=1, padx=5, pady=5)
max_entry.insert(0, "100")  # Пример значения

# Кнопка генерации
generate_button = ttk.Button(window, text="Сгенерировать и поменять", command=generate_numbers)
generate_button.pack(pady=10)

# Лейблы для вывода результатов
original_numbers_label = ttk.Label(window, text="Исходные числа: ")
original_numbers_label.pack(pady=5)

swapped_numbers_label = ttk.Label(window, text="После замены: ")
swapped_numbers_label.pack(pady=5)

window.mainloop()
