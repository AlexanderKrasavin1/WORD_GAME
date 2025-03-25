import json
import tkinter as tk
from tkinter import ttk, messagebox, font

SAVE_FILE = "progress.json"

class WordGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Словообразование PRO")
        self.root.geometry("1100x800")
        self.root.configure(bg="#f0f0f0")
        
        # Загрузка данных из JSON
        with open('levels.json', 'r', encoding='utf-8') as f:
            self.levels = json.load(f)
        
        with open('morpheme_explanations.json', 'r', encoding='utf-8') as f:
            self.morpheme_explanations = json.load(f)

        self.title_font = font.Font(family="Helvetica", size=18, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=12)
        self.label_font = font.Font(family="Helvetica", size=12)
        
        self.progress = self.load_progress()
        self.current_root = 0
        self.sub_type = 'prefix'
        self.current_words = []
        self.guessed_words = []
        
        self.notebook = None
        self.show_main_menu()

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
        messagebox.showinfo("Сброс", "Прогресс сброшен!")
        self.show_main_menu()

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
                     bg="#4CAF50", fg="white", command=cmd).pack(pady=5, padx=20)

    def show_root_selection(self):
        self.clear_window()
        tk.Label(self.root, text="Выберите корень", 
                 font=self.title_font, bg="#f0f0f0").pack(pady=20)
        
        for i, level in enumerate(self.levels):
            frame = tk.Frame(self.root, bg="#f0f0f0")
            frame.pack(pady=5)
            
            tk.Button(frame, text=level['root'], font=self.button_font,
                      command=lambda idx=i: self.prepare_game_screen(idx),
                      bg="#2196F3", fg="white").pack(side="left")
            
            total = self.get_total_words(i)
            guessed = len(self.progress['completed'].get(str(i), []))
            tk.Label(frame, text=f"Угадано: {guessed}/{total}",
                     font=self.label_font, bg="#f0f0f0").pack(side="left", padx=10)
        
        self.add_back_button(self.show_main_menu)

    def prepare_game_screen(self, root_idx):
        self.current_root = root_idx
        self.clear_window()
        self.create_notebook()
        self.show_game_screen()

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        
        tabs = [
            ('Приставочное', 'prefix'),
            ('Суффиксальное', 'suffix'),
            ('Смешанное', 'mixed')
        ]
        
        for text, stype in tabs:
            frame = tk.Frame(self.notebook, bg="#f0f0f0")
            self.notebook.add(frame, text=text)
        
        self.notebook.pack(fill="both", expand=True)
        self.notebook.bind("<<NotebookTabChanged>>", self.tab_changed)
        self.update_tab_content()

    def tab_changed(self, event):
        self.sub_type = ['prefix', 'suffix', 'mixed'][self.notebook.index("current")]
        self.update_tab_content()

    def update_tab_content(self):
        level = self.levels[self.current_root]
        
        self.current_words = []
        if self.sub_type == 'prefix':
            for key in level:
                if key.startswith('word-prefixes'):
                    self.current_words.extend(level[key])
        elif self.sub_type == 'suffix':
            for key in level:
                if key.startswith('word-suffixes'):
                    self.current_words.extend(level[key])
        else:
            for key in level:
                if key.startswith('word-'):
                    self.current_words.extend(level[key])
        
        self.guessed_words = self.progress['completed'].get(str(self.current_root), [])
        self.show_game_screen()

    def show_game_screen(self):
        level = self.levels[self.current_root]
        
        tab = self.notebook.nametowidget(self.notebook.select())
        for widget in tab.winfo_children():
            widget.destroy()
        
        main_frame = tk.Frame(tab, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        left_frame = tk.Frame(main_frame, bg="#f0f0f0")
        left_frame.pack(side="left", fill="both", expand=True)
        
        header_text = f"Корень: {level['root']}"
        tk.Label(left_frame, text=header_text, 
                font=self.label_font, bg="#f0f0f0").pack(pady=5)
        
        total = self.get_total_words(self.current_root)
        guessed = len(self.guessed_words)
        self.counter_label = tk.Label(left_frame, 
            text=f"Угадано слов: {guessed}/{total}",
            font=self.label_font, bg="#f0f0f0")
        self.counter_label.pack()
        
        self.answer_frame = tk.Frame(left_frame, bg="white", bd=2, relief="groove")
        self.answer_frame.pack(pady=10, ipadx=10, ipady=10, fill="x")
        
        self.morpheme_frame = tk.Frame(left_frame, bg="#f0f0f0")
        self.morpheme_frame.pack(pady=10)
        
        for morph in level['prefixes']:
            self.create_morpheme_button(morph, "#2196F3")
        
        self.create_morpheme_button(level['root'], "#9C27B0")
        
        for morph in level['suffixes']:
            self.create_morpheme_button(morph, "#FF9800")
        
        right_frame = tk.Frame(main_frame, bg="#f0f0f0")
        right_frame.pack(side="right", fill="y", padx=20)
        
        guessed_frame = tk.LabelFrame(right_frame, 
                                    text="Отгаданные слова",
                                    font=self.label_font,
                                    bg="#f0f0f0")
        guessed_frame.pack(pady=10)
        
        categories = {}
        for key in level:
            if key.startswith('word-'):
                category = key.split('-')[-1]
                if category not in categories:
                    categories[category] = []
                categories[category].extend(level[key])
        
        category_names = {
            'nouns': 'Существительные',
            'adjectives': 'Прилагательные',
            'verbs': 'Глаголы',
            'adverbs': 'Наречия'
        }
        
        for category in ['nouns', 'adjectives', 'verbs', 'adverbs']:
            if category not in categories:
                continue
                
            frame = tk.Frame(guessed_frame, bg="#f0f0f0")
            frame.pack(side="left", padx=10, pady=5, fill="y")
            
            tk.Label(frame, text=category_names[category], 
                    font=self.label_font, bg="#f0f0f0").pack()
            
            guessed_words = [w for w in self.guessed_words if w in categories[category]]
            for word in guessed_words:
                lbl = tk.Label(frame, text=word, 
                              font=self.label_font, bg="#E0E0E0")
                lbl.pack(pady=2)
                self.setup_tooltip(lbl, word)
        
        control_frame = tk.Frame(left_frame, bg="#f0f0f0")
        control_frame.pack(pady=20)
        
        controls = [
            ("Проверить", "#4CAF50", self.check_answer),
            ("Очистить поле", "#607D8B", self.clear_answer),
            ("Удалить последнюю", "#FF5722", self.remove_last_morpheme),
            ("Назад", "#9E9E9E", lambda: self.show_root_selection())
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
        level = self.levels[self.current_root]
        opposite_type = 'suffix' if self.sub_type == 'prefix' else 'prefix'
        opposite_words = []
        
        for key in level:
            if key.startswith(f'word-{opposite_type}'):
                opposite_words.extend(level[key])

        if answer in self.current_words:
            if answer not in self.guessed_words:
                self.guessed_words.append(answer)
                self.progress['completed'][str(self.current_root)] = self.guessed_words
                self.save_progress()
                
                total = self.get_total_words(self.current_root)
                self.counter_label.config(text=f"Угадано слов: {len(self.guessed_words)}/{total}")
                
                self.clear_answer()
                self.show_game_screen()
                
                if len(self.guessed_words) == total:
                    messagebox.showinfo("Успех", "Все слова для этого корня отгаданы!")
                    self.show_root_selection()
            else:
                messagebox.showerror("Ошибка", "Это слово уже отгадано!")
        elif answer in opposite_words:
            messagebox.showerror("Ошибка", "Слово существует, но образуется по-другому!")
        else:
            messagebox.showerror("Ошибка", "Такого слова не существует!")

    def setup_tooltip(self, widget, morph):
        def show_tip(_):
            try:
                explanations = self.morpheme_explanations[self.current_root]
                text = explanations.get(morph, "Пояснение отсутствует")
                
                tip = tk.Toplevel(self.root)
                tip.wm_overrideredirect(True)
                tip.geometry(f"+{self.root.winfo_pointerx()+15}+{self.root.winfo_pointery()+15}")
                tk.Label(tip, text=text, bg="#FFF9C4", font=self.label_font, 
                        padx=5, pady=3, justify="left").pack()
                self.current_tooltip = tip
            
            except Exception as e:
                print(f"Ошибка в подсказке: {str(e)}")
        
        def hide_tip(_):
            if hasattr(self, 'current_tooltip'):
                self.current_tooltip.destroy()
        
        widget.bind("<Enter>", show_tip)
        widget.bind("<Leave>", hide_tip)

    def get_total_words(self, root_idx):
        total = 0
        for key in self.levels[root_idx]:
            if key.startswith('word-'):
                total += len(self.levels[root_idx][key])
        return total

    def clear_answer(self):
        for widget in self.answer_frame.winfo_children():
            widget.destroy()

    def remove_last_morpheme(self):
        children = self.answer_frame.winfo_children()
        if children:
            children[-1].destroy()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_completed(self):
        self.clear_window()
        tk.Label(self.root, text="Пройденные уровни", 
                 font=self.title_font, bg="#f0f0f0").pack(pady=20)
        
        if not self.progress['completed']:
            tk.Label(self.root, text="Пока нет пройденных уровней", 
                     font=self.label_font, bg="#f0f0f0").pack()
        else:
            for key in self.progress['completed']:
                level = self.levels[int(key)]
                total = self.get_total_words(int(key))
                guessed = len(self.progress['completed'][key])
                tk.Label(self.root, 
                         text=f"{level['root']}: {guessed}/{total} слов",
                         font=self.label_font, bg="#f0f0f0").pack(pady=5)
        
        self.add_back_button(self.show_main_menu)

    def add_back_button(self, command):
        tk.Button(self.root, text="Назад", font=self.button_font,
                 bg="#9E9E9E", fg="white", command=command).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    game = WordGame(root)
    root.mainloop()