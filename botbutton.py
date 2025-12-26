import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from datetime import datetime

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# имена героев 
HERO_GUIDES = {
    # Juggernaut
    "джагер": ("Juggernaut", """
🎮 **Гайд на Juggernaut**

**📦 Ключевые предметы:**
1. **Фейзы/ПТ** -> **Маэлстром** -> **Манта**
2. **Башер/Аганим** -> **Баттерфляй/Скади**
3. **Можно: Радик (для умных)**  

**🛡️ Как играть ПРОТИВ него:**
• Контроль через стан/сайленс (Род, Хекс, Орхид).
• Предметы: **Гост сэптер**, **Блейд мэйл**, **Вангард/Кримсон**.
• В тимфайтах - фокусьте, джага наносит очень много урона.
"""),
    "джага": ("Juggernaut", None),
    "juggernaut": ("Juggernaut", None),
    "юрнеро": ("Juggernaut", None),

    # Templar Assassin
    "тэмпларка": ("Templar Assassin", """
🎮 **Гайд на Templar Assassin**

**📦 Ключевые предметы:**
1. **Фейзы/ПТ** -> **Дезолятор** -> **Блинк**
2. **БКБ (ОБЯЗАТЕЛЬНО)** -> **Кристалис/Даедалус**
3. **Можно: Баттерфляй, Скади, Рапира**

**🛡️ Как играть ПРОТИВ нее:**
• **МАГИЧЕСКИЙ УРОН** (некр, пудж) быстрый переодический урон ломает **Refraction**.
• Предметы: **Гем/Сентри**, **Варды**.
• Расставляйте **варды**, чтобы видеть трапки.
• В драках фокусируйте **ПЕРВОЙ**, пока не выжала БКБ.
"""),
    "та": ("Templar Assassin", None),
    "ланая": ("Templar Assassin", None),
    "templar": ("Templar Assassin", None),
    "templar assasin": ("Templar Assassin", None),
    "темпларка": ("Templar Assassin", None),

    # Pudge
    "пудж": ("Pudge", """
🎮 **Гайд на Pudge**

**📦 Ключевые предметы (РОМ):**
1. **Фазы** -> **Блинк/Аганим** -> **Хек스/Блейд мэйл**
2. **БКБ (иногда)** -> **Шива/Бладстоун**
3. **Можно: Тарраска, Кримсон, Этериал**

**🛡️ Как играть ПРОТИВ него:**
• Стойте за крипами против хука. Следите за ним по мини карте
• Предметы: **Блинк**, **Форс стэфф**, **Линка**
• Разрушайте его **фогги** (варды, скан).
• В драках убивайте первым - без ульты он слаб.
"""),
    "падж": ("Pudge", None),
    "пуджик": ("Pudge", None),
    "pudge": ("Pudge", None),

    # Morphling
    "морф": ("Morphling", """
🎮 **Гайд на Morphling**

**📦 Ключевые предметы:**
1. **ПТ** -> **Этериал** -> **Скади**
2. **Линка/Баттерфляй** -> **Сатаника/Мьёллнир**
3. **Можно: БКБ, Рапира, Хекс**

**🛡️ Как играть ПРОТИВ:**
• **Контроль** (Шейкер, Лион)
• Предметы: **Орчид**, **Хекс**, **Сильвер Эдж**
• Давить на ранней стадии игры 
• Контролить, не давать сбежать
"""),
    "морфлинг": ("Morphling", None),
    "morphling": ("Morphling", None),
    "морфик": ("Morphling", None),

    # Earthshaker
    "шейкер": ("Earthshaker", """
🎮 **Гайд на Earthshaker**

**📦 Ключевые предметы (поддержка):**
1. **Арканы** -> **Блинк** -> **Аганим**
2. **Форс/Еул** -> **БКБ/Шива/Рефрешер**
3. **Можно: Бладстон, Хекс**

**🛡️ Как играть ПРОТИВ:**
• **Не копиться** на Echo Slam
• Держать **дистанцию** от Fissure
• Предметы: **БКБ**, **Линка**, **Хекс**
• Варды на хг - видеть его позицию
"""),
    "earthshaker": ("Earthshaker", None),
    "землетряс": ("Earthshaker", None),
    "эс": ("Earthshaker", None),
    "шакер": ("Earthshaker", None),

    # Invoker
    "инвокер": ("Invoker", """
🎮 **Гайд на Invoker**

**📦 Ключевые предметы (МИД):**
1. **ПТ/Фейзы** -> **Мидас** -> **Аганим** (критично)
2. **Орчид/БКБ** -> **Шива/Октарин/Хекс**
3. **Можно: Блинк, вич блейд, Скади, Рапира**

**🛡️ Как играть ПРОТИВ:**
• **Агрессивный ранней игры** - у него 0 задержек
• Предметы: **БКБ**, **Линкенс** (от Солар Крейда), **Гост**
• **Сайленс и стан** (Пудж, Найт, Сайленсер)
• Не копиться на **Метеор + Бласт**
"""),
    "маг": ("Invoker", None),
    "invoker": ("Invoker", None),
    "карл": ("Invoker", None),
    "вокер": ("Invoker", None),

    # Riki
    "рики": ("Riki", """
🎮 **Гайд на Riki**

**📦 Ключевые предметы:**
1. **БФ/ПТ** -> **Диффузал** -> **Басер/Манта**
2. **Баттерфляй/Скади** -> **Абеддон/БКБ**
3. **Можно: БФ, Рапира, Мьёллнир**

**🛡️ Как играть ПРОТИВ:**
• **СЕНТРИИ ВСЮДУ!** (гем, варды)
• Герои с **АОЕ уроном** (Лешрак, Акс)
• Предметы: **Гост**, **Блейд мэйл**, **Мьёллнир**
• **Детекторы невидимости** постоянно
"""),
    "riki": ("Riki", None),
    "невидимка": ("Riki", None),
    "рикимару": ("Riki", None),

    # Clinkz
    "клинкз": ("Clinkz", """
🎮 **Гайд на Clinkz**

**📦 Ключевые предметы:**
1. **Орхид** -> **Дезирер/Кристалис** -> **БКБ**
2. **БФ/Даэдолус** -> **Бладторн/Скади**
3. **Можно: Блинк, Манта, Рапира**

**🛡️ Как играть ПРОТИВ:**
• **Группировка** - он любит соло килы
• Герои с **ивнейом** (Спектра, Акс)
• Предметы: **Гост**, **Вангард**, **Блейд мэйл**
• **Варды в лесу** - видеть его ганки
"""),
    "clinkz": ("Clinkz", None),
    "скелет": ("Clinkz", None),
    "клиник": ("Clinkz", None),
    "клинкс": ("Clinkz", None),

    # Phantom Assassin
    "па": ("Phantom Assassin", """
🎮 **Гайд на Phantom Assassin**

**📦 Ключевые предметы:**
1. **БФ/ПТ** -> **Баттерфляй** -> **БКБ**
2. **Абеддон/Сатаника** -> **Рапира/Скади**
3. **Можно: Блинк, Мьёллнир, Манта**

**🛡️ Как играть ПРОТИВ:**
• **МКБ!** (Москито, Виндранер)
• Предметы: **Гост**, **Блейд мэйл**, **Шива**
• Контроль через **стан до БКБ**
• Не давать **фармить мид/лейт**
"""),
    "фантом ассасин": ("Phantom Assassin", None),
    "пха": ("Phantom Assassin", None),
    "phantom assassin": ("Phantom Assassin", None),
    "фантомка": ("Phantom Assassin", None),
    "фа": ("Phantom Assassin", None),

    # Timbersaw
    "тимбер": ("Timbersaw", """
🎮 **Гайд на Timbersaw**

**📦 Ключевые предметы:**
1. **Soul Ring** -> **Arcane Boots** -> **Eul's Scepter**
2. **Kaya and Sange** -> **Lotus Orb** / **Shiva's Guard**
3. **Поздняя игра: Heart of Tarrasque, Aghanim's Scepter, Octarine Core**

**🛡️ Как играть ПРОТИВ:**
• Герои с **магическим иммунитетом** (Naix, Juggernaut)
• **Break** (Silver Edge, Viper)
• Предметы: **Spirit Vessel**, **Heaven's Halberd**, **Rod of Atos**
• Уклоняться от **Timber Chain** через деревья
"""),
    "тимберсо": ("Timbersaw", None),
    "timbersaw": ("Timbersaw", None),
    "пильщик": ("Timbersaw", None),

    # Dark Seer
    "дарк сир": ("Dark Seer", """
🎮 **Гайд на Dark Seer**

**📦 Ключевые предметы:**
1. **Soul Ring** -> **Arcane Boots** -> **Mekansm**
2. **Guardian Greaves** -> **Aghanim's Scepter** -> **Shiva's Guard**
3. **Поздняя игра: Refresher Orb, Octarine Core, Heart of Tarrasque**

**🛡️ Как играть ПРОТИВ:**
• Разрушать **Ion Shell** на крипах
• Герои с **Area of Effect** уроном (Leshrac, Sand King)
• Предметы: **Pipe of Insight**, **Crimson Guard**, **Black King Bar**
• Избегать узких коридоров для **Vacuum + Wall**
"""),
    "дарксир": ("Dark Seer", None),
    "dark seer": ("Dark Seer", None),
    "темный силач": ("Dark Seer", None),

    # Naga Siren
    "нага": ("Naga Siren", """
🎮 **Гайд на Naga Siren**

**📦 Ключевые предметы:**
1. **Power Treads** -> **Diffusal Blade** -> **Manta Style**
2. **Heart of Tarrasque** -> **Butterfly** / **Eye of Skadi**
3. **Поздняя игра: Abyssal Blade, Monkey King Bar, Divine Rapier**

**🛡️ Как играть ПРОТИВ:**
• **AOE контроль** (Earthshaker, Magnus)
• Предметы: **Battle Fury**, **Maelstrom**, **Mjollnir**
• **Gem of True Sight** против иллюзий
• Разрушать **Song of the Siren** через BKB или сильные дебафы
"""),
    "нага сайрен": ("Naga Siren", None),
    "naga siren": ("Naga Siren", None),
    "сирена": ("Naga Siren", None),

    # Outworld Destroyer
    "аутворлд": ("Outworld Destroyer", """
🎮 **Гайд на Outworld Destroyer**

**📦 Ключевые предметы:**
1. **Power Treads** -> **Witch Blade** -> **BKB**
2. **Hurricane Pike** -> **Shiva's Guard** / **Scythe of Vyse**
3. **Поздняя игра: Octarine Core, Refresher Orb, Aeon Disk**

**🛡️ Как играть ПРОТИВ:**
• Герои с **сильным физическим уроном** (Ursa, Troll)
• **Silence** и **stun** (Silencer, Lion)
• Предметы: **Black King Bar**, **Linken's Sphere**, **Ethereal Blade**
• Избегать **Astral Imprisonment** в одиночку
"""),
    "аутворлд дестройер": ("Outworld Destroyer", None),
    "од": ("Outworld Destroyer", None),
    "outworld destroyer": ("Outworld Destroyer", None),
    "разрушитель миров": ("Outworld Destroyer", None),

    # Storm Spirit
    "шторм": ("Storm Spirit", """
🎮 **Гайд на Storm Spirit**

**📦 Ключевые предметы:**
1. **Power Treads** -> **Kaya** -> **Orchid Malevolence**
2. **Bloodstone** -> **Shiva's Guard** / **Scythe of Vyse**
3. **Поздняя игра: Octarine Core, Refresher Orb, Aeon Disk**

**🛡️ Как играть ПРОТИВ:**
• **Silence** и **instant stun** (Silencer, Skywrath)
• Предметы: **Orchid Malevolence**, **Scythe of Vyse**, **Rod of Atos**
• **Mana burn** герои (Anti-Mage, Lion)
• Контролить **Ball Lightning** через silence/hex
"""),
    "шторм спирит": ("Storm Spirit", None),
    "storm spirit": ("Storm Spirit", None),
    "шторма": ("Storm Spirit", None),

    # Void Spirit
    "войд спирит": ("Void Spirit", """
🎮 **Гайд на Void Spirit**

**📦 Ключевые предметы:**
1. **Power Treads** -> **Witch Blade** -> **Eul's Scepter**
2. **Kaya and Sange** -> **Aghanim's Scepter** -> **Shiva's Guard**
3. **Поздняя игра: Octarine Core, Refresher Orb, Heart of Tarrasque**

**🛡️ Как играть ПРОТИВ:**
• **Silence** и **root** (Silencer, Treant)
• Предметы: **Orchid Malevolence**, **Scythe of Vyse**, **Heaven's Halberd**
• Контролить мобильность через **AoE станы**
• Не давать набрать **Resonant Pulse** stacks
"""),
    "void spirit": ("Void Spirit", None),
    "спирит войд": ("Void Spirit", None),

    # Spirit Breaker
    "спирит брейкер": ("Spirit Breaker", """
🎮 **Гайд на Spirit Breaker**

**📦 Ключевые предметы:**
1. **Phase Boots** -> **Urn of Shadows** -> **Shadow Blade**
2. **Black King Bar** -> **Aghanim's Scepter** -> **Assault Cuirass**
3. **Поздняя игра: Heart of Tarrasque, Shiva's Guard, Octarine Core**

**🛡️ Как играть ПРОТИВ:**
• **Stun** и **slow** во время **Charge of Darkness**
• Предметы: **Eul's Scepter**, **Force Staff**, **Ghost Scepter**
• **Vision** по карте (wards, Hawk)
• Не стоять в одиночку против его ганков
"""),
    "спиритбрейкер": ("Spirit Breaker", None),
    "баратрум": ("Spirit Breaker", None),
    "бара": ("Spirit Breaker", None),
    "spirit breaker": ("Spirit Breaker", None),

    # Faceless Void
    "фейселес": ("Faceless Void", """
🎮 **Гайд на Faceless Void**

**📦 Ключевые предметы:**
1. **Power Treads** -> **Mask of Madness** -> **Maelstrom**
2. **Manta Style** -> **Butterfly** / **Eye of Skadi**
3. **Поздняя игра: Monkey King Bar, Daedalus, Satanic**

**🛡️ Как играть ПРОТИВ:**
• Герои с **уходом из Chronosphere** (Void Spirit, Storm)
• Предметы: **Black King Bar**, **Force Staff**, **Eul's Scepter**
• **AOE контроль** вне баббла (Enigma, Magnus)
• Не стоять группой в его **Chronosphere**
"""),
    "фейселес войд": ("Faceless Void", None),
    "безглазый": ("Faceless Void", None),
    "faceless void": ("Faceless Void", None),
    "войд": ("Faceless Void", None),
    "безликий": ("Faceless Void", None),

    # Earth Spirit
    "ёрз": ("Earth Spirit", """
🎮 **Гайд на Earth Spirit**

**📦 Ключевые предметы:**
1. **Soul Ring** -> **Arcane Boots** -> **Urn of Shadows**
2. **Spirit Vessel** -> **Aghanim's Scepter** -> **Lotus Orb**
3. **Поздняя игра: Shiva's Guard, Heart of Tarrasque, Octarine Core**

**🛡️ Как играть ПРОТИВ:**
• Герои с **магическим иммунитетом** (Lifestealer, Juggernaut)
• **Dispel** его **Geomagnetic Grip** (Oracle, Legion)
• Предметы: **Black King Bar**, **Linken's Sphere**, **Manta Style**
• Уклоняться от **Boulder Smash** и **Rolling Boulder**
"""),
    "земля": ("Earth Spirit", None),
    "земеля": ("Earth Spirit", None),
    "earth spirit": ("Earth Spirit", None),
    "камень": ("Earth Spirit", None),
}

GUIDE_DB = {}
for keys, (display_name, message) in HERO_GUIDES.items():
    if message is None:
        for k, (dn, msg) in HERO_GUIDES.items():
            if dn == display_name and msg is not None:
                message = msg
                break
    GUIDE_DB[keys] = (display_name, message)

UNIQUE_HEROES = sorted({info[0] for info in GUIDE_DB.values()})

def get_main_keyboard():
    """Основная клавиатура с кнопками"""
    keyboard = [
        [InlineKeyboardButton("👤 Поиск вручную", callback_data="search_manual")],
        [InlineKeyboardButton("📚 Все герои", callback_data="all_heroes")],
        [InlineKeyboardButton("❓ Помощь", callback_data="help")],
        [InlineKeyboardButton("🔥 Популярные", callback_data="popular")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_heroes_keyboard(page=0):
    """Клавиатура со всеми героями (пагинация)"""
    heroes_per_page = 12
    start_idx = page * heroes_per_page
    end_idx = start_idx + heroes_per_page
    
    heroes_page = UNIQUE_HEROES[start_idx:end_idx]
    
    keyboard = []
    row = []
    for i, hero in enumerate(heroes_page):
        row.append(InlineKeyboardButton(hero, callback_data=f"hero_{hero}"))
        if len(row) == 3:
            keyboard.append(row)
            row = []
    if row: 
        keyboard.append(row)
    
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"page_{page-1}"))
    if end_idx < len(UNIQUE_HEROES):
        nav_buttons.append(InlineKeyboardButton("Вперед ➡️", callback_data=f"page_{page+1}"))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    keyboard.append([InlineKeyboardButton("🏠 Главная", callback_data="main_menu")])
    
    return InlineKeyboardMarkup(keyboard)

def get_popular_keyboard():
    """Клавиатура с популярными героями"""
    popular_heroes = ["Juggernaut", "Pudge", "Invoker", "Templar Assassin", "Phantom Assassin", "Riki"]
    
    keyboard = []
    row = []
    for i, hero in enumerate(popular_heroes):
        if hero in UNIQUE_HEROES:
            row.append(InlineKeyboardButton(hero, callback_data=f"hero_{hero}"))
            if len(row) == 2:
                keyboard.append(row)
                row = []
    if row:
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("📚 Все герои", callback_data="all_heroes")])
    keyboard.append([InlineKeyboardButton("🏠 Главная", callback_data="main_menu")])
    
    return InlineKeyboardMarkup(keyboard)

def log_request(user, message: str, found: bool = False, hero_name: str = ""):
    """Логирует запросы в консоль"""
    try:
        time_str = datetime.now().strftime("%H:%M:%S")
        username = user.username if user and user.username else "без_username"
        first_name = user.first_name if user else "Неизвестный"
        
        if found:
            print(f"[{time_str}] 🟢 @{username} ({first_name}): '{message}' -> {hero_name}")
        else:
            print(f"[{time_str}] 🔴 @{username} ({first_name}): '{message}' -> НЕ НАЙДЕН")
    except Exception as e:
        print(f"Ошибка логирования: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.message.from_user
    log_request(user, "/start", True, "Приветствие")
    
    welcome_text = (
        "👋 **Здарова!** 🎮\n\n"
        "Это бот-справочник по Dota 2 с **кнопками!**\n\n"
        "📌 **Выбери действие:**"
    )
    
    await update.message.reply_text(
        welcome_text,
        parse_mode='Markdown',
        reply_markup=get_main_keyboard()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    user = update.message.from_user
    log_request(user, "/help", True, "Помощь")
    
    help_text = (
        "🤖 **Dota 2 Guide Bot - Помощник для новичков**\n\n"
        "Этот бот создан, чтобы помочь тебе освоить Dota 2!\n\n"
        "✨ **Что он умеет:**\n"
        "• Показывает **предметы** для каждого героя\n"
        "• Дает советы по **раскачке** навыков\n"
        "• Рассказывает, **как играть против** конкретного героя\n"
        "• Поддерживает **русские и английские** названия\n\n"
        "🎯 **Как использовать:**\n"
        "1. Нажми кнопку '📚 Все герои' для списка\n"
        "2. Или напиши имя героя в чат (например: 'джага')\n"
        "3. Выбери героя из списка и получи гайд\n\n"
        "🆘 **Новичкам на заметку:**\n"
        "• Не стесняйся экспериментировать с билдами\n"
        "• Смотрите про-матчи для вдохновения\n"
        "• Главное - получать удовольствие от игры!\n\n"
        "💪 **Удачи в игре, бро!**"
    )
    
    keyboard = [
        [InlineKeyboardButton("📚 Все герои", callback_data="all_heroes")],
        [InlineKeyboardButton("🔥 Популярные", callback_data="popular")],
        [InlineKeyboardButton("🏠 Главная", callback_data="main_menu")]
    ]
    
    if update.callback_query:
        await update.callback_query.message.edit_text(
            help_text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text(
            help_text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    data = query.data
    
    if data == "main_menu":
        await query.message.edit_text(
            "🏠 **Главное меню:**\n\nВыбери действие:",
            parse_mode='Markdown',
            reply_markup=get_main_keyboard()
        )
    
    elif data == "all_heroes":
        log_request(user, "all_heroes", True, "Список героев")
        await query.message.edit_text(
            f"📚 **Все герои:** ({len(UNIQUE_HEROES)} героев)\n\nВыбери героя:",
            parse_mode='Markdown',
            reply_markup=get_heroes_keyboard(0)
        )
    
    elif data.startswith("page_"):
        page = int(data.split("_")[1])
        await query.message.edit_reply_markup(
            reply_markup=get_heroes_keyboard(page)
        )
    
    elif data == "popular":
        log_request(user, "popular", True, "Популярные герои")
        await query.message.edit_text(
            "🔥 **Популярные герои:**\n\nВыбери героя:",
            parse_mode='Markdown',
            reply_markup=get_popular_keyboard()
        )
    
    elif data == "help":
        help_text = "🤖 **Dota 2 Guide Bot - Помощник для новичков**\n\nЭтот бот создан, чтобы помочь тебе освоить Dota 2!\n\n✨ **Что он умеет:**\n• Показывает **предметы** для каждого героя\n• Дает советы по **раскачке** навыков\n• Рассказывает, **как играть против** конкретного героя\n• Поддерживает **русские и английские** названия\n\n🎯 **Как использовать:**\n1. Нажми кнопку '📚 Все герои' для списка\n2. Или напиши имя героя в чат (например: 'джага')\n3. Выбери героя из списка и получи гайд\n\n💪 **Удачи в игре, бро!**"
        
        keyboard = [
            [InlineKeyboardButton("📚 Все герои", callback_data="all_heroes")],
            [InlineKeyboardButton("🔥 Популярные", callback_data="popular")],
            [InlineKeyboardButton("🏠 Главная", callback_data="main_menu")]
        ]
        
        await query.message.edit_text(
            help_text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    elif data == "search_manual":
        await query.message.edit_text(
            "🔍 **Поиск героя вручную:**\n\nДля ввода имени персонажа вручную просто **отправьте мне его имя!**\n\n📝 **Примеры:**\n• `джага` или `juggernaut`\n• `пудж` или `pudge`\n• `та` или `templar assasin`\n• `инвокер` или `invoker`\n\n💡 **Совет:** Можно использовать русские и английские названия!",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 Главная", callback_data="main_menu")],
                [InlineKeyboardButton("📚 Все герои", callback_data="all_heroes")]
            ])
        )
    
    elif data.startswith("hero_"):
        hero_name = data[5:]
        
        found = False
        guide_text = ""
        for key, (name, text) in GUIDE_DB.items():
            if name == hero_name:
                found = True
                guide_text = text
                break
        
        if found:
            log_request(user, hero_name, True, hero_name)
            
            keyboard = [
                [InlineKeyboardButton("📚 Все герои", callback_data="all_heroes")],
                [InlineKeyboardButton("🔥 Популярные", callback_data="popular")],
                [InlineKeyboardButton("🏠 Главная", callback_data="main_menu")]
            ]
            
            await query.message.edit_text(
                f"**{hero_name}**\n{guide_text}",
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            log_request(user, hero_name, False)
            await query.message.edit_text(
                f"Герой'{hero_name}' еще не добавлен. Либо я не смог распознать вашу команду!",
                parse_mode='Markdown',
                reply_markup=get_main_keyboard()
            )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений"""
    user_message = update.message.text.strip().lower()
    user = update.message.from_user
    
    if user_message in GUIDE_DB:
        hero_name, guide_text = GUIDE_DB[user_message]
        
        log_request(user, user_message, True, hero_name)
        
        keyboard = [
            [InlineKeyboardButton("📚 Все герои", callback_data="all_heroes")],
            [InlineKeyboardButton("🔥 Популярные", callback_data="popular")],
            [InlineKeyboardButton("🏠 Главная", callback_data="main_menu")]
        ]
        
        await update.message.reply_text(
            f"**{hero_name}**\n{guide_text}",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        log_request(user, user_message, False)
        
        keyboard = [
            [InlineKeyboardButton("👤 Поиск вручную", callback_data="search_manual")],
            [InlineKeyboardButton("📚 Все герои", callback_data="all_heroes")],
            [InlineKeyboardButton("🔥 Популярные", callback_data="popular")],
            [InlineKeyboardButton("❓ Помощь", callback_data="help")]
        ]
        
        await update.message.reply_text(
            f"Герой '{user_message}' еще не добавлен. Либо я не смог распознать вашу команду!\n\n"
            "💡 **Советы:**\n"
            "• Попробуй другое название\n"
            "• Используй кнопки\n"
            "• Напиши `/start` для главного меню",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

def main():
    """Запускает бота"""
    TOKEN = "8275172773:AAHygwPVQ6yOMlZ5fHpoXohrft43gYHnHQI"
    
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Бот с кнопками запущен!")
    print("📊 Логи запросов в консоли:")
    print("🟢 - найден герой")
    print("🔴 - не найден")
    print("-" * 40)
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()