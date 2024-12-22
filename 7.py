"""в текстовом файле записан текст, в котором имеются названия городов.
Откорректировать текст, чтобы с заглавной буквы были
только названия городов и первые слова в предложении"""
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import re

# работает криво

def load_file():
    """Загрузить текст из файла."""
    filepath = filedialog.askopenfilename(filetypes=[("Текстовые файлы", "*.txt")])
    if filepath:
        with open(filepath, "r", encoding="utf-8") as file:
            text = file.read()
        text_display.delete("1.0", tk.END)
        text_display.insert(tk.END, text)


def save_file():
    """Сохранить обработанный текст в файл."""
    filepath = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Текстовые файлы", "*.txt")],
    )
    if filepath:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(text_display.get("1.0", tk.END).strip())
        messagebox.showinfo("Успех", "Файл успешно сохранен!")


def correct_text():
    """Обработать текст в текстовом виджете."""
    text = text_display.get("1.0", tk.END).strip()  # Получить текст из виджета

    # Список городов России
    cities = {
        "Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань",
        "Нижний Новгород", "Челябинск", "Самара", "Омск", "Ростов-на-Дону",
        "Уфа", "Красноярск", "Пермь", "Воронеж", "Волгоград", "Краснодар",
        "Саратов", "Тюмень", "Тольятти", "Ижевск", "Барнаул", "Ульяновск",
        "Иркутск", "Хабаровск", "Ярославль", "Владивосток", "Махачкала",
        "Томск", "Оренбург", "Кемерово", "Рязань", "Астрахань", "Пенза",
        "Липецк", "Тула", "Киров", "Чебоксары", "Курск", "Брянск", "Иваново",
        "Магнитогорск", "Тверь", "Ставрополь", "Белгород", "Сочи", "Калуга",
        "Архангельск", "Смоленск", "Владикавказ", "Якутск", "Грозный",
        "Чита", "Кострома", "Псков", "Нальчик", "Петрозаводск", "Новокузнецк",
        "Сургут", "Тамбов", "Мурманск", "Волжский", "Великий Новгород",
        "Новороссийск"
    }

    # Приведение к регистру для проверки городов
    cities_lower = {city.lower(): city for city in cities}

    # Разделение текста на предложения
    sentences = re.split(r"([.!?]\s*)", text)
    corrected_text = ""

    for i in range(0, len(sentences), 2):
        if i < len(sentences):
            sentence = sentences[i].strip()  # Текст предложения
            delimiter = sentences[i + 1] if i + 1 < len(sentences) else ""  # Разделитель

            # Разделить предложение на слова
            words = sentence.split()

            # Обработка слов в предложении
            for idx, word in enumerate(words):
                word_lower = re.sub(r"[^\w-]", "", word).lower()  # Удаляем пунктуацию для проверки
                # Если это первый слово в предложении
                if idx == 0:
                    words[idx] = word.capitalize()
                # Если это название города
                elif word_lower in cities_lower:
                    # Сохраняем пунктуацию, если есть
                    words[idx] = word.replace(word_lower, cities_lower[word_lower])

            # Собрать предложение обратно
            corrected_sentence = " ".join(words)
            corrected_text += corrected_sentence + delimiter

    # Обновить текст в виджете
    text_display.delete("1.0", tk.END)
    text_display.insert(tk.END, corrected_text)


# Создание главного окна tkinter
root = tk.Tk()
root.title("Инструмент для обработки текста")

# Создание компонентов интерфейса
frame = tk.Frame(root)
frame.pack(pady=10)

load_button = ttk.Button(frame, text="Загрузить файл", command=load_file)
load_button.pack(side=tk.LEFT, padx=5)

correct_button = ttk.Button(frame, text="Обработать текст", command=correct_text)
correct_button.pack(side=tk.LEFT, padx=5)

save_button = ttk.Button(frame, text="Сохранить файл", command=save_file)
save_button.pack(side=tk.LEFT, padx=5)

text_display = tk.Text(root, wrap=tk.WORD, height=20, width=60)
text_display.pack(padx=10, pady=10)

# Запуск главного цикла tkinter
root.mainloop()
