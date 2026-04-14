from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

TOKEN = "8722229628:AAEUWYHylzayNOLpk46hrHVEMmmH_naQRA8"

users = set()

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users.add(update.effective_user.id)

    keyboard = [
        [InlineKeyboardButton("📡 Server Check", callback_data='check')],
        [InlineKeyboardButton("ℹ️ Help", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🔥 Welcome to Advanced Bot 🔥\nChoose an option:",
        reply_markup=reply_markup
    )

# Help Command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start - Start bot\n/check <site> - Check server")

# Button Handler
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "help":
        await query.edit_message_text("Use /check example.com")

    elif query.data == "check":
        await query.edit_message_text("Send: /check google.com")

# Server Check Command
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text("Usage: /check example.com")
        return

    site = context.args[0]

    import requests
    try:
        r = requests.get(f"http://{site}", timeout=5)
        await update.message.reply_text(f"✅ {site} is UP\nStatus: {r.status_code}")
    except:
        await update.message.reply_text(f"❌ {site} is DOWN")

# Main
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("check", check))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()
