TELEGRAM_TOKEN = "8361243003:AAEkkPW197WYeSApN1CuCTvIrigr-13EzCI"
ADMIN_CHAT_ID = "5400588836"
import os
import logging
from telegram import Update, InputMediaPhoto
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get(TELEGRAM_TOKEN)  # set this in your environment
ADMIN_CHAT_ID = int(os.environ.get("5400588836", 0))  # set admin id or leave 0 to print and set later

# Optionally restrict allowed senders (set allowed user IDs as ints)
ALLOWED_SENDERS = None  # e.g. {123456789, 987654321} or None to allow everyone

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    await update.message.reply_text("ሰላም፣ ለመመዝገብ 350 ብር በቴሌ ብር ___ ፣ በንግድ ባንክ ቁጥር____ ክፍያዎን ይፈጽሙ። ክፍያውን የፈጸማቹበትን የሚያሳይ ምስል ከላይ ለናሙና በተቀመጠው ምስል መሰረት በዚህ ቦት ይላኩ።")
    # logger.info("Start from user %s (%s). chat_id=%s", user.username, user.id, chat_id)
    # If ADMIN_CHAT_ID is not configured, print the id so you can copy it
    if ADMIN_CHAT_ID != 0:
        await update.message.reply_text(f"ADMIN_CHAT_ID is: 5400588836. Your chat id is: {chat_id}")
        logger.info("Detected chat id: %s", chat_id)

async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    sender_id = update.effective_user.id
    if ALLOWED_SENDERS is not None and sender_id not in ALLOWED_SENDERS:
        await message.reply_text("You are not allowed to use this bot.")
        return

    if not message.caption:
        await message.reply_text("enter ur name as a caption under the screenshot")
        return

    # Get the highest resolution photo (last in list)
    photo = message.photo[-1]
    file_id = photo.file_id
    caption = message.caption or ""
    admin_id = "5400588836"
    if admin_id == 0:
        await message.reply_text("Admin chat id not set on the bot. Ask the admin to send /start.")
        return

    # Option A: forward original message (keeps sender info in forwarded message)
    try:
        await context.bot.forward_message(chat_id=admin_id,
                                          from_chat_id=message.chat_id,
                                          message_id=message.message_id)
    except Exception as e:
        logger.exception("Forward failed; fallback to send_photo")
        # Option B: send the photo by file_id (will not look like a forward)
        await context.bot.send_photo(chat_id=admin_id, photo=file_id, caption=f"From @{update.effective_user.username or update.effective_user.id}\n{caption}")

    # confirm to user
    await message.reply_text("Thanks — your screenshot was forwarded to the admin.")

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Optional: allow users to send /id request
    await update.message.reply_text("Please send a screenshot image with ur name on the caption to forward to the admin. for better understanding see the above bot picture to know about the format")

def main():
    if TELEGRAM_TOKEN is None:
        raise RuntimeError("Please set TELEGRAM_TOKEN environment variable")
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, photo_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    logger.info("Bot starting (polling)...")
    application.run_polling()

if __name__ == "__main__":
    main()
