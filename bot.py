import json
import datetime
import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# 🔐 ЖЁСТКО ЗАДАННЫЕ ДАННЫЕ
TOKEN = "7970596881:AAGMETGS2Rvcp5PhGvo57l09ODbbBQR19aU"
USER_ID = 918342062

if not TOKEN or not USER_ID:
    raise ValueError("BOT_TOKEN и USER_ID должны быть заданы как переменные среды.")

USER_ID = int(USER_ID)

DATA_FILE = "data.json"

MOTIVATIONS = [
    "Ты сильнее, чем кажется.",
    "Каждый день — новый шанс стать лучше.",
    "Сила в постоянстве.",
    "Ты не один в этом пути.",
    "Срыв — это не поражение, а урок.",
    "Сегодня — идеальный день не сдаваться.",
    "Каждый правильный шаг — победа.",
    "Ты управляешь своей жизнью.",
    "Твоя сила растёт каждый день.",
    "Ты можешь всё, если не сдашься.",
    "Ничто не стоит твоей энергии, кроме мечты.",
    "Воздержание — путь к свободе.",
    "Победа — это продолжать идти.",
    "Сдержанность — это сила.",
    "Маленькие шаги создают большие перемены.",
    "Ты заслуживаешь лучшего.",
    "Прошлое не определяет тебя.",
    "Ты выбираешь быть лучшей версией себя.",
    "Каждое утро — новый старт.",
    "Настоящая сила — в самообладании.",
    "Ты уже преодолел многое — не останавливайся.",
    "Внутри тебя — огромная сила.",
    "Ты пример для будущего себя.",
    "Один день без срыва — это уже успех.",
    "Мотивация приходит и уходит. Дисциплина — ключ.",
    "Ты не проиграешь, пока не сдашься.",
    "Контроль над собой — это суперсила.",
    "Ты на правильном пути.",
    "Сила — это выбор каждый день.",
    "Каждый день без срыва — кирпич в стене успеха.",
    "Ты борешься за самого себя.",
    "Ты заслуживаешь спокойствия.",
    "Твоя жизнь — в твоих руках.",
    "Победа — в последовательности.",
    "Один день за раз — и ты победишь.",
    "Ты уже делаешь невозможное.",
    "Сегодня ты стал сильнее, чем вчера.",
    "Ничего не менять — значит проигрывать.",
    "Сдержанность — это любовь к себе.",
    "Ты хозяин своей воли.",
    "Будь терпелив — результат будет.",
    "Сила растёт через сопротивление.",
    "Ты уже победитель, если не сдаёшься.",
    "Ты живёшь ради своей цели.",
    "Мир принадлежит тем, кто себя контролирует.",
    "Ты победишь, если продолжишь.",
    "Жизнь без зависимости — жизнь настоящая.",
    "Не давай слабости управлять.",
    "Каждый день — вклад в будущее.",
    "Ты не один. Верь в себя.",
    "Ты стал сильнее, чем думаешь.",
    "Будущее — в твоих руках.",
    "Сложно? Значит, ты растёшь.",
    "Каждое «нет» делает тебя сильнее.",
    "Настоящее «да» — это отказ от ложных удовольствий.",
    "Ты создаёшь нового себя.",
    "Жизнь без срывов — это реальность.",
    "Вставай и иди дальше.",
    "С каждым днём — ближе к свободе.",
    "Ты борешься — ты победишь.",
    "Ради себя. Ради будущего.",
    "Один день без срыва — уже подвиг.",
    "Ты — главный герой своей истории.",
    "Сильный — это тот, кто не сдаётся.",
    "Ты сильнее привычек.",
    "Ты держишь удар.",
    "Каждая победа начинается с отказа.",
    "Твоя сила — в постоянстве.",
    "Не сдавайся. Это пройдёт.",
    "Каждый день ты доказываешь свою силу.",
    "Сейчас — важнее всего.",
    "Будь тем, кем хочешь стать."
]

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {"start_date": None, "days": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_day_number(start_date):
    today = datetime.date.today()
    delta = today - datetime.date.fromisoformat(start_date)
    return delta.days + 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != USER_ID:
        return
    data = load_data()
    if not data["start_date"]:
        data["start_date"] = str(datetime.date.today())
        save_data(data)
        await update.message.reply_text("📅 Отсчёт начат с сегодняшнего дня.")
    else:
        await update.message.reply_text("📅 Отсчёт уже начат.")

async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != USER_ID:
        return
    text = update.message.text
    today = str(datetime.date.today())
    data = load_data()
    data["days"].append({"date": today, "response": text})
    save_data(data)
    await update.message.reply_text("✅ Ответ сохранён.")

# Обновлено: используем bot напрямую
async def send_motivation(bot):
    message = random.choice(MOTIVATIONS)
    await bot.send_message(chat_id=USER_ID, text=f"💪 {message}")

async def send_stat_request(bot):
    data = load_data()
    if not data["start_date"]:
        return
    day_number = get_day_number(data["start_date"])
    text = f"""📅 День: {day_number}
🧠 Срыв: (да/нет)
🛏 Сон до 23:30: (да/нет)"""
    await bot.send_message(chat_id=USER_ID, text=text)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != USER_ID:
        return
    data = load_data()
    total = len(data["days"])
    no_fails = sum(1 for d in data["days"] if "нет" in d["response"].lower())
    week_data = [d for d in data["days"] if datetime.date.fromisoformat(d["date"]) >= datetime.date.today() - datetime.timedelta(days=7)]
    month_data = [d for d in data["days"] if datetime.date.fromisoformat(d["date"]).month == datetime.date.today().month]

    await update.message.reply_text(
        f"📊 Всего дней: {total}\n"
        f"✅ Без срывов: {no_fails}\n"
        f"📆 За неделю: {len(week_data)}\n"
        f"📅 За месяц: {len(month_data)}"
    )

def main():
    app = Application.builder().token(TOKEN).build()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_motivation, "cron", hour=19, minute=0, args=[app.bot])
    scheduler.add_job(send_stat_request, "cron", hour=23, minute=30, args=[app.bot])
    scheduler.start()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_response))

    app.run_polling()

if __name__ == "__main__":
    main()
