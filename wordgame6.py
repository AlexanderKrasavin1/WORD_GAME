import json
import tkinter as tk
from tkinter import messagebox, font, ttk
import random
from translate import Translator

SAVE_FILE = "progress.json"

class WordGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Словообразование PRO")
        
        # Загрузка прогресса и настроек
        self.progress = self.load_progress()
        self.settings = self.progress['settings']
        
        # Применение настроек
        self.apply_settings()
        
        # Инициализация данных игры
        self.load_data_files()
        
        # Настройка шрифтов
        self.title_font = font.Font(family="Helvetica", size=18, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=12)
        self.label_font = font.Font(family="Helvetica", size=12)
        
        # Игровые переменные
        self.current_root = 0
        self.sub_type = ''
        self.current_words = []
        self.guessed_words = []
        self.hints = []
        self.used_hints = set()
        
        self.show_main_menu()

    def load_data_files(self):
        """Загрузка файлов с уровнями и объяснениями"""
        with open('levels.json', 'r', encoding='utf-8') as f:
            self.levels = json.load(f)
        with open('morpheme_explanations.json', 'r', encoding='utf-8') as f:
            self.morpheme_explanations = json.load(f)

    def load_progress(self):
        """Загрузка прогресса из файла"""
        try:
            with open(SAVE_FILE, "r") as file:
                data = json.load(file)
                return self.upgrade_progress_format(data)
        except (FileNotFoundError, json.JSONDecodeError):
            return self.get_default_progress()

    def upgrade_progress_format(self, data):
        """Конвертация старых версий файла прогресса"""
        defaults = self.get_default_progress()
        for key in defaults:
            if key not in data:
                data[key] = defaults[key]
        data['settings'] = {**defaults['settings'], **data.get('settings', {})}
        return data

    def get_default_progress(self):
        """Создание прогресса по умолчанию"""
        return {
            "completed": {},
            "score": 0,
            "hints": {},
            "achievements": {
                'no_hints': False,
                'word_master': False,
                'economist': False
            },
            "settings": {
                'language': 'Русский',
                'window_size': '1200x800',
                'fullscreen': False
            }
        }

    def save_progress(self):
        """Сохранение прогресса в файл"""
        data = {
            "completed": {str(k): v for k, v in self.progress['completed'].items()},
            "score": self.progress['score'],
            "hints": self.progress['hints'],
            "achievements": self.progress['achievements'],
            "settings": self.settings
        }
        with open(SAVE_FILE, "w") as file:
            json.dump(data, file, indent=2)

    def apply_settings(self):
        """Применение настроек интерфейса"""
        if self.settings['fullscreen']:
            self.root.attributes('-fullscreen', True)
        else:
            self.root.attributes('-fullscreen', False)
            self.root.geometry(self.settings['window_size'])
        self.root.update_idletasks()

    def show_main_menu(self):
        """Отображение главного меню"""
        self.clear_window()
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True)
        
        self.create_header(main_frame, "Главное меню")
        
        buttons = [
            ("Играть", self.show_root_selection),
            ("Пройденные уровни", self.show_completed),
            ("Достижения", self.show_achievements),
            ("Настройки", self.show_settings),
            ("Сбросить прогресс", self.reset_progress),
            ("Выйти", self.root.quit)
        ]
        
        for text, cmd in buttons:
            self.create_menu_button(main_frame, text, cmd)

    def create_header(self, parent, text):
        """Создание заголовка"""
        header_frame = tk.Frame(parent, bg="#f0f0f0")
        header_frame.pack(pady=10)
        tk.Label(header_frame, text=text, 
                font=self.title_font, bg="#f0f0f0").pack()
        tk.Label(header_frame, text=f"Очки: {self.progress['score']}", 
                font=self.label_font, bg="#f0f0f0").pack(pady=5)

    def create_menu_button(self, parent, text, command):
        """Создание кнопки меню"""
        tk.Button(parent, text=text, font=self.button_font,
                bg="#4CAF50", fg="white", command=command
                ).pack(pady=5, padx=20, ipadx=10, ipady=5)

    def show_root_selection(self):
        """Выбор корня"""
        self.clear_window()
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True)
        
        self.create_header(main_frame, "Выберите корень")
        
        for i, level in enumerate(self.levels):
            frame = tk.Frame(main_frame, bg="#f0f0f0")
            frame.pack(pady=5)
            
            self.create_level_button(frame, level['root'], i)
            self.create_progress_label(frame, i)
        
        self.add_back_button(self.show_main_menu)

    def create_level_button(self, parent, text, index):
        """Кнопка выбора уровня"""
        tk.Button(parent, text=text, font=self.button_font,
                 command=lambda idx=index: self.show_sublevel_select(idx),
                 bg="#2196F3", fg="white").pack(side="left")

    def create_progress_label(self, parent, index):
        """Отображение прогресса по уровню"""
        total = self.get_total_words(index)
        guessed = len(self.progress['completed'].get(str(index), {}).get('guessed', []))
        tk.Label(parent, text=f"Угадано: {guessed}/{total}",
                font=self.label_font, bg="#f0f0f0").pack(side="left", padx=10)

    def show_sublevel_select(self, root_idx):
        """Выбор типа словообразования"""
        self.current_root = root_idx
        self.clear_window()
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True)
        
        self.create_header(main_frame, f"Корень: {self.levels[root_idx]['root']}")
        
        sublevels = [
            ("Приставочное образование", 'prefix'),
            ("Суффиксальное образование", 'suffix')
        ]
        
        for text, stype in sublevels:
            self.create_sublevel_button(main_frame, text, stype)
        
        self.add_back_button(self.show_root_selection)

    def create_sublevel_button(self, parent, text, stype):
        """Кнопка выбора типа образования"""
        tk.Button(parent, text=text, font=self.button_font,
                 command=lambda t=stype: self.start_level(t),
                 bg="#FF9800", fg="white").pack(pady=10)

    def start_level(self, sub_type):
        """Начало уровня"""
        self.sub_type = sub_type
        level = self.levels[self.current_root]
        self.hints = []
        
        level_key = f"{self.current_root}-{sub_type}"
        self.used_hints = set(self.progress['hints'].get(level_key, []))
        self.guessed_words = self.progress['completed'].get(str(self.current_root), {}).get('guessed', [])
        
        self.current_words = [
            word for key in level 
            if key.startswith(f'word-{sub_type}')
            for word in level[key]
        ]
        
        self.show_game_screen()

    def show_game_screen(self):
        """Игровой экран"""
        self.clear_window()
        level = self.levels[self.current_root]
        
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        left_frame = tk.Frame(main_frame, bg="#f0f0f0")
        left_frame.pack(side="left", fill="both", expand=True)
        
        # Левая панель
        header_frame = tk.Frame(left_frame, bg="#f0f0f0")
        header_frame.pack(pady=5)
        
        type_names = {
            'prefix': 'Приставочное',
            'suffix': 'Суффиксальное'
        }
        tk.Label(header_frame, 
                text=f"{type_names[self.sub_type]} образование: {level['root']}", 
                font=self.label_font, bg="#f0f0f0").pack()
        tk.Label(header_frame, 
                text=f"Очки: {self.progress['score']} | Угадано слов: {len(self.guessed_words)}/{self.get_total_words(self.current_root)}",
                font=self.label_font, bg="#f0f0f0").pack()
        
        self.answer_frame = tk.Frame(left_frame, bg="white", bd=2, relief="groove")
        self.answer_frame.pack(pady=10, ipadx=10, ipady=10, fill="x")
        
        self.morpheme_frame = tk.Frame(left_frame, bg="#f0f0f0")
        self.morpheme_frame.pack(pady=10)
        
        for morph in level['prefixes']:
            self.create_morpheme_button(morph, "#2196F3")
        
        self.create_morpheme_button(level['root'], "#9C27B0")
        
        for morph in level['suffixes']:
            self.create_morpheme_button(morph, "#FF9800")
        
        # Правая панель
        right_frame = tk.Frame(main_frame, bg="#f0f0f0")
        right_frame.pack(side="right", fill="both", padx=20)
        
        # Отгаданные слова
        guessed_frame = tk.LabelFrame(right_frame, 
                                    text="Отгаданные слова",
                                    font=self.label_font,
                                    bg="#f0f0f0")
        guessed_frame.pack(pady=10, fill="both")
        
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
                lbl.bind("<Button-3>", lambda e, w=word: self.show_translation_popup(w))
        
        # Подсказки
        self.hints_frame = tk.LabelFrame(right_frame,
                                       text="Подсказки",
                                       font=self.label_font,
                                       bg="#f0f0f0")
        self.hints_frame.pack(pady=10, fill="both", expand=True)
        self.update_hints_display()
        
        # Управление
        control_frame = tk.Frame(left_frame, bg="#f0f0f0")
        control_frame.pack(pady=20)
        
        controls = [
            ("Проверить", "#4CAF50", self.check_answer),
            ("Очистить поле", "#607D8B", self.clear_answer),
            ("Удалить последнюю", "#FF5722", self.remove_last_morpheme),
            ("Подсказка (30)", "#9C27B0", self.buy_hint),
            ("Назад", "#9E9E9E", lambda: self.show_sublevel_select(self.current_root))
        ]
        
        for text, color, cmd in controls:
            tk.Button(control_frame, text=text, font=self.button_font,
                     bg=color, fg="white", command=cmd).pack(side="left", padx=5)

    def create_morpheme_button(self, morph, color):
        """Создание кнопки морфемы"""
        btn = tk.Button(self.morpheme_frame, text=morph, font=self.button_font,
                      bg=color, fg="white", command=lambda m=morph: self.add_morpheme(m))
        btn.pack(side="left", padx=5, pady=5)
        self.setup_tooltip(btn, morph)

    def add_morpheme(self, morph):
        """Добавление морфемы в поле ответа"""
        label = tk.Label(self.answer_frame, text=morph, font=self.label_font,
                        bg="#E0E0E0", padx=5, pady=2)
        label.pack(side="left", padx=2)

    def check_answer(self):
        """Проверка ответа"""
        answer = "".join([child['text'] for child in self.answer_frame.winfo_children()])
        level = self.levels[self.current_root]
        opposite_type = 'suffix' if self.sub_type == 'prefix' else 'prefix'
        opposite_words = []
        
        for key in level:
            if key.startswith(f'word-{opposite_type}'):
                opposite_words.extend(level[key])

        if answer in self.current_words:
            self.handle_correct_answer(answer)
        elif answer in opposite_words:
            messagebox.showerror("Ошибка", "Слово существует, но образуется по-другому!")
        else:
            messagebox.showerror("Ошибка", "Такого слова не существует!")

    def handle_correct_answer(self, answer):
        """Обработка правильного ответа"""
        if answer not in self.guessed_words:
            self.progress['score'] += 10
            self.guessed_words.append(answer)
            
            if str(self.current_root) not in self.progress['completed']:
                self.progress['completed'][str(self.current_root)] = {
                    'guessed': [],
                    'hints': []
                }
            self.progress['completed'][str(self.current_root)]['guessed'] = self.guessed_words
            self.save_progress()
            
            if len(self.guessed_words) == self.get_total_words(self.current_root):
                self.progress['score'] += 50
                messagebox.showinfo("Уровень пройден!", "Все слова отгаданы! +50 бонусных очков")
                self.save_progress()
            
            messagebox.showinfo("Правильно!", f"+10 очков! Текущий счёт: {self.progress['score']}")
            self.clear_answer()
            self.check_achievements()
            self.show_game_screen()
            
            if len(self.guessed_words) == self.get_total_words(self.current_root):
                self.show_root_selection()
        else:
            messagebox.showerror("Ошибка", "Это слово уже отгадано!")

    def setup_tooltip(self, widget, morph):
        """Создание всплывающей подсказки с переводом"""
        def show_tip(event):
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
        
        def hide_tip(event):
            if hasattr(self, 'current_tooltip'):
                self.current_tooltip.destroy()
        
        def translate_handler(event):
            translated = self.translate_word(morph)
            translate_win = tk.Toplevel(self.root)
            translate_win.wm_overrideredirect(True)
            translate_win.geometry(f"+{event.x_root+20}+{event.y_root+20}")
            tk.Label(translate_win, 
                    text=f"{morph} → {translated}",
                    bg="#E1F5FE", 
                    font=self.label_font,
                    padx=5, 
                    pady=2).pack()
            translate_win.bind("<Button>", lambda e: translate_win.destroy())
        
        widget.bind("<Enter>", show_tip)
        widget.bind("<Leave>", hide_tip)
        widget.bind("<Button-3>", translate_handler)

    def get_total_words(self, root_idx):
        """Получение общего количества слов для уровня"""
        total = 0
        for key in self.levels[root_idx]:
            if key.startswith('word-'):
                total += len(self.levels[root_idx][key])
        return total

    def clear_answer(self):
        """Очистка поля ответа"""
        for widget in self.answer_frame.winfo_children():
            widget.destroy()

    def remove_last_morpheme(self):
        """Удаление последней морфемы"""
        children = self.answer_frame.winfo_children()
        if children:
            children[-1].destroy()

    def clear_window(self):
        """Очистка окна"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_completed(self):
        """Показать пройденные уровни"""
        self.clear_window()
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True)
        
        self.create_header(main_frame, "Пройденные уровни")
        
        if not self.progress['completed']:
            tk.Label(main_frame, text="Пока нет пройденных уровней", 
                     font=self.label_font, bg="#f0f0f0").pack()
        else:
            for key in self.progress['completed']:
                level = self.levels[int(key)]
                total = self.get_total_words(int(key))
                guessed = len(self.progress['completed'][key].get('guessed', []))
                tk.Label(main_frame, 
                         text=f"{level['root']}: {guessed}/{total} слов",
                         font=self.label_font, bg="#f0f0f0").pack(pady=5)
        
        self.add_back_button(self.show_main_menu)

    def add_back_button(self, command):
        """Добавление кнопки 'Назад'"""
        tk.Button(self.root, text="Назад", font=self.button_font,
                 bg="#9E9E9E", fg="white", command=command).pack(pady=20)

    def buy_hint(self):
        """Покупка подсказки"""
        if self.progress['score'] < 30:
            messagebox.showerror("Ошибка", "Недостаточно очков для подсказки!")
            return
        
        level = self.levels[self.current_root]
        all_words = []
        for key in level:
            if key.startswith(f'word-{self.sub_type}'):
                all_words.extend(level[key])
        
        available_words = [word for word in all_words 
                          if word not in self.guessed_words 
                          and word not in self.used_hints]
        
        if not available_words:
            messagebox.showinfo("Подсказка", "Нет доступных слов для подсказки!")
            return
            
        selected_word = random.choice(available_words)
        self.used_hints.add(selected_word)
        explanation = self.get_word_explanation(selected_word)
        root_word = level['root']
        
        level_key = f"{self.current_root}-{self.sub_type}"
        self.progress['hints'][level_key] = list(self.used_hints)
        
        if "пример:" in explanation:
            example_part = explanation.split("пример:")[1]
            masked_example = example_part.replace(root_word, '*' * len(root_word))
            formatted_hint = explanation.split("пример:")[0] + "пример:" + masked_example
        else:
            formatted_hint = explanation
        
        self.progress['score'] -= 30
        self.hints.append(formatted_hint)
        self.save_progress()
        self.check_achievements()
        self.update_hints_display()
        self.show_game_screen()

    def get_word_explanation(self, word):
        """Получение объяснения для слова"""
        explanations = next(item for item in self.morpheme_explanations 
                          if item['root'] == self.levels[self.current_root]['root'])
        return explanations.get(word, "Пояснение отсутствует")

    def update_hints_display(self):
        """Обновление отображения подсказок"""
        for widget in self.hints_frame.winfo_children():
            widget.destroy()
        
        for hint in self.hints:
            lbl = tk.Label(self.hints_frame, text=hint,
                          font=self.label_font, bg="#FFF9C4",
                          wraplength=250, justify="left")
            lbl.pack(pady=5, padx=5, anchor="w")

    def check_achievements(self):
        """Проверка достижений"""
        total_guessed = sum(len(l['guessed']) for l in self.progress['completed'].values())
        
        achievements = [
            ('no_hints', total_guessed >= 10, "Чистая победа!\nОтгадано 10 слов без подсказок"),
            ('word_master', total_guessed >= 50, "Мастер словообразования!\nОтгадано 50 слов"),
            ('economist', self.progress['score'] >= 500, "Экономист!\nНакоплено 500 очков")
        ]
        
        for name, condition, message in achievements:
            if condition and not self.progress['achievements'][name]:
                self.progress['achievements'][name] = True
                messagebox.showinfo("Достижение!", message)
                self.save_progress()

    def reset_progress(self):
        """Сброс прогресса"""
        self.progress = self.get_default_progress()
        self.save_progress()
        messagebox.showinfo("Сброс", "Прогресс и очки сброшены!")
        self.show_main_menu()
    
    def translate_word(self, word):
        """Перевод слова с русского на выбранный язык"""
        try:
            translator = Translator(from_lang='ru', to_lang=self.settings['target_lang'])
            return translator.translate(word)
        except Exception as e:
            print(f"Ошибка перевода: {str(e)}")
            return "Ошибка перевода"

    def show_achievements(self):
        """Показать достижения"""
        self.clear_window()
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True)
        
        self.create_header(main_frame, "Достижения")
        
        achievements = [
            {
                'title': "Чистая победа",
                'description': "Отгадать 10 слов без использования подсказок",
                'status': self.progress['achievements']['no_hints']
            },
            {
                'title': "Мастер словообразования",
                'description': "Отгадать 50 слов",
                'status': self.progress['achievements']['word_master']
            },
            {
                'title': "Экономист",
                'description': "Накопить 500 очков",
                'status': self.progress['achievements']['economist']
            }
        ]
        
        for achievement in achievements:
            frame = tk.Frame(main_frame, bg="#E0E0E0", padx=10, pady=5)
            frame.pack(pady=5, fill="x", padx=50)
            
            color = "#4CAF50" if achievement['status'] else "#757575"
            tk.Label(frame, text="✓" if achievement['status'] else "✗", 
                     font=self.title_font, bg=color, fg="white", width=3).pack(side="left")
            
            text_frame = tk.Frame(frame, bg="#E0E0E0")
            text_frame.pack(side="left", padx=10)
            
            tk.Label(text_frame, text=achievement['title'], 
                    font=self.button_font, bg="#E0E0E0", anchor="w").pack(anchor="w")
            tk.Label(text_frame, text=achievement['description'], 
                    font=self.label_font, bg="#E0E0E0", fg="#424242").pack(anchor="w")
        
        self.add_back_button(self.show_main_menu)
    

    def show_settings(self):
        """Настройки игры с выбором языка перевода"""
        self.clear_window()
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=50, pady=30)
        
        self.create_header(main_frame, "Настройки")
        
        # Инициализация переменных
        self.lang_var = tk.StringVar(value=self.settings.get('language', 'Русский'))
        self.target_lang_var = tk.StringVar(value=self.settings.get('target_lang', 'en'))
        self.size_var = tk.StringVar(value=self.settings.get('window_size', '1200x800'))
        self.fullscreen_var = tk.BooleanVar(value=self.settings.get('fullscreen', False))
        
        # Блок выбора языка интерфейса
        interface_lang_frame = tk.Frame(main_frame, bg="#f0f0f0")
        interface_lang_frame.pack(fill="x", pady=10)
        
        tk.Label(interface_lang_frame, 
                text="Язык интерфейса:", 
                font=self.label_font, 
                bg="#f0f0f0").pack(side="left")
        
        ttk.Combobox(
            interface_lang_frame,
            textvariable=self.lang_var,
            values=['Русский', 'English'],
            state="readonly",
            width=15
        ).pack(side="left", padx=10)
        
        # Блок выбора языка перевода
        translation_lang_frame = tk.Frame(main_frame, bg="#f0f0f0")
        translation_lang_frame.pack(fill="x", pady=10)
        
        tk.Label(translation_lang_frame, 
                text="Язык перевода:", 
                font=self.label_font, 
                bg="#f0f0f0").pack(side="left")
        
        ttk.Combobox(
            translation_lang_frame,
            textvariable=self.target_lang_var,
            values=['en', 'es', 'de', 'fr', 'it', 'zh', 'ja'],
            state="readonly",
            width=15
        ).pack(side="left", padx=10)
        
        # Блок размера окна
        size_frame = tk.Frame(main_frame, bg="#f0f0f0")
        size_frame.pack(fill="x", pady=10)
        
        tk.Label(size_frame, 
                text="Размер окна:", 
                font=self.label_font, 
                bg="#f0f0f0").pack(side="left")
        
        ttk.Combobox(
            size_frame,
            textvariable=self.size_var,
            values=['800x600', '1200x800', '1600x900'],
            state="readonly",
            width=15
        ).pack(side="left", padx=10)
        
        # Блок полноэкранного режима
        fullscreen_frame = tk.Frame(main_frame, bg="#f0f0f0")
        fullscreen_frame.pack(fill="x", pady=10)
        
        tk.Checkbutton(
            fullscreen_frame,
            text="Полноэкранный режим",
            variable=self.fullscreen_var,
            font=self.label_font,
            bg="#f0f0f0"
        ).pack(side="left")
        
        # Кнопки управления
        btn_frame = tk.Frame(main_frame, bg="#f0f0f0")
        btn_frame.pack(pady=20)
        
        tk.Button(
            btn_frame,
            text="Применить",
            font=self.button_font,
            bg="#4CAF50",
            fg="white",
            command=self.save_settings
        ).pack(side="left", padx=10)
        
        tk.Button(
            btn_frame,
            text="Отмена",
            font=self.button_font,
            bg="#F44336",
            fg="white",
            command=self.show_main_menu
        ).pack(side="left", padx=10)
        
        self.add_back_button(self.show_main_menu)

    def save_settings(self):
        """Сохранение настроек с принудительной проверкой"""
        new_settings = {
            'language': self.lang_var.get(),
            'target_lang': self.target_lang_var.get().lower(),  # нормализация кода
            'window_size': self.size_var.get(),
            'fullscreen': self.fullscreen_var.get()
        }
        
        # Принудительная валидация языка перевода
        valid_langs = ['en', 'es', 'de', 'fr']
        if new_settings['target_lang'] not in valid_langs:
            new_settings['target_lang'] = 'en'
            messagebox.showwarning("Ошибка", "Неверный язык перевода. Установлен английский по умолчанию.")
        
        # Проверка реального перевода
        try:
            test_result = self.translate_word("пример")
            if test_result.lower() in ["пример", "error"]:
                raise Exception("Тестовый перевод не удался")
        except Exception as e:
            messagebox.showerror("Ошибка", 
                f"Проверка переводчика не пройдена: {str(e)}\n"
                "Убедитесь в наличии интернет-соединения")
            return
        
        self.settings.update(new_settings)
        self.save_progress()
        self.apply_settings()
        messagebox.showinfo("Успех", "Настройки сохранены!")
        self.show_main_menu()

    def translate_word(self, word):
        """Перевод слова с русского на выбранный язык"""
        try:
            # Проверка и преобразование кодов языков
            lang_codes = {
                'Русский': 'en',
                'English': 'en',
                'es': 'es',
                'de': 'de',
                'fr': 'fr'
            }
            
            target_lang = self.settings.get('target_lang', 'en')
            target_code = lang_codes.get(target_lang, 'en')
            
            # Для русского интерфейса переводим на выбранный язык
            if self.settings['language'] == 'Русский':
                translator = Translator(from_lang='ru', to_lang=target_code)
            else:
                # Для английского интерфейса переводим на английский
                translator = Translator(from_lang='ru', to_lang='en')
            
            result = translator.translate(word)
            
            # Фикс бага с возвратом исходного слова
            if result.lower() == word.lower():
                return f"{word} (перевод недоступен)"
                
            return result
        except Exception as e:
            print(f"Ошибка перевода: {str(e)}")
            return "Ошибка перевода"

    def show_translation_popup(self, word):
        """Показать всплывающее окно с переводом"""
        translated = self.translate_word(word)
        popup = tk.Toplevel(self.root)
        popup.wm_overrideredirect(True)
        popup.geometry(f"+{self.root.winfo_pointerx()+20}+{self.root.winfo_pointery()+20}")
        tk.Label(popup, 
                text=f"{word} → {translated}",
                bg="#E1F5FE", 
                font=self.label_font,
                padx=5, 
                pady=2).pack()
        popup.bind("<Button>", lambda e: popup.destroy())

if __name__ == "__main__":
    root = tk.Tk()
    game = WordGame(root)
    root.mainloop()