from aiogram import Bot, Dispatcher, types
import asyncio

BOT_TOKEN = "8196057136:AAE8oQ4oaQVZfCusSAK-PYXNqVSNW2YsTTY"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message()
async def handle_message(message: types.Message):
    # Обрабатываем игровые эмодзи (кости, дартс и т.д.)
    if message.dice:
        dice = message.dice
        await analyze_game_result(message, dice)

    # Обычные эмодзи
    elif message.text:
        text = message.text

        if text.isdigit():
            try:
                emoji = chr(int(text))
                await message.answer(emoji)
            except (ValueError, OverflowError):
                pass
        else:
            for char in text:
                if is_emoji(char):
                    await message.answer(f"{char} - {ord(char)}")


async def analyze_game_result(message, dice):
    emoji = dice.emoji
    value = dice.value

    response = f"🎮 Анализ игры:\n"
    response += f"Эмодзи: {emoji}\n"
    response += f"Значение: {value}\n"
    response += f"Тип: {get_dice_type(emoji)}\n\n"

    # Анализ по типам игр
    if emoji == "🎲":  # Кости
        response += analyze_dice(value)
    elif emoji == "🎯":  # Дартс
        response += analyze_darts(value)
    elif emoji == "🏀":  # Баскетбол
        response += analyze_basketball(value)
    elif emoji == "⚽️":  # Футбол
        response += analyze_football(value)
    elif emoji == "🎳":  # Боулинг
        response += analyze_bowling(value)

    await message.answer(response)


def analyze_dice(value):
    analysis = "🎲 Кости:\n"

    # Больше/Меньше
    if value in [4, 5, 6]:
        analysis += "🔴 Больше (4-5-6)\n"
    else:
        analysis += "🔵 Меньше (1-2-3)\n"

    # Четное/Нечетное
    if value % 2 == 0:
        analysis += "🔴 Четное\n"
    else:
        analysis += "🔵 Нечетное\n"

    # Конкретное число
    analysis += f"🎯 Число: {value}\n"

    return analysis


def analyze_darts(value):
    analysis = "🎯 Дартс:\n"
    if value == 1:
        analysis += "🎯 Мимо - 2.5x\n"
    elif value == 2:
        analysis += "🎯 Красное - 1.8x\n"
    elif value == 3:
        analysis += "🎯 Белое - 1.8x\n"
    elif value == 4:
        analysis += "🎯 Красное - 1.8x\n"
    elif value == 5:
        analysis += "🎯 Белое - 1.8x\n"
    elif value == 6:
        analysis += "🎯 Центр - 2.5x\n"
    return analysis


def analyze_basketball(value):
    analysis = "🏀 Баскетбол:\n"
    if value in [4, 5]:  # Гол
        analysis += "✅ Гол - 1.8x\n"
    else:  # Мимо (1-3)
        analysis += "❌ Мимо - 1.3x\n"
    return analysis


def analyze_football(value):
    analysis = "⚽️ Футбол:\n"
    if value in [4, 5]:  # Гол
        analysis += "✅ Гол - 1.3x\n"
    else:  # Мимо (1-3)
        analysis += "❌ Мимо - 1.8x\n"
    return analysis


def analyze_bowling(value):
    analysis = "🎳 Боулинг:\n"

    if value == 1:
        analysis += "❌ Мимо - 0 кеглей\n"
    elif value == 2:
        analysis += "🎯 1 кегля\n"
    elif value == 3:
        analysis += "🎯 3 кегли\n"
    elif value == 4:
        analysis += "🎯 4 кегли\n"
    elif value == 5:
        analysis += "🎯 5 кеглей\n"
    elif value == 6:
        analysis += "🎳 Страйк! 6 кеглей 🎳\n"

    return analysis

def get_dice_type(emoji):
    types = {
        "🎲": "Dice (1-6)",
        "🎯": "Darts (1-6)",
        "🏀": "Basketball (1-5)",
        "⚽️": "Football (1-5)",
        "🎳": "Bowling (1-6)",
    }
    return types.get(emoji, "Unknown")


def is_emoji(char):
    code = ord(char)
    return (0x1F600 <= code <= 0x1F64F) or \
        (0x1F300 <= code <= 0x1F5FF) or \
        (0x1F680 <= code <= 0x1F6FF) or \
        (0x1F900 <= code <= 0x1F9FF) or \
        (0x2600 <= code <= 0x26FF) or \
        (0x2700 <= code <= 0x27BF)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
