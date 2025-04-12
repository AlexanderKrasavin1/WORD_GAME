import json
import tkinter as tk
from tkinter import messagebox, font, ttk
import random
from translate import Translator

SAVE_FILE = "progress.json"

class WordGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Formation PRO")
        
        # Загрузка прогресса и настроек
        self.progress = self.load_progress()
        self.settings = self.progress['settings']
        
        # Система локализации
        self.locales = {
            'Русский': {
                'main_menu': 'Главное меню',
                'play': 'Играть',
                'completed_levels': 'Пройденные уровни',
                'achievements': 'Достижения',
                'settings': 'Настройки',
                'reset': 'Сбросить прогресс',
                'exit': 'Выйти',
                'score': 'Очки',
                'select_root': 'Выберите корень',
                'guessed': 'Угадано',
                'hint': 'Подсказка',
                'check': 'Проверить',
                'clear': 'Очистить поле',
                'remove': 'Удалить последнюю',
                'back': 'Назад',
                'correct': 'Правильно!',
                'error': 'Ошибка',
                'word_exists': 'Слово существует, но образуется по-другому!',
                'word_not_exists': 'Такого слова не существует!',
                'level_completed': 'Уровень пройден!',
                'all_words_guessed': 'Все слова отгаданы! +50 бонусных очков',
                'word_already_guessed': 'Это слово уже отгадано!',
                'hint_cost': 'Подсказка (30)',
                'not_enough_points': 'Недостаточно очков для подсказки!',
                'no_hints_available': 'Нет доступных слов для подсказки!',
                'settings_applied': 'Изменения применены!',
                'interface_lang': 'Язык интерфейса',
                'translation_lang': 'Язык перевода',
                'window_size': 'Размер окна',
                'fullscreen': 'Полноэкранный режим',
                'apply': 'Применить',
                'cancel': 'Отмена',
                'translation_error': 'Ошибка перевода',
                'root_explanation': 'Пояснение корня',
                'no_explanation': 'Пояснение отсутствует',
                'guessed_words': 'Отгаданные слова',
                'nouns': 'Существительные',
                'adjectives': 'Прилагательные',
                'verbs': 'Глаголы',
                'adverbs': 'Наречия',
                'prefix_formation': 'Приставочное образование',
                'suffix_formation': 'Суффиксальное образование',
                'reset_confirm': 'Прогресс и очки сброшены!',
                'no_completed_levels': 'Пока нет пройденных уровней',
                'achievement_unlocked': 'Достижение!',
                'current_score': 'Текущий счёт',
                'words_guessed': 'Угадано слов',
                'prefix': 'Приставка',
                'suffix': 'Суффикс',
                'no_hints_achievement': 'Отгадано 10 слов без подсказок',
                'word_master_achievement': 'Отгадано 50 слов',
                'economist_achievement': 'Накоплено 500 очков',
                'no_hints_title': 'Чистая победа',
                'no_hints_desc': 'Отгадать 10 слов без использования подсказок',
                'word_master_title': 'Мастер словообразования',
                'word_master_desc': 'Отгадать 50 слов',
                'economist_title': 'Экономист',
                'economist_desc': 'Накопить 500 очков',
                'confirm_reset': 'Вы уверены, что хотите сбросить прогресс?'
            },
            'English': {
                'main_menu': 'Main Menu',
                'play': 'Play',
                'completed_levels': 'Completed Levels',
                'achievements': 'Achievements',
                'settings': 'Settings',
                'reset': 'Reset Progress',
                'exit': 'Exit',
                'score': 'Score',
                'select_root': 'Select Root',
                'guessed': 'Guessed',
                'hint': 'Hint',
                'check': 'Check',
                'clear': 'Clear Field',
                'remove': 'Remove Last',
                'back': 'Back',
                'correct': 'Correct!',
                'error': 'Error',
                'word_exists': 'Word exists but formed differently!',
                'word_not_exists': 'Word does not exist!',
                'level_completed': 'Level completed!',
                'all_words_guessed': 'All words guessed! +50 bonus points',
                'word_already_guessed': 'This word is already guessed!',
                'hint_cost': 'Hint (30)',
                'not_enough_points': 'Not enough points for a hint!',
                'no_hints_available': 'No words available for hints!',
                'settings_applied': 'Changes applied!',
                'interface_lang': 'Interface Language',
                'translation_lang': 'Translation Language',
                'window_size': 'Window Size',
                'fullscreen': 'Fullscreen Mode',
                'apply': 'Apply',
                'cancel': 'Cancel',
                'translation_error': 'Translation Error',
                'root_explanation': 'Root Explanation',
                'no_explanation': 'No explanation available',
                'guessed_words': 'Guessed Words',
                'nouns': 'Nouns',
                'adjectives': 'Adjectives',
                'verbs': 'Verbs',
                'adverbs': 'Adverbs',
                'prefix_formation': 'Prefix Formation',
                'suffix_formation': 'Suffix Formation',
                'reset_confirm': 'Progress and scores reset!',
                'no_completed_levels': 'No completed levels yet',
                'achievement_unlocked': 'Achievement Unlocked!',
                'current_score': 'Current score',
                'words_guessed': 'Words guessed',
                'prefix': 'Prefix',
                'suffix': 'Suffix',
                'no_hints_achievement': 'Guessed 10 words without hints',
                'word_master_achievement': 'Guessed 50 words',
                'economist_achievement': 'Earned 500 points',
                'no_hints_title': 'Clean Victory',
                'no_hints_desc': 'Guess 10 words without using hints',
                'word_master_title': 'Word Formation Master',
                'word_master_desc': 'Guess 50 words',
                'economist_title': 'Economist',
                'economist_desc': 'Earn 500 points',
                'confirm_reset': 'Are you sure you want to reset progress?'
            },
            '中文': {
                'main_menu': '主菜单',
                'play': '玩',
                'completed_levels': '完成的关卡',
                'achievements': '成就',
                'settings': '设置',
                'reset': '重置进度',
                'exit': '退出',
                'score': '分数',
                'select_root': '选择词根',
                'guessed': '已猜',
                'hint': '提示',
                'check': '检查',
                'clear': '清空',
                'remove': '删除最后',
                'back': '返回',
                'correct': '正确!',
                'error': '错误',
                'word_exists': '单词存在但形式不同!',
                'word_not_exists': '单词不存在!',
                'level_completed': '关卡完成!',
                'all_words_guessed': '所有单词已猜出! +50 奖励分',
                'word_already_guessed': '这个单词已经猜过了!',
                'hint_cost': '提示 (30)',
                'not_enough_points': '点数不足无法获取提示!',
                'no_hints_available': '没有可用的提示单词!',
                'settings_applied': '设置已应用!',
                'interface_lang': '界面语言',
                'translation_lang': '翻译语言',
                'window_size': '窗口大小',
                'fullscreen': '全屏模式',
                'apply': '应用',
                'cancel': '取消',
                'translation_error': '翻译错误',
                'root_explanation': '词根解释',
                'no_explanation': '无解释',
                'guessed_words': '已猜单词',
                'nouns': '名词',
                'adjectives': '形容词',
                'verbs': '动词',
                'adverbs': '副词',
                'prefix_formation': '前缀构词',
                'suffix_formation': '后缀构词',
                'reset_confirm': '进度和分数已重置!',
                'no_completed_levels': '暂无完成的关卡',
                'achievement_unlocked': '成就达成!',
                'current_score': '当前分数',
                'words_guessed': '已猜单词',
                'prefix': '前缀',
                'suffix': '后缀',
                'no_hints_achievement': '不提示猜出10个单词',
                'word_master_achievement': '猜出50个单词',
                'economist_achievement': '累积500分',
                'no_hints_title': '纯净胜利',
                'no_hints_desc': '不使用提示猜出10个单词',
                'word_master_title': '构词大师',
                'word_master_desc': '猜出50个单词',
                'economist_title': '经济学家',
                'economist_desc': '累积500分',
                'confirm_reset': '确定要重置进度吗?'
            }
        }
        
        self.current_locale = self.settings['language']
        self.locale = self.locales.get(self.current_locale, self.locales['Русский'])
        
        # Применение настроек
        self.apply_settings()
        
        # Инициализация данных игры
        self.load_data_files()
        
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

    def load_data_files(self):
        """Загрузка файлов с уровнями и объяснениями"""
        try:
            with open('levels.json', 'r', encoding='utf-8') as f:
                self.levels = json.load(f)
            with open('morpheme_explanations.json', 'r', encoding='utf-8') as f:
                self.morpheme_explanations = json.load(f)
        except FileNotFoundError:
            # Создаем минимальные тестовые данные, если файлы не найдены
            self.levels = [{
                "root": "вод",
                "prefixes": ["при", "за", "пере"],
                "suffixes": ["а", "ный", "ить"],
                "word-prefix": ["привод", "завод", "перевод"],
                "word-suffix": ["водить", "водный", "водитель"]
            }]
            
            self.morpheme_explanations = [{
                "root": "вод",
                "root_exp": "Корень, связанный с водой или вождением",
                "при": "Приставка, обозначающая приближение",
                "за": "Приставка, обозначающая начало действия",
                "пере": "Приставка, обозначающая повторение или изменение",
                "а": "Суффикс для образования существительных",
                "ный": "Суффикс для образования прилагательных",
                "ить": "Суффикс для образования глаголов",
                "привод": "Устройство для передачи движения, пример: привод механизма",
                "завод": "Промышленное предприятие, пример: автомобильный завод",
                "перевод": "1) Перемещение через что-либо, 2) Текст на другом языке",
                "водить": "Управлять транспортным средством, пример: водить машину",
                "водный": "Связанный с водой, пример: водный раствор",
                "водитель": "Человек, управляющий транспортным средством"
            }]

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
        
        self.create_header(main_frame, f"{self.tr('root')}: {level['root']}")
        
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
        """Игровой экран"""
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
        """Создание всплывающих подсказок (исключая корень)"""
        if morph == self.levels[self.current_root]['root']:
            return
            
        def show_tip(event):
            try:
                explanations = next(item for item in self.morpheme_explanations 
                                  if item['root'] == self.levels[self.current_root]['root'])
                text = explanations.get(morph, self.tr('no_explanation'))
                
                tip = tk.Toplevel(self.root)
                tip.wm_overrideredirect(True)
                tip.geometry(f"+{self.root.winfo_pointerx()+15}+{self.root.winfo_pointery()+15}")
                tk.Label(tip, text=text, bg="#FFF9C4", font=self.label_font, 
                        padx=5, pady=3, justify="left").pack()
                self.current_tooltip = tip
            
            except Exception as e:
                print(f"{self.tr('error')} в подсказке: {str(e)}")
        
        def hide_tip(event):
            if hasattr(self, 'current_tooltip'):
                self.current_tooltip.destroy()
        
        widget.bind("<Enter>", show_tip)
        widget.bind("<Leave>", hide_tip)

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