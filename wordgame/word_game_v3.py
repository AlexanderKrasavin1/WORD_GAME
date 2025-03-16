import random
import json
import tkinter as tk
from tkinter import messagebox, font

# Укажите путь к JSON-файлу
file_path = 'levels.json'
# Открываем файл и загружаем данные
with open(file_path, 'r', encoding='utf-8') as file:
    levels = json.load(file)
    print(levels)



SAVE_FILE = "progress.json"

def load_progress():
    try:
        with open(SAVE_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"level_index": 0, "completed_levels": []}

def save_progress(data):
    with open(SAVE_FILE, "w") as file:
        json.dump(data, file)

def reset_progress():
    save_progress({"level_index": 0, "completed_levels": []})

class WordGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Игра по уровням")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")  # Светло-серый фон
        
        # Шрифты
        self.title_font = font.Font(family="Helvetica", size=18, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=12)
        self.label_font = font.Font(family="Helvetica", size=12)
        
        progress = load_progress()
        self.level_index = progress["level_index"]
        self.completed_levels = list(set(progress["completed_levels"]))
        self.current_words = []
        self.guessed_words = []  # Список отгаданных слов на текущем уровне
        
        self.show_main_menu()
    
    def show_main_menu(self):
        self.clear_window()
        tk.Label(self.root, text="Добро пожаловать в игру!", font=self.title_font, bg="#f0f0f0", fg="#333333").pack(pady=20)
        
        # Кнопки меню
        button_style = {"font": self.button_font, "bg": "#4CAF50", "fg": "white", "activebackground": "#45a049", "bd": 0, "padx": 20, "pady": 10}
        tk.Button(self.root, text="Играть", command=self.start_game, **button_style).pack(pady=10)
        tk.Button(self.root, text="Пройденные уровни", command=self.show_completed_levels, **button_style).pack(pady=10)
        tk.Button(self.root, text="Сбросить прогресс", command=self.reset_game, **button_style).pack(pady=10)
        tk.Button(self.root, text="Выйти", command=self.quit_game, **button_style).pack(pady=10)
    
    def start_game(self):
        self.show_level_selection()
    
    def reset_game(self):
        reset_progress()
        self.level_index = 0
        self.completed_levels = []
        self.show_main_menu()
    
    def show_completed_levels(self):
        self.clear_window()
        tk.Label(self.root, text="Пройденные уровни", font=self.title_font, bg="#f0f0f0", fg="#333333").pack(pady=20)
        
        for level in sorted(set(self.completed_levels)):
            tk.Button(self.root, text=f"Уровень {level + 1}", command=lambda lvl=level: self.select_level(lvl),
                      font=self.button_font, bg="#2196F3", fg="white", activebackground="#1e88e5", bd=0, padx=20, pady=10).pack(pady=5)
        
        tk.Button(self.root, text="Назад в меню", command=self.show_main_menu,
                  font=self.button_font, bg="#607D8B", fg="white", activebackground="#546E7A", bd=0, padx=20, pady=10).pack(pady=10)
        tk.Button(self.root, text="Выйти", command=self.quit_game,
                  font=self.button_font, bg="#f44336", fg="white", activebackground="#e53935", bd=0, padx=20, pady=10).pack(pady=10)
    
    def show_level_selection(self):
        self.clear_window()
        tk.Label(self.root, text="Выберите уровень", font=self.title_font, bg="#f0f0f0", fg="#333333").pack(pady=20)
        
        for i in range(len(levels)):
            if i == 0 or (i - 1) in self.completed_levels:  # Доступ только к пройденным уровням и первому
                tk.Button(self.root, text=f"Уровень {i + 1}", command=lambda lvl=i: self.select_level(lvl),
                          font=self.button_font, bg="#2196F3", fg="white", activebackground="#1e88e5", bd=0, padx=20, pady=10).pack(pady=5)
        
        tk.Button(self.root, text="Назад в меню", command=self.show_main_menu,
                  font=self.button_font, bg="#607D8B", fg="white", activebackground="#546E7A", bd=0, padx=20, pady=10).pack(pady=10)
        tk.Button(self.root, text="Выйти", command=self.quit_game,
                  font=self.button_font, bg="#f44336", fg="white", activebackground="#e53935", bd=0, padx=20, pady=10).pack(pady=10)
    
    def select_level(self, level_index):
        self.level_index = level_index
        self.guessed_words = []  # Сбрасываем список отгаданных слов
        self.show_level()
    
    def show_level(self):
        self.clear_window()
        level = levels[self.level_index]
        self.current_words = level["words"]
        
        tk.Label(self.root, text=f"Уровень {self.level_index + 1}", font=self.title_font, bg="#f0f0f0", fg="#333333").pack(pady=20)
        tk.Label(self.root, text="Составьте слово из предложенных морфем:", font=self.label_font, bg="#f0f0f0", fg="#333333").pack(pady=10)
        
        # Счетчик слов
        self.words_left = len(self.current_words) - len(self.guessed_words)
        self.words_left_label = tk.Label(self.root, text=f"Слов осталось: {self.words_left}", font=self.label_font, bg="#f0f0f0", fg="#333333")
        self.words_left_label.pack(pady=10)
        
        # Поле для отображения отгаданных слов
        self.guessed_words_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.guessed_words_frame.pack(pady=10)
        tk.Label(self.guessed_words_frame, text="Отгаданные слова:", font=self.label_font, bg="#f0f0f0", fg="#333333").pack()
        self.guessed_words_label = tk.Label(self.guessed_words_frame, text=", ".join(self.guessed_words), font=self.label_font, bg="#f0f0f0", fg="#333333")
        self.guessed_words_label.pack()
        
        # Поле для составления слова
        self.answer_frame = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        self.answer_frame.pack(pady=10, ipadx=10, ipady=10)
        
        # Поле для морфем
        self.morpheme_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.morpheme_frame.pack(pady=20)
        
        # Добавляем морфемы в виде кнопок
        self.morphemes = level["morphemes"] + [level["root"]]
        
        for morpheme in self.morphemes:
            # Кнопка с корнем будет синей, остальные — оранжевыми
            if morpheme == level["root"]:
                button_color = "#2196F3"  # Синий цвет для корня
            else:
                button_color = "#FF9800"  # Оранжевый цвет для остальных морфем
            
            button = tk.Button(self.morpheme_frame, text=morpheme, font=self.button_font, bg=button_color, fg="white", activebackground="#FB8C00", bd=0, padx=10, pady=5,
                              command=lambda m=morpheme: self.add_morpheme_to_answer(m))
            button.pack(side="left", padx=5, pady=5)
        
        # Кнопка проверки
        tk.Button(self.root, text="Проверить", command=self.check_answer,
                  font=self.button_font, bg="#4CAF50", fg="white", activebackground="#45a049", bd=0, padx=20, pady=10).pack(pady=10)
        tk.Button(self.root, text="Очистить поле", command=self.clear_answer_frame,
                  font=self.button_font, bg="#607D8B", fg="white", activebackground="#546E7A", bd=0, padx=20, pady=10).pack(pady=10)
        # Кнопка "Очистить последний введенный слог"
        tk.Button(self.root, text="Очистить последний слог", command=self.clear_last_morpheme,
                  font=self.button_font, bg="#FF5722", fg="white", activebackground="#E64A19", bd=0, padx=20, pady=10).pack(pady=10)
        tk.Button(self.root, text="Назад к выбору уровня", command=self.show_level_selection,
                  font=self.button_font, bg="#2196F3", fg="white", activebackground="#1e88e5", bd=0, padx=20, pady=10).pack(pady=10)
        tk.Button(self.root, text="Выйти", command=self.quit_game,
                  font=self.button_font, bg="#f44336", fg="white", activebackground="#e53935", bd=0, padx=20, pady=10).pack(pady=10)
    
    def add_morpheme_to_answer(self, morpheme):
        # Добавляем морфему в поле ответа
        label = tk.Label(self.answer_frame, text=morpheme, font=self.label_font, bg="#E0E0E0", fg="#333333", bd=2, relief="raised", padx=5, pady=5)
        label.pack(side="left", padx=5, pady=5)
    
    def clear_answer_frame(self):
        # Очищаем поле ввода
        for widget in self.answer_frame.winfo_children():
            widget.destroy()
    
    def clear_last_morpheme(self):
        # Удаляем последнюю добавленную морфему
        children = self.answer_frame.winfo_children()
        if children:
            children[-1].destroy()
    
    def check_answer(self):
        answer = "".join([child["text"] for child in self.answer_frame.winfo_children()])
        if answer in self.current_words and answer not in self.guessed_words:
            self.guessed_words.append(answer)
            self.guessed_words_label.config(text=", ".join(self.guessed_words))
            messagebox.showinfo("Правильно!", f"Вы отгадали слово: {answer}")
            self.clear_answer_frame()  # Очищаем поле ввода
            
            # Обновляем счетчик слов
            self.words_left = len(self.current_words) - len(self.guessed_words)
            self.words_left_label.config(text=f"Слов осталось: {self.words_left}")
            
            # Проверяем, все ли слова отгаданы
            if len(self.guessed_words) == len(self.current_words):
                if self.level_index not in self.completed_levels:
                    self.completed_levels.append(self.level_index)
                    save_progress({"level_index": self.level_index, "completed_levels": self.completed_levels})
                messagebox.showinfo("Уровень пройден!", "Вы отгадали все слова! Переход к следующему уровню.")
                self.level_index += 1
                if self.level_index < len(levels):
                    self.select_level(self.level_index)
                else:
                    messagebox.showinfo("Поздравляем!", "Вы прошли все уровни!")
                    self.show_main_menu()
        else:
            messagebox.showerror("Ошибка", "Неправильно! Попробуйте еще раз.")
    
    def quit_game(self):
        save_progress({"level_index": self.level_index, "completed_levels": self.completed_levels})
        self.root.quit()
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = WordGame(root)
    root.mainloop()