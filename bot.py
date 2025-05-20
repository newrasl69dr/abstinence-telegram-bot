import json
import datetime
import random
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = "7970596881:AAGMETGS2Rvcp5PhGvo57l09ODbbBQR19aU"
USER_ID = 918342062

DATA_FILE = "data.json"

MOTIVATIONS = [
    # ... твои мотивации ...
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

async def scheduled_send_motivation(bot):
    await send_motivation(bot)

async def scheduled_send_stat_request(bot):
    await send_stat_request(bot)

async def main():
    app = Application.builder().token(TOKEN).build()

    scheduler = AsyncIOScheduler()

    # Чтобы вызвать асинхронные функции из планировщика, обернём их в вызов задачи в asyncio
    scheduler.add_job(lambda: asyncio.create_task(scheduled_send_motivation(app.bot)), "cron", hour=19, minute=0)
    scheduler.add_job(lambda: asyncio.create_task(scheduled_send_stat_request(app.bot)), "cron", hour=23, minute=30)

    scheduler.start()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_response))

    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
