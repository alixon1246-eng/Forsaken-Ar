import json
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Загрузка карточек
with open("cards.json", "r", encoding="utf-8") as f:
    cards = json.load(f)

# Вероятности выпадения
rarity_chances = {
    "Обычная": 50,
    "Редкая": 30,
    "Эпическая": 15,
    "Мифическая": 4,
    "Легендарная": 1
}

# Загрузка базы пользователей
try:
    with open("users.json", "r", encoding="utf-8") as f:
        users = json.load(f)
except FileNotFoundError:
    users = {}

# Функция выдачи карточки
def get_card():
    roll = random.randint(1, 100)
    cumulative = 0
    for rarity, chance in rarity_chances.items():
        cumulative += chance
        if roll <= cumulative:
            possible_cards = [c for c in cards if c["rarity"] == rarity]
            return random.choice(possible_cards)

# Команда получения карточки
async def get(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    card = get_card()
    
    # Добавление карточки в коллекцию пользователя
    if user_id not in users:
        users[user_id] = []
    users[user_id].append(card)
    
    # Сохранение базы
    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)
    
    await update.message.reply_text(
        f"✨ Вы получили карточку! ✨\n\n"
        f"Имя: {card['name']}\n"
        f"Редкость: {card['rarity']}"
    )

# Команда просмотра коллекции
async def collection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id not in users or not users[user_id]:
        await update.message.reply_text("У вас пока нет карточек!")
        return
    
    text = "🎴 Ваша коллекция:\n\n"
    for c in users[user_id]:
        text += f"{c['name']} - {c['rarity']}\n"
    
    await update.message.reply_text(text)

# Основной запуск бота
if name == "__main__":
    TOKEN = "8257598316:AAFZXQVulpqFb84VrBWlVX8YjxNou_YVJtw"
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("Fors", get))
    app.add_handler(CommandHandler("collection", collection))
    
    print("Бот запущен...")
    app.run_polling()