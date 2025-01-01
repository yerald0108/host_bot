import logging
import os
from bot.handlers import setup_handlers
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application
from telegram import BotCommand

# Cargar el archivo .env
load_dotenv()

# Obtener el token del bot desde el archivo .env
TOKEN = os.getenv('BOT_TOKEN')

# Configuración básica de logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Función para configurar los comandos del menú
async def set_bot_commands(application):
    commands = [
        BotCommand("start", "Iniciar el bot"),
        BotCommand("info", "Más infromación"),
        BotCommand("tutorial", "Como usar el bot"),
        
    ]
    await application.bot.set_my_commands(commands)

# Función principal para ejecutar el bot
def main():
    # Crear la aplicación del bot
    application = Application.builder().token(TOKEN).build()
    # Llama a los manejadores
    setup_handlers(application)

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()