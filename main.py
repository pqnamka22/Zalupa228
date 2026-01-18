import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart

TOKEN = "8238153006:AAGtGZnLt4SkSWnCCl0dKZr-x5iUM0Ej1R0"

bot = Bot(token=TOKEN)
dp = Dispatcher()

users = {}

COSMETICS = [
    ("CeraVe Hydrating Cleanser", ["dry", "sensitive"], "🌿 Мягкое очищение с церамидами"),
    ("CeraVe Foaming Cleanser", ["oily", "combo"], "🫧 Пенка для жирной кожи"),
    ("La Roche-Posay Effaclar Gel", ["oily"], "✨ Против акне"),
    ("Bioderma Sensibio Gel", ["sensitive"], "🌸 Без раздражения"),

    ("Pyunkang Yul Essence Toner", ["dry", "sensitive"], "💧 Увлажнение"),
    ("COSRX AHA/BHA Toner", ["oily", "combo"], "🧼 Поры"),
    ("Some By Mi Miracle Toner", ["oily"], "🌿 Антивоспалительный"),

    ("The Ordinary Niacinamide 10%", ["oily", "combo"], "✨ Себум"),
    ("The Ordinary Hyaluronic Acid", ["dry", "sensitive"], "💦 Увлажнение"),
    ("La Roche-Posay Hyalu B5", ["dry"], "🌷 Восстановление"),

    ("CeraVe Moisturizing Cream", ["dry", "sensitive"], "🧴 Барьер"),
    ("Neutrogena Hydro Boost", ["combo", "dry"], "💎 Гель-крем"),
    ("Effaclar Duo+", ["oily"], "🔥 Акне"),

    ("La Roche-Posay Anthelios SPF50", ["all"], "☀️ SPF"),
    ("Eucerin Oil Control SPF50", ["oily"], "🧊 Матирующий"),
] * 4


skin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🌸 Сухая"), KeyboardButton(text="✨ Жирная")],
        [KeyboardButton(text="🌿 Комбинированная"), KeyboardButton(text="💧 Чувствительная")]
    ],
    resize_keyboard=True
)

yes_no_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Да 🌼"), KeyboardButton(text="Нет 🌸")]],
    resize_keyboard=True
)


@dp.message(CommandStart())
async def start(msg: Message):
    users[msg.from_user.id] = {"step": 0}
    await msg.answer(
        "🌷 Привет!\n"
        "Я бьюти-ассистент 💄✨\n\n"
        "Отвечай на вопросы — я подберу уход 🌿",
        reply_markup=skin_kb
    )


@dp.message(F.text.in_(["🌸 Сухая", "✨ Жирная", "🌿 Комбинированная", "💧 Чувствительная"]))
async def set_skin(msg: Message):
    users[msg.from_user.id]["skin"] = {
        "🌸 Сухая": "dry",
        "✨ Жирная": "oily",
        "🌿 Комбинированная": "combo",
        "💧 Чувствительная": "sensitive",
    }[msg.text]
    users[msg.from_user.id]["step"] = 1
    await msg.answer("🌼 Есть ли высыпания?", reply_markup=yes_no_kb)


@dp.message(F.text.in_(["Да 🌼", "Нет 🌸"]))
async def questions(msg: Message):
    u = users[msg.from_user.id]
    step = u["step"]
    u["step"] += 1

    if step == 1:
        await msg.answer("💧 Есть ли стянутость?")
    elif step == 2:
        await msg.answer("✨ Есть ли жирный блеск?")
    elif step == 3:
        await show_result(msg)


async def show_result(msg: Message):
    skin = users[msg.from_user.id]["skin"]
    result = []

    for name, types, desc in COSMETICS:
        if skin in types or "all" in types:
            result.append((name, desc))
        if len(result) == 10:
            break

    text = "🌸 **Подборка для тебя** 💄\n\n"
    for i, (name, desc) in enumerate(result, 1):
        text += f"🌷 **{i}. {name}**\n{desc}\n\n"

    await msg.answer(text, parse_mode="Markdown")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
