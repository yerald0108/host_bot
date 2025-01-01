from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, filters
from bot.utils import start, manejar_autorizacion, recibir_captura, mensaje_error, mas_informacion, tutorial
from bot.button_handlers import button_handler

def setup_handlers(application):
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("info", mas_informacion))
    application.add_handler(CommandHandler("tutorial", tutorial))
    application.add_handler(CallbackQueryHandler(manejar_autorizacion, pattern=r"^(aprobar|rechazar):\d+$"))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.PHOTO, recibir_captura))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mensaje_error))

