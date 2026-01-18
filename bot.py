import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart

TOKEN = "8238153006:AAGtGZnLt4SkSWnCCl0dKZr-x5iUM0Ej1R0"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# -------------------- ХРАНЕНИЕ ДАННЫХ --------------------

users = {}

# -------------------- БАЗА КОСМЕТИКИ --------------------

COSMETICS = [
    # Очищение
    ("CeraVe Hydrating Cleanser", ["dry", "sensitive"], "🌿 Мягкое очищение с церамидами"),
    ("CeraVe Foaming Cleanser", ["oily", "combo"], "🫧 Пенка для жирной кожи"),
    ("La Roche-Posay Effaclar Gel", ["oily"], "✨ Против акне и жирного блеска"),
    ("Bioderma Sensibio Gel", ["sensitive"], "🌸 Без раздражения"),

    # Тоники
    ("Pyunkang Yul Essence Toner", ["dry", "sensitive"], "💧 Глубокое увлажнение"),
    ("COSRX AHA/BHA Toner", ["oily", "combo"], "🧼 Очищает поры"),
    ("Some By Mi Miracle Toner", ["oily"], "🌿 Антивоспалительный"),

    # Сыворотки
    ("The Ordinary Niacinamide 10%", ["oily", "combo"], "✨ Контроль себума"),
    ("The Ordinary Hyaluronic Acid", ["dry", "sensitive"], "💦 Интенсивное увлажнение"),
    ("La Roche-Posay Hyalu B5", ["dry"], "🌷 Восстановление кожи"),

    # Кремы
    ("CeraVe Moisturizing Cream", ["dry", "sensitive"], "🧴 Восстановление барьера"),
    ("Neutrogena Hydro Boost", ["combo", "dry"], "💎 Лёгкий гель-крем"),
    ("Effaclar Duo+", ["oily"], "🔥 Коррекция акне"),

    # SPF
    ("La Roche-Posay Anthelios SPF50", ["all"], "☀️ Защита от солнца"),
    ("Eucerin Oil Control SPF50", ["oily"], "🧊 Матирующий SPF"),
] * 4  # ~60 продуктов

# -------------------- КНОПКИ --------------------

skin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🌸 Сухая"), KeyboardButton(text="✨ Жирная")],
        [KeyboardButton(text="🌿 Комбинированная"), KeyboardButton(text="💧 Чувствительная")]
    ],
    resize_keyboard=True
)

yes_no_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Да 🌼"), KeyboardButton(text="Нет 🌸")]
    ],
    resize_keyboard=True
)

# -------------------- СТАРТ --------------------

@dp.message(CommandStart())
async def start(msg: Message):
    users[msg.from_user.id] = {"step": 0}
    await msg.answer(
        "🌷 Привет!\n"
        "Я твой бьюти-ассистент 💄✨\n\n"
        "Я задам несколько вопросов и подберу уход специально для тебя 🌿\n\n"
        "Выбери тип кожи 👇",
        reply_markup=skin_kb
    )

# -------------------- ТИП КОЖИ --------------------

@dp.message(F.text.in_(["🌸 Сухая", "✨ Жирная", "🌿 Комбинированная", "💧 Чувствительная"]))
async def skin(msg: Message):
    skin_map = {
        "🌸 Сухая": "dry",
        "✨ Жирная": "oily",
        "🌿 Комбинированная": "combo",
        "💧 Чувствительная": "sensitive"
    }
    users[msg.from_user.id]["skin"] = skin_map[msg.text]
    users[msg.from_user.id]["step"] = 1

    await msg.answer(
        "🌼 Есть ли высыпания или акне?",
        reply_markup=yes_no_kb
    )

# -------------------- ВОПРОСЫ --------------------

@dp.message(F.text.in_(["Да 🌼", "Нет 🌸"]))
async def questions(msg: Message):
    user = users.get(msg.from_user.id)
    if not user:
        return

    step = user["step"]
    user[f"q{step}"] = msg.text
    user["step"] += 1

    if step == 1:
        await msg.answer("💧 Есть ли ощущение стянутости после умывания?")
    elif step == 2:
        await msg.answer("✨ Часто появляется жирный блеск?")
    elif step == 3:
        await show_result(msg)

# -------------------- РЕЗУЛЬТАТ --------------------

async def show_result(msg: Message):
    skin = users[msg.from_user.id]["skin"]

    selected = []
    for name, types, desc in COSMETICS:
        if skin in types or "all" in types:
            selected.append((name, desc))
        if len(selected) == 10:
            break

    text = (
        "🌸 **Твоя персональная бьюти-подборка** 💄✨\n"
        "Я подобрал средства, которые подойдут твоей коже 🌿\n\n"
    )

    for i, (name, desc) in enumerate(selected, 1):
        text += (
            f"🌷 **{i}. {name}**\n"
            f"{desc}\n\n"
        )

    text += "💖 Используй уход регулярно и кожа будет сиять ✨"

    await msg.answer(text, parse_mode="Markdown")

# -------------------- ЗАПУСК --------------------

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
