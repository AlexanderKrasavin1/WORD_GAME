import json
import tkinter as tk
from tkinter import messagebox, font

# Конфигурационные файлы
LEVELS_FILE = [
    {
        "root": "ход",
        "prefixes": ["при", "под", "вы"],
        "suffixes": ["ок", "ить"],
        "words_prefixes": ["приход", "подход", "выход"],
        "words_suffixes": ["ходок", "ходить"]
    },
    {
        "root": "бег",
        "prefixes": ["за", "про"],
        "suffixes": ["ун", "ств", "о"],
        "words_prefixes": ["забег", "пробег"],
        "words_suffixes": ["бегун", "бегство"]
    }
]
SAVE_FILE = "progress.json"

# Пояснения для морфем (необходимо дополнить)
MORPHEME_EXPLANATIONS = {
    'при': 'Приставка со значением приближения',
    'под': 'Приставка со значением направления',
    'вы': 'Приставка со значением движения изнутри',
    'ок': 'Суффикс для образования существительных',
    'ить': 'Глагольный суффикс',
    'ун': 'Суффикс для обозначения деятеля',
    'ств': 'Суффикс для образования абстрактных существительных'
}

class WordGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Словообразование")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Загрузка данных
       
        self.levels = LEVELS_FILE
            
        # Инициализация шрифтов
        self.title_font = font.Font(family="Helvetica", size=18, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=12)
        self.label_font = font.Font(family="Helvetica", size=12)
        
        # Состояние игры
        self.progress = self.load_progress()
        self.current_root = 0
        self.sub_type = ''
        self.current_words = []
        self.guessed_words = []
        
        self.show_main_menu()

    # region Система прогресса
    def load_progress(self):
        try:
            with open(SAVE_FILE, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {"completed": {}}
    
    def save_progress(self):
        with open(SAVE_FILE, "w") as file:
            json.dump(self.progress, file, indent=2)
    
    def reset_progress(self):
        self.progress = {"completed": {}}
        self.save_progress()
    # endregion

    # region Навигация
    def show_main_menu(self):
        self.clear_window()
        tk.Label(self.root, text="Главное меню", 
                 font=self.title_font, bg="#f0f0f0").pack(pady=20)
        
        buttons = [
            ("Играть", self.show_root_selection),
            ("Пройденные уровни", self.show_completed),
            ("Сбросить прогресс", self.reset_progress),
            ("Выйти", self.root.quit)
        ]
        
        for text, cmd in buttons:
            tk.Button(self.root, text=text, font=self.button_font,
                      bg="#4CAF50", fg="white", activebackground="#45a049",
                      command=cmd).pack(pady=5, padx=20, ipadx=10, ipady=5)

    def show_root_selection(self):
        self.clear_window()
        tk.Label(self.root, text="Выберите корень", 
                 font=self.title_font, bg="#f0f0f0").pack(pady=20)
        
        for i, level in enumerate(self.levels):
            tk.Button(self.root, text=level['root'], font=self.button_font,
                      command=lambda idx=i: self.show_sublevel_select(idx),
                      bg="#2196F3", fg="white", activebackground="#1e88e5"
                      ).pack(pady=5)
        
        self.add_back_button(self.show_main_menu)

    def show_sublevel_select(self, root_idx):
        self.clear_window()
        self.current_root = root_idx
        level = self.levels[root_idx]
        
        tk.Label(self.root, text=f"Корень: {level['root']}", 
                 font=self.title_font, bg="#f0f0f0").pack(pady=20)
        
        sublevels = [
            ("Приставочное образование", 'prefix'),
            ("Суффиксальное образование", 'suffix')
        ]
        
        for text, stype in sublevels:
            tk.Button(self.root, text=text, font=self.button_font,
                      command=lambda t=stype: self.start_level(t),
                      bg="#FF9800", fg="white", activebackground="#FB8C00"
                      ).pack(pady=10)
        
        self.add_back_button(self.show_root_selection)
    # endregion

    # region Игровой процесс
    def start_level(self, sub_type):
        self.sub_type = sub_type
        level = self.levels[self.current_root]
        self.current_words = level[f"words_{sub_type}es"]
        self.guessed_words = []
        self.show_game_screen()

    def show_game_screen(self):
        self.clear_window()
        level = self.levels[self.current_root]
        
        # Заголовок
        type_name = "Приставочное" if self.sub_type == 'prefix' else "Суффиксальное"
        header_text = f"{type_name} образование: {level['root']}"
        tk.Label(self.root, text=header_text, 
                 font=self.label_font, bg="#f0f0f0").pack(pady=5)
        
        # Счетчик
        self.counter_label = tk.Label(self.root, 
            text=f"Осталось слов: {len(self.current_words) - len(self.guessed_words)}",
            font=self.label_font, bg="#f0f0f0")
        self.counter_label.pack()
        
        # Поле ответа
        self.answer_frame = tk.Frame(self.root, bg="white", bd=2, relief="groove")
        self.answer_frame.pack(pady=10, ipadx=10, ipady=10)
        
        # Морфемы
        self.morpheme_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.morpheme_frame.pack(pady=10)
        
        root_morpheme = level['root']
        affixes = level[f"{self.sub_type}es"]
        
        # Кнопка корня
        self.create_morpheme_button(root_morpheme, "#2196F3")
        
        # Кнопки аффиксов
        for morph in affixes:
            self.create_morpheme_button(morph, "#FF9800")
        
        # Панель управления
        control_frame = tk.Frame(self.root, bg="#f0f0f0")
        control_frame.pack(pady=20)
        
        controls = [
            ("Проверить", "#4CAF50", self.check_answer),
            ("Очистить поле", "#607D8B", self.clear_answer),
            ("Удалить последнюю", "#FF5722", self.remove_last_morpheme),
            ("Назад", "#9E9E9E", lambda: self.show_sublevel_select(self.current_root))
        ]
        
        for text, color, cmd in controls:
            tk.Button(control_frame, text=text, font=self.button_font,
                      bg=color, fg="white", command=cmd).pack(side="left", padx=5)

    def create_morpheme_button(self, morph, color):
        btn = tk.Button(self.morpheme_frame, text=morph, font=self.button_font,
                       bg=color, fg="white", command=lambda m=morph: self.add_morpheme(m))
        btn.pack(side="left", padx=5, pady=5)
        self.setup_tooltip(btn, morph)

    def add_morpheme(self, morph):
        label = tk.Label(self.answer_frame, text=morph, font=self.label_font,
                        bg="#E0E0E0", padx=5, pady=2)
        label.pack(side="left", padx=2)

    def check_answer(self):
        answer = "".join([child['text'] for child in self.answer_frame.winfo_children()])
        
        if answer in self.current_words and answer not in self.guessed_words:
            self.guessed_words.append(answer)
            self.clear_answer()
            
            remaining = len(self.current_words) - len(self.guessed_words)
            self.counter_label.config(text=f"Осталось слов: {remaining}")
            
            if remaining == 0:
                self.mark_level_completed()
                messagebox.showinfo("Успех", "Все слова отгаданы! Уровень пройден!")
                self.show_sublevel_select(self.current_root)
        else:
            messagebox.showerror("Ошибка", "Неверное слово или уже отгадано")
    # endregion

    # region Вспомогательные методы
    def setup_tooltip(self, widget, morph):
        def show_tip(_):
            text = MORPHEME_EXPLANATIONS.get(morph, "Пояснение отсутствует")
            tip = tk.Toplevel(self.root)
            tip.wm_overrideredirect(True)
            tip.geometry(f"+{self.root.winfo_pointerx()+10}+{self.root.winfo_pointery()+10}")
            tk.Label(tip, text=text, bg="lightyellow", relief="solid", borderwidth=1).pack()
            self.current_tooltip = tip
        
        def hide_tip(_):
            if hasattr(self, 'current_tooltip'):
                self.current_tooltip.destroy()
        
        widget.bind("<Enter>", show_tip)
        widget.bind("<Leave>", hide_tip)

    def mark_level_completed(self):
        key = f"{self.current_root}-{self.sub_type}"
        self.progress['completed'][key] = True
        self.save_progress()

    def clear_answer(self):
        for widget in self.answer_frame.winfo_children():
            widget.destroy()

    def remove_last_morpheme(self):
        children = self.answer_frame.winfo_children()
        if children:
            children[-1].destroy()

    def add_back_button(self, command):
        tk.Button(self.root, text="Назад", font=self.button_font,
                 bg="#9E9E9E", fg="white", command=command).pack(pady=20)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_completed(self):
        self.clear_window()
        tk.Label(self.root, text="Пройденные уровни", 
                 font=self.title_font, bg="#f0f0f0").pack(pady=20)
        
        # Отображение пройденных уровней
        for key in self.progress['completed']:
            root_idx, sub_type = key.split('-')
            root = self.levels[int(root_idx)]['root']
            stype = 'Приставочное' if sub_type == 'prefix' else 'Суффиксальное'
            tk.Label(self.root, text=f"{root} ({stype})", 
                    font=self.label_font, bg="#f0f0f0").pack()
        
        self.add_back_button(self.show_main_menu)
    # endregion

if __name__ == "__main__":
    root = tk.Tk()
    game = WordGame(root)
    root.mainloop()