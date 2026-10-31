from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import json, os

BOT_TOKEN = "9282829798:AAH5saLm0O6y5Tcnu0neTX6vcaARjLRiS2E"
DATA_FILE = "users.json"

def load_data():
    if not os.path.exists(DATA_FILE): return {}
    with open(DATA_FILE, "r") as f: return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = load_data()
    user_id = str(update.effective_user.id)
    name = update.effective_user.first_name
    
    if user_id not in users:
        users[user_id] = {"balance": 0, "refer": 0}
        # রেফার চেক
        if context.args:
            ref_id = context.args[0]
            if ref_id != user_id and ref_id in users:
                users[ref_id]["balance"] += 10
                users[ref_id]["refer"] += 1
                await context.bot.send_message(ref_id, f"🎉 নতুন রেফার! +10 টাকা। {name} তোমার লিংকে জয়েন করেছে।")
        save_data(users)

    link = f"https://t.me/{context.bot.username}?start={user_id}"
    text = f"হ্যালো {name} 👋\n\n💰 Refer & Earn Bot এ স্বাগতম\n\nতোমার রেফার লিংক:\n{link}\n\nপ্রতি রেফারে 10 টাকা।\n\nব্যালেন্স: {users[user_id]['balance']} টাকা\nরেফার: {users[user_id]['refer']} জন"

    keyboard = [[InlineKeyboardButton("👥 আমার রেফার লিংক", callback_data="my_link")],[InlineKeyboardButton("💰 ব্যালেন্স চেক", callback_data="bal")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    users = load_data()
    user_id = str(query.from_user.id)
    if user_id in users:
        if query.data == "bal":
            await query.answer(f"ব্যালেন্স: {users[user_id]['balance']} টাকা")
        if query.data == "my_link":
            link = f"https://t.me/{context.bot.username}?start={user_id}"
            await query.message.reply_text(f"তোমার লিংক:\n{link}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
print("Bot Running...")
app.run_polling()
