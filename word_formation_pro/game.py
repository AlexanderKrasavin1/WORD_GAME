import json
import tkinter as tk
from tkinter import messagebox, font, ttk
import random
from translate import Translator
from constants import SAVE_FILE
from localization import locales
from data_loader import load_levels, load_explanations

class WordGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Formation PRO")
        
        # Загрузка прогресса и настроек
        self.progress = self.load_progress()
        self.settings = self.progress['settings']
        
        # Система локализации
        self.locales = locales
        self.current_locale = self.settings['language']
        self.locale = self.locales.get(self.current_locale, self.locales['Русский'])
        
        # Применение настроек
        self.apply_settings()
        
        # Инициализация данных игры
        self.levels = load_levels()
        self.morpheme_explanations = load_explanations()
        
        # Настройка шрифтов
        self.setup_fonts()
        
        # Игровые переменные
        self.current_root = 0
        self.sub_type = ''
        self.current_words = []
        self.guessed_words = []
        self.hints = []
        self.used_hints = set()
        self.current_screen = None
        self.translation_frame = None
        
        self.show_main_menu()

    def setup_fonts(self):
        """Настройка шрифтов для разных языков"""
        default_font = 'Helvetica'
        chinese_font = 'Microsoft YaHei' if self.current_locale == '中文' else default_font
        
        self.title_font = font.Font(
            family=chinese_font if self.current_locale == '中文' else default_font, 
            size=18, 
            weight="bold"
        )
        self.button_font = font.Font(
            family=chinese_font if self.current_locale == '中文' else default_font, 
            size=12
        )
        self.label_font = font.Font(
            family=chinese_font if self.current_locale == '中文' else default_font, 
            size=12
        )

    def tr(self, key):
        """Получение перевода по ключу"""
        return self.locale.get(key, key)

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
                'target_lang': 'en',
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
        """Применение настроек с обновлением локализации"""
        self.current_locale = self.settings['language']
        self.locale = self.locales.get(self.current_locale, self.locales['Русский'])
        self.setup_fonts()
        
        if self.settings['fullscreen']:
            self.root.attributes('-fullscreen', True)
        else:
            self.root.attributes('-fullscreen', False)
            self.root.geometry(self.settings['window_size'])
        self.root.update_idletasks()
        
        if hasattr(self, 'current_screen'):
            self.current_screen()

    def show_main_menu(self):
        """Отображение главного меню"""
        self.clear_window()
        self.current_screen = self.show_main_menu
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True)
        
        self.create_header(main_frame, self.tr('main_menu'))
        
        buttons = [
            (self.tr('play'), self.show_root_selection),
            (self.tr('completed_levels'), self.show_completed),
            (self.tr('achievements'), self.show_achievements),
            (self.tr('settings'), self.show_settings),
            (self.tr('reset'), self.reset_progress),
            (self.tr('exit'), self.root.quit)
        ]
        
        for text, cmd in buttons:
            self.create_menu_button(main_frame, text, cmd)

    def create_header(self, parent, text):
        """Создание заголовка"""
        header_frame = tk.Frame(parent, bg="#f0f0f0")
        header_frame.pack(pady=10)
        tk.Label(header_frame, text=text, 
                font=self.title_font, bg="#f0f0f0").pack()
        tk.Label(header_frame, text=f"{self.tr('score')}: {self.progress['score']}", 
                font=self.label_font, bg="#f0f0f0").pack(pady=5)

    def create_menu_button(self, parent, text, command):
        """Создание кнопки меню"""
        tk.Button(parent, text=text, font=self.button_font,
                bg="#4CAF50", fg="white", command=command
                ).pack(pady=5, padx=20, ipadx=10, ipady=5)

    def show_root_selection(self):
        """Выбор корня"""
        self.clear_window()
        self.current_screen = self.show_root_selection
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True)
        
        self.create_header(main_frame, self.tr('select_root'))
        
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
        tk.Label(parent, text=f"{self.tr('guessed')}: {guessed}/{total}",
                font=self.label_font, bg="#f0f0f0").pack(side="left", padx=10)

    def show_sublevel_select(self, root_idx):
        """Выбор типа словообразования с пояснением корня"""
        self.current_root = root_idx
        level = self.levels[root_idx]
        self.clear_window()
        self.current_screen = lambda: self.show_sublevel_select(root_idx)
        
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True)
        
        self.create_header(main_frame, f"{level['root']}")
        
        # Блок с пояснением корня
        root_explanation = self.get_root_explanation(level['root'])
        if root_explanation != self.tr('no_explanation'):
            explanation_frame = tk.LabelFrame(main_frame, 
                                            text=self.tr('root_explanation'),
                                            font=self.label_font,
                                            bg="#f0f0f0",
                                            padx=10,
                                            pady=10)
            explanation_frame.pack(pady=10, fill="x", padx=20)
            
            tk.Label(explanation_frame, 
                    text=root_explanation,
                    font=self.label_font,
                    bg="#f0f0f0",
                    wraplength=600,
                    justify="left").pack()
        
        # Блок выбора типа образования
        sublevels_frame = tk.Frame(main_frame, bg="#f0f0f0")
        sublevels_frame.pack(pady=20)
        
        sublevels = [
            (self.tr('prefix_formation'), 'prefix'),
            (self.tr('suffix_formation'), 'suffix')
        ]
        
        for text, stype in sublevels:
            btn = tk.Button(sublevels_frame, 
                          text=text, 
                          font=self.button_font,
                          command=lambda t=stype: self.start_level(t),
                          bg="#FF9800", 
                          fg="white",
                          width=25)
            btn.pack(pady=5)
        
        self.add_back_button(self.show_root_selection)

    def get_root_explanation(self, root):
        """Получение пояснения для корня"""
        for item in self.morpheme_explanations:
            if item['root'] == root:
                return item.get('root_exp', self.tr('no_explanation'))
        return self.tr('no_explanation')

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
        """Игровой экран с новой областью пояснений"""
        self.clear_window()
        self.current_screen = self.show_game_screen
        level = self.levels[self.current_root]
        
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        left_frame = tk.Frame(main_frame, bg="#f0f0f0")
        left_frame.pack(side="left", fill="both", expand=True)
        
        # Левая панель
        header_frame = tk.Frame(left_frame, bg="#f0f0f0")
        header_frame.pack(pady=5)
        
        type_names = {
            'prefix': self.tr('prefix_formation'),
            'suffix': self.tr('suffix_formation')
        }
        tk.Label(header_frame, 
                text=f"{type_names[self.sub_type]}: {level['root']}", 
                font=self.label_font, bg="#f0f0f0").pack()
        tk.Label(header_frame, 
                text=f"{self.tr('score')}: {self.progress['score']} | {self.tr('words_guessed')}: {len(self.guessed_words)}/{self.get_total_words(self.current_root)}",
                font=self.label_font, bg="#f0f0f0").pack()
        
        self.answer_frame = tk.Frame(left_frame, bg="white", bd=2, relief="groove")
        self.answer_frame.pack(pady=10, ipadx=10, ipady=10, fill="x")
        
        self.morpheme_frame = tk.Frame(left_frame, bg="#f0f0f0")
        self.morpheme_frame.pack(pady=10)
        
        for morph in level['prefixes']:
            self.create_morpheme_button(morph, "#2196F3")
        
        # Кнопка корня без подсказки
        root_btn = tk.Button(self.morpheme_frame, 
                           text=level['root'], 
                           font=self.button_font,
                           command=lambda: self.add_morpheme(level['root']),
                           bg="#9C27B0", 
                           fg="white")
        root_btn.pack(side="left", padx=5, pady=5)
        
        for morph in level['suffixes']:
            self.create_morpheme_button(morph, "#FF9800")
        
        # Область для пояснений
        self.explanation_frame = tk.LabelFrame(left_frame, 
                                             text=self.tr('explanation'),
                                             font=self.label_font,
                                             bg="#f0f0f0",
                                             height=100)
        self.explanation_frame.pack(pady=10, fill="x", expand=False)
        self.explanation_label = tk.Label(self.explanation_frame, 
                                        text="", 
                                        font=self.label_font,
                                        bg="#f0f0f0",
                                        wraplength=600,
                                        justify="left")
        self.explanation_label.pack(padx=10, pady=5, fill="both", expand=True)
        
        # Правая панель
        right_frame = tk.Frame(main_frame, bg="#f0f0f0")
        right_frame.pack(side="right", fill="both", padx=20)
        
        # Отгаданные слова
        guessed_frame = tk.LabelFrame(right_frame, 
                                    text=self.tr('guessed_words'),
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
            'nouns': self.tr('nouns'),
            'adjectives': self.tr('adjectives'),
            'verbs': self.tr('verbs'),
            'adverbs': self.tr('adverbs')
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
                                       text=self.tr('hint'),
                                       font=self.label_font,
                                       bg="#f0f0f0")
        self.hints_frame.pack(pady=10, fill="both", expand=True)
        self.update_hints_display()
        
        # Управление
        control_frame = tk.Frame(left_frame, bg="#f0f0f0")
        control_frame.pack(pady=20)
        
        controls = [
            (self.tr('check'), "#4CAF50", self.check_answer),
            (self.tr('clear'), "#607D8B", self.clear_answer),
            (self.tr('remove'), "#FF5722", self.remove_last_morpheme),
            (self.tr('hint_cost'), "#9C27B0", self.buy_hint),
            (self.tr('back'), "#9E9E9E", lambda: self.show_sublevel_select(self.current_root))
        ]
        
        for text, color, cmd in controls:
            tk.Button(control_frame, text=text, font=self.button_font,
                     bg=color, fg="white", command=cmd).pack(side="left", padx=5)

    def create_morpheme_button(self, morph, color):
        """Создание кнопки морфемы с подсказкой"""
        btn = tk.Button(self.morpheme_frame, 
                      text=morph, 
                      font=self.button_font,
                      bg=color, 
                      fg="white", 
                      command=lambda m=morph: self.add_morpheme(m))
        btn.pack(side="left", padx=5, pady=5)
        self.setup_tooltip(btn, morph)

    def setup_tooltip(self, widget, morph):
        """Модифицированная система подсказок с фиксированным расположением"""
        if morph == self.levels[self.current_root]['root']:
            return

        def show_tip(event):
            try:
                explanations = next(item for item in self.morpheme_explanations 
                                  if item['root'] == self.levels[self.current_root]['root'])
                text = explanations.get(morph, self.tr('no_explanation'))
                
                # Улучшенное форматирование текста
                formatted_text = text
                if "пример:" in text:
                    parts = text.split("пример:")
                    formatted_text = f"{parts[0].strip()}\n\nПример: {parts[1].strip()}"
                
                self.explanation_label.config(text=formatted_text)
            
            except Exception as e:
                print(f"{self.tr('error')} в подсказке: {str(e)}")
                self.explanation_label.config(text=self.tr('no_explanation'))

        def hide_tip(event):
            self.explanation_label.config(text="")

        # Для слов добавляем обработку правой кнопки мыши
        if morph in [word for key in self.levels[self.current_root] 
                   if key.startswith('word-') for word in self.levels[self.current_root][key]]:
            widget.bind("<Button-3>", lambda e, w=morph: self.show_translation_popup(w))
        
        widget.bind("<Enter>", show_tip)
        widget.bind("<Leave>", hide_tip)

    def show_translation_popup(self, word):
        """Показать всплывающее окно с переводом в стиле пояснений"""
        if self.translation_frame:
            self.translation_frame.destroy()
        
        translated = self.translate_word(word)
        
        self.translation_frame = tk.LabelFrame(self.root, 
                                            text=self.tr('translation'),
                                            font=self.label_font,
                                            bg="#f0f0f0",
                                            padx=10,
                                            pady=10)
        self.translation_frame.place(relx=0.7, rely=0.3, anchor="center")
        
        # Добавляем текст перевода
        tk.Label(self.translation_frame, 
                text=f"{word} → {translated}",
                font=self.label_font,
                bg="#f0f0f0",
                wraplength=300,
                justify="left").pack()
        
        # Добавляем кнопку закрытия
        tk.Button(self.translation_frame, 
                 text="×", 
                 font=self.title_font,
                 command=self.translation_frame.destroy,
                 bg="#f0f0f0",
                 bd=0).pack(anchor="e")

        # Автоматическое закрытие через 5 секунд
        self.root.after(5000, self.translation_frame.destroy)

    def add_morpheme(self, morph):
        """Добавление морфемы в поле ответа"""
        label = tk.Label(self.answer_frame, 
                        text=morph, 
                        font=self.label_font,
                        bg="#E0E0E0", 
                        padx=5, 
                        pady=2)
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
            messagebox.showerror(self.tr('error'), self.tr('word_exists'))
        else:
            messagebox.showerror(self.tr('error'), self.tr('word_not_exists'))

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
                messagebox.showinfo(self.tr('level_completed'), self.tr('all_words_guessed'))
                self.save_progress()
            
            messagebox.showinfo(self.tr('correct'), 
                              f"+10 {self.tr('score')}! {self.tr('current_score')}: {self.progress['score']}")
            self.clear_answer()
            self.check_achievements()
            self.show_game_screen()
            
            if len(self.guessed_words) == self.get_total_words(self.current_root):
                self.show_root_selection()
        else:
            messagebox.showerror(self.tr('error'), self.tr('word_already_guessed'))

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
        self.current_screen = self.show_completed
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True)
        
        self.create_header(main_frame, self.tr('completed_levels'))
        
        if not self.progress['completed']:
            tk.Label(main_frame, text=self.tr('no_completed_levels'), 
                     font=self.label_font, bg="#f0f0f0").pack()
        else:
            for key in self.progress['completed']:
                level = self.levels[int(key)]
                total = self.get_total_words(int(key))
                guessed = len(self.progress['completed'][key].get('guessed', []))
                tk.Label(main_frame, 
                         text=f"{level['root']}: {guessed}/{total} {self.tr('guessed')}",
                         font=self.label_font, bg="#f0f0f0").pack(pady=5)
        
        self.add_back_button(self.show_main_menu)

    def add_back_button(self, command):
        """Добавление кнопки 'Назад'"""
        tk.Button(self.root, text=self.tr('back'), font=self.button_font,
                 bg="#9E9E9E", fg="white", command=command).pack(pady=20)

    def buy_hint(self):
        """Покупка подсказки"""
        if self.progress['score'] < 30:
            messagebox.showerror(self.tr('error'), self.tr('not_enough_points'))
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
            messagebox.showinfo(self.tr('hint'), self.tr('no_hints_available'))
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
        return explanations.get(word, self.tr('no_explanation'))

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
            ('no_hints', total_guessed >= 10, self.tr('no_hints_achievement')),
            ('word_master', total_guessed >= 50, self.tr('word_master_achievement')),
            ('economist', self.progress['score'] >= 500, self.tr('economist_achievement'))
        ]
        
        for name, condition, message in achievements:
            if condition and not self.progress['achievements'][name]:
                self.progress['achievements'][name] = True
                messagebox.showinfo(self.tr('achievement_unlocked'), 
                                  f"{self.tr('achievement_unlocked')}!\n{message}")
                self.save_progress()

    def reset_progress(self):
        """Сброс прогресса"""
        if messagebox.askyesno(self.tr('reset'), self.tr('confirm_reset')):
            self.progress = self.get_default_progress()
            self.save_progress()
            messagebox.showinfo(self.tr('reset'), self.tr('reset_confirm'))
            self.show_main_menu()

    def show_achievements(self):
        """Показать достижения"""
        self.clear_window()
        self.current_screen = self.show_achievements
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True)
        
        self.create_header(main_frame, self.tr('achievements'))
        
        achievements = [
            {
                'title': self.tr('no_hints_title'),
                'description': self.tr('no_hints_desc'),
                'status': self.progress['achievements']['no_hints']
            },
            {
                'title': self.tr('word_master_title'),
                'description': self.tr('word_master_desc'),
                'status': self.progress['achievements']['word_master']
            },
            {
                'title': self.tr('economist_title'),
                'description': self.tr('economist_desc'),
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
        """Настройки игры"""
        self.clear_window()
        self.current_screen = self.show_settings
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=50, pady=30)
        
        self.create_header(main_frame, self.tr('settings'))
        
        # Виджеты настроек
        self.lang_var = tk.StringVar(value=self.settings['language'])
        self.target_lang_var = tk.StringVar(value=self.settings['target_lang'])
        self.size_var = tk.StringVar(value=self.settings['window_size'])
        self.fullscreen_var = tk.BooleanVar(value=self.settings['fullscreen'])
        
        # Выбор языка интерфейса
        lang_frame = tk.Frame(main_frame, bg="#f0f0f0")
        lang_frame.pack(fill="x", pady=10)
        tk.Label(lang_frame, text=self.tr('interface_lang') + ":", 
                font=self.label_font, bg="#f0f0f0").pack(side="left")
        ttk.Combobox(lang_frame, textvariable=self.lang_var, 
                   values=['Русский', 'English', '中文'], state="readonly").pack(side="left", padx=10)
        
        # Выбор языка перевода
        target_lang_frame = tk.Frame(main_frame, bg="#f0f0f0")
        target_lang_frame.pack(fill="x", pady=10)
        tk.Label(target_lang_frame, text=self.tr('translation_lang') + ":", 
               font=self.label_font, bg="#f0f0f0").pack(side="left")
        ttk.Combobox(target_lang_frame, textvariable=self.target_lang_var, 
                    values=['en', 'es', 'de', 'fr', 'zh'], state="readonly").pack(side="left", padx=10)
        
        # Размер окна
        size_frame = tk.Frame(main_frame, bg="#f0f0f0")
        size_frame.pack(fill="x", pady=10)
        tk.Label(size_frame, text=self.tr('window_size') + ":", 
                font=self.label_font, bg="#f0f0f0").pack(side="left")
        ttk.Combobox(size_frame, textvariable=self.size_var, 
                    values=['800x600', '1200x800', '1600x900'], state="readonly").pack(side="left", padx=10)
        
        # Полноэкранный режим
        fullscreen_frame = tk.Frame(main_frame, bg="#f0f0f0")
        fullscreen_frame.pack(fill="x", pady=10)
        fullscreen_check = tk.Checkbutton(fullscreen_frame, 
                                         text=self.tr('fullscreen'),
                                         variable=self.fullscreen_var,
                                         font=self.label_font,
                                         bg="#f0f0f0")
        fullscreen_check.pack(side="left")
        
        # Кнопки управления
        btn_frame = tk.Frame(main_frame, bg="#f0f0f0")
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text=self.tr('apply'), font=self.button_font,
                 bg="#4CAF50", fg="white", command=self.save_settings).pack(side="left", padx=10)
        tk.Button(btn_frame, text=self.tr('cancel'), font=self.button_font,
                 bg="#F44336", fg="white", command=self.show_main_menu).pack(side="left", padx=10)
        
        self.add_back_button(self.show_main_menu)

    def save_settings(self):
        """Сохранение настроек"""
        new_settings = {
            'language': self.lang_var.get(),
            'target_lang': self.target_lang_var.get(),
            'window_size': self.size_var.get(),
            'fullscreen': self.fullscreen_var.get()
        }
        
        if new_settings != self.settings:
            self.settings.update(new_settings)
            self.apply_settings()
            self.save_progress()
            messagebox.showinfo(self.tr('settings'), self.tr('settings_applied'))
        
        self.show_main_menu()

    def translate_word(self, word):
        """Перевод слова с русского на выбранный язык"""
        try:
            target_lang = self.settings['target_lang']
            # Для китайского используем код 'zh'
            if target_lang == 'ch':
                target_lang = 'zh'
            translator = Translator(from_lang='ru', to_lang=target_lang)
            translation = translator.translate(word)
            return translation
        except Exception as e:
            print(f"{self.tr('error')}: {str(e)}")
            return self.tr('translation_error')