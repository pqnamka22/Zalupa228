import telebot
from telebot import types
import random

TOKEN = "8238153006:AAGtGZnLt4SkSWnCCl0dKZr-x5iUM0Ej1R0"
bot = telebot.TeleBot(TOKEN)

# временное хранилище пользователей
user_data = {}

# ---------- БАЗА КОСМЕТИКИ (100+) ----------
# формат: (название, описание, бренд, категория)
COSMETICS = {
    "dry": [
        ("CeraVe Moisturizing Cream", "Питательный крем для сухой кожи 🌸", "CeraVe", "💰"),
        ("La Roche-Posay Lipikar Baume AP+", "Восстанавливает и успокаивает кожу 💧", "La Roche-Posay", "💎"),
        ("Avene Hydrance Riche", "Глубокое увлажнение и комфорт ✨", "Avene", "🪙"),
        ("Bioderma Atoderm Cream", "Защита кожного барьера 🌼", "Bioderma", "💎"),
        ("Weleda Skin Food", "Плотный крем для очень сухой кожи 🌿", "Weleda", "💰"),
        ("Eucerin UreaRepair 5%", "Смягчает и убирает стянутость", "Eucerin", "🪙"),
        ("Nivea Soft", "Лёгкий базовый крем", "Nivea", "💰"),
        ("Clinique Moisture Surge", "Интенсивное увлажнение 💦", "Clinique", "💎"),
        ("Embryolisse Lait-Creme", "Классика для сухой кожи", "Embryolisse", "🪙"),
        ("Librederm Cerafavit", "Восстанавливает кожу после стресса", "Librederm", "💰"),
        # добавляем ещё 20+
        ("Neutrogena Hydro Boost", "Увлажняет кожу и держит влагу 💧", "Neutrogena", "💰"),
        ("The Ordinary Natural Moisturizing", "Бюджетное увлажнение 🌸", "The Ordinary", "💰"),
        ("Vichy Aqualia Thermal", "Глубокое увлажнение 💦", "Vichy", "🪙"),
        ("SVR Hydraliane", "Комфорт коже", "SVR", "🪙"),
        ("Avène XeraCalm A.D", "Успокаивающее питание", "Avene", "💎"),
        ("La Roche-Posay Toleriane Rich", "Питание и комфорт 🌿", "La Roche-Posay", "🪙"),
        ("Kiehl’s Ultra Facial Cream", "Лёгкий крем для лица", "Kiehl’s", "💎"),
        ("Dr. Jart+ Ceramidin Cream", "Защита и восстановление", "Dr. Jart+", "💎"),
        ("Innisfree Green Tea Cream", "Увлажнение с антиоксидантами 🌱", "Innisfree", "💰"),
        ("Etude House Moistfull Collagen", "Питание и эластичность 💦", "Etude House", "🪙")
    ],
    "oily": [
        ("La Roche-Posay Effaclar Duo+", "Против прыщей и жирного блеска ✨", "La Roche-Posay", "💎"),
        ("CeraVe Foaming Cleanser", "Очищение без пересушивания", "CeraVe", "💰"),
        ("COSRX Low pH Cleanser", "Мягкое умывание 🌿", "COSRX", "💰"),
        ("The Ordinary Niacinamide 10%", "Контроль себума", "The Ordinary", "💰"),
        ("Bioderma Sebium", "Баланс жирной кожи", "Bioderma", "🪙"),
        ("SVR Sebiaclear", "Матирующий уход", "SVR", "🪙"),
        ("Clinique Anti-Blemish", "Для проблемной кожи", "Clinique", "💎"),
        ("Avene Cleanance", "Успокаивает кожу", "Avene", "💎"),
        ("Vichy Normaderm", "Сужает поры", "Vichy", "🪙"),
        ("Librederm Zinc", "Подсушивает воспаления", "Librederm", "💰"),
        # ещё 20+
        ("Neutrogena Visibly Clear", "Контроль жирности и прыщей", "Neutrogena", "💰"),
        ("Paula’s Choice BHA", "Отшелушивание и матирование", "Paula’s Choice", "💎"),
        ("Garnier Pure Active", "Доступный уход против прыщей", "Garnier", "💰"),
        ("La Roche-Posay Effaclar K+", "Матирующий уход 🌿", "La Roche-Posay", "🪙"),
        ("Innisfree Jeju Volcanic", "Матирование и очищение", "Innisfree", "💰"),
        ("COSRX Acne Pimple Master", "Локальная точечная помощь", "COSRX", "💰"),
        ("Kiehl’s Blue Herbal Spot", "Премиум точечное лечение 💎", "Kiehl’s", "💎"),
        ("Dr. Jart+ Ctrl-A", "Контроль себума и прыщей", "Dr. Jart+", "💎"),
        ("Etude House AC Clean Up", "Бюджетное решение 💰", "Etude House", "💰"),
        ("Vichy Normaderm Phytosolution", "Средний бюджет 🪙", "Vichy", "🪙")
    ],
    "combo": [
        ("CeraVe Moisturizing Lotion", "Баланс для комбинированной кожи", "CeraVe", "💰"),
        ("La Roche-Posay Toleriane", "Успокаивает чувствительную кожу", "La Roche-Posay", "💎"),
        ("Clinique Dramatically Different", "Поддержка баланса", "Clinique", "💎"),
        ("Bioderma Sensibio", "Для чувствительной кожи 🌸", "Bioderma", "🪙"),
        ("COSRX Snail Cream", "Восстановление и увлажнение", "COSRX", "💰"),
        ("Avene Hydrance Light", "Лёгкий крем", "Avene", "🪙"),
        ("Vichy Aqualia Thermal", "Увлажнение 💧", "Vichy", "🪙"),
        ("SVR Hydraliane", "Комфорт коже", "SVR", "🪙"),
        ("Librederm Hyaluronic", "Гиалуроновый уход", "Librederm", "💰"),
        ("Nivea Aqua Effect", "Освежающий крем", "Nivea", "💰"),
        # ещё 20+
        ("Neutrogena Hydro Boost Gel", "Лёгкий баланс увлажнения", "Neutrogena", "💰"),
        ("The Ordinary Natural Moisturizing", "Для комбинированной кожи 💧", "The Ordinary", "💰"),
        ("Kiehl’s Ultra Facial Oil-Free", "Баланс и контроль блеска", "Kiehl’s", "💎"),
        ("Innisfree Green Tea Balancing", "Лёгкий уход 🌱", "Innisfree", "💰"),
        ("Dr. Jart+ Ceramidin Lite", "Увлажнение без утяжеления 💎", "Dr. Jart+", "💎"),
        ("Etude House Moistfull Collagen", "Баланс и питание 🪙", "Etude House", "🪙"),
        ("Paula’s Choice RESIST", "Контроль блеска и покраснений 💎", "Paula’s Choice", "💎"),
        ("Vichy Normaderm Tri-Active", "Увлажнение и матирование 🪙", "Vichy", "🪙"),
        ("SVR Hydraliane Light", "Лёгкий комфорт 🪙", "SVR", "🪙"),
        ("Bioderma Hydrabio Light", "Баланс для комбинированной кожи 🌸", "Bioderma", "💎")
    ]
}

# ---------- СТАРТ ----------
@bot.message_handler(commands=["start"])
def start(message):
    user_data[message.chat.id] = {}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🌸 Сухая", "✨ Жирная", "🌼 Комбинированная")
    bot.send_message(
        message.chat.id,
        "Привет! 🌷\nДавай подберём косметику 💄\n\nВыбери тип кожи:",
        reply_markup=markup
    )

# ---------- ТИП КОЖИ ----------
@bot.message_handler(func=lambda m: m.text in ["🌸 Сухая", "✨ Жирная", "🌼 Комбинированная"])
def skin_type(message):
    skin_map = {"🌸 Сухая":"dry", "✨ Жирная":"oily", "🌼 Комбинированная":"combo"}
    user_data[message.chat.id]["skin"] = skin_map[message.text]
    ask_budget(message)

# ---------- ВЫБОР БЮДЖЕТА ----------
def budget_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("💰 Бюджет", "🪙 Средний", "💎 Премиум")
    return kb

def ask_budget(message):
    bot.send_message(
        message.chat.id,
        "Выбери свой бюджет 💵:",
        reply_markup=budget_keyboard()
    )
    bot.register_next_step_handler(message, budget_selected)

def budget_selected(message):
    if message.text not in ["💰 Бюджет", "🪙 Средний", "💎 Премиум"]:
        bot.send_message(message.chat.id, "Пожалуйста, выбери кнопку 💖")
        ask_budget(message)
        return
    user_data[message.chat.id]["budget"] = message.text
    ask_question_1(message)

# ---------- ВОПРОСЫ ----------
def yes_no_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("✅ Да", "❌ Нет")
    return kb

def ask_question_1(message):
    bot.send_message(
        message.chat.id,
        "Есть ли у тебя прыщики? 🌱",
        reply_markup=yes_no_keyboard()
    )
    bot.register_next_step_handler(message, q1)

def q1(message):
    user_data[message.chat.id]["acne"] = message.text
    bot.send_message(message.chat.id, "Кожа часто блестит? ✨", reply_markup=yes_no_keyboard())
    bot.register_next_step_handler(message, q2)

def q2(message):
    user_data[message.chat.id]["shine"] = message.text
    bot.send_message(message.chat.id, "Есть чувство стянутости? 🌸", reply_markup=yes_no_keyboard())
    bot.register_next_step_handler(message, q3)

def q3(message):
    user_data[message.chat.id]["tight"] = message.text
    bot.send_message(message.chat.id, "Кожа чувствительная? 🌼", reply_markup=yes_no_keyboard())
    bot.register_next_step_handler(message, result)

# ---------- РЕЗУЛЬТАТ ----------
def result(message):
    skin = user_data[message.chat.id]["skin"]
    budget = user_data[message.chat.id]["budget"]
    products = [p for p in COSMETICS[skin] if p[3]==budget]

    if not products:
        products = COSMETICS[skin]  # если нет по бюджету, выводим все

    random.shuffle(products)
    text = "✨ *Тебе подойдёт эта косметика:* ✨\n\n"
    for name, desc, brand, price in products[:10]:
        text += f"🌸 *{name}* ({brand}, {price})\n{desc}\n\n"

    bot.send_message(
        message.chat.id,
        text,
        parse_mode="Markdown",
        reply_markup=types.ReplyKeyboardRemove()
    )

# ---------- ЗАПУСК ----------
bot.infinity_polling()
