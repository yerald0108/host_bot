import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext
from datetime import datetime

load_dotenv()
MY_ID = os.getenv("MY_ID")

solicitudes_pendientes = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name or "Usuario"
    welcome_message = (
        f"✨👋 ¡Hola <b>{user_name}</b>! ¡Bienvenido a <b>Empleos Bot</b>! 🎉\n\n"
        "🔑 Aquí te ofrecemos acceso exclusivo a oportunidades laborales increíbles en <b>La Habana</b>. 💼\n\n"
        "🌟 Si estás listo para comenzar, haz clic en el botón <b>Comenzar</b> a continuación.\n\n"
        "👉 <i>Recuerda, las oportunidades no esperan. ¡No te quedes fuera!</i> 🚀"
    )
    keyboard = [
        [InlineKeyboardButton("Comenzar 🆗", callback_data="mostrar")],
        [InlineKeyboardButton("Más Información 💭", callback_data="mas_informacion")],
        [InlineKeyboardButton("Como usar el bot 🤖", callback_data="tutorial")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Verificar si el update es de tipo mensaje o callback_query
    if update.message:
        # Si es un mensaje, usamos reply_html
        await update.message.reply_html(welcome_message, reply_markup=reply_markup)
    elif update.callback_query:
        # Si es un callback_query, editamos el mensaje o enviamos la respuesta
        await update.callback_query.answer()  # Responde al callback
        await update.callback_query.edit_message_text(welcome_message, reply_markup=reply_markup, parse_mode="HTML")

async def mas_informacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        info_message = (
            "🌟✨ <b>¿Por qué elegir <u>Empleos Bot</u>?</b> ✨🌟\n\n"
            "📈 <b>¡Impulsa tu carrera profesional!</b>\n"
            "🔍 Accede a oportunidades exclusivas que te conectan con los mejores empleos. 💼\n\n"
            "🎯 <b>Fácil y rápido:</b>\n"
            "👉 En un solo lugar, encuentra ofertas adaptadas a ti.\n\n"
            "🤝 <b>Conexiones que importan:</b>\n"
            "🔗 Únete a redes de empresas y profesionales listos para contratar. 🚀\n\n"
            "💡 <b>Consejos y recursos:</b>\n"
            "📝 Aprende a destacar en el mercado laboral con las mejores herramientas. 🌟\n\n"
            "💪 <i>¡Es hora de alcanzar tus metas y construir el futuro que mereces!</i> 🏆\n\n"
            "👉 <b>Empleos Bot está aquí para ayudarte. ¡Tu próximo empleo te espera!</b> 🌈"
        )

        # Crear botón "Volver Atrás"
        keyboard = [
            [InlineKeyboardButton("🔙 Volver Atrás", callback_data="volver_inicio")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Responder al usuario con el mensaje y el botón
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            info_message, reply_markup=reply_markup, parse_mode="HTML"
        )
        
async def mostrar_metodos_pago(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:

        keyboard = [
            [InlineKeyboardButton("1️⃣ Pagar por transferencia", callback_data="pagar_transferencia")],
            [InlineKeyboardButton("2️⃣ Pagar por saldo", callback_data="pagar_saldo")],
            [InlineKeyboardButton("Volver atrás 🔙", callback_data="volver_inicio_start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        message_text = (
            "💳 <b>Para entrar al grupo de WhatsApp:</b>\n\n"
            "1️⃣ Realiza un pago de <b>100 pesos</b> mediante transferencia bancaria.\n\n"
            "2️⃣ O puede pagar <b>200 pesos</b> usando saldo.\n\n"
            "✨ Elige tu método de pago preferido para continuar."
        )

        if update.callback_query:
            # Editar el mensaje existente si es posible
            if update.callback_query.message and update.callback_query.message.text:
                await update.callback_query.edit_message_text(
                    text=message_text,
                    reply_markup=reply_markup,
                    parse_mode="HTML"
                )
            else:
                # Enviar un nuevo mensaje si no se puede editar
                await update.callback_query.message.reply_text(
                    text=message_text,
                    reply_markup=reply_markup,
                    parse_mode="HTML"
                )
            # Responder al callback para evitar problemas de timeout
            await update.callback_query.answer()
        else:
            # En caso de que sea un mensaje normal y no un callback
            await update.message.reply_text(
                text=message_text,
                reply_markup=reply_markup,
                parse_mode="HTML"
            )
    except Exception as e:
        print(f"Error en la función mostrar_metodos_pago: {e}")

async def pagar_transferencia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        cuenta_bancaria = os.getenv("CUENTA_BANCARIA", "9227959873757970")
        telefono_confirmacion = os.getenv("TELEFONO_CONFIRMACION", "56835698")

        # Crear los botones interactivos
        keyboard = [
            [InlineKeyboardButton("Estoy de acuerdo ✅", callback_data="aceptar_pago")],
            [InlineKeyboardButton("Volver atrás 🔙", callback_data="volver_metodos_pago")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Si el callback_query está presente, editamos el mensaje original
        if update.callback_query:
            if update.callback_query.message and update.callback_query.message.text:
                # Editar el mensaje con los detalles de pago
                await update.callback_query.edit_message_text(
                    text=(
                        f"🏦 <b>Por favor realiza el pago a los siguientes datos:</b>\n\n"
                        f"💳  <b>Transferir a:</b> <code>{cuenta_bancaria}</code>\n\n"
                        f"📲 <b>Confirmar a:</b> <code>{telefono_confirmacion}</code>\n\n"
                        "📝 <i>Nota:</i> Mantén presionado para copiar los números \n\n"
                        "🛎 <b>Importante:</b> Marcar la opción confirmar móvil.\n\n"
                        "⚠️ <b>Cualquier uso indebido de esta información tendrá graves consecuencias.</b> ⚖️"
                    ),
                    parse_mode="HTML",
                    reply_markup=reply_markup
                )
            else:
                # Si no se puede editar el mensaje, enviamos uno nuevo (aunque esto no debería ocurrir)
                await update.callback_query.message.reply_text(
                    text="Hubo un problema al editar el mensaje.",
                    reply_markup=reply_markup,
                    parse_mode="HTML"
                )
            # Responder al callback para evitar problemas de timeout
            await update.callback_query.answer()
    except Exception as e:
        print(f"Error en la función pagar_por_transferencia: {e}")

async def pagar_por_saldo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query  # Asegura que obtienes el callback correctamente

    # Mensaje para pagar por saldo
    mensaje = (
        "💰 <b>Pagar por Saldo</b>\n\n"
        "Para pagar por saldo, transfiere al siguiente número: \n\n"
        "📞 <code>56835698</code>\n\n"
        "📝 <i>Nota:</i> Mantén presionado para copiar el número \n\n"
        "✅ Presione el botón <b>Estoy de Acuerdo</b> para continuar"
    )

    # Definir los botones para el usuario
    keyboard = [
        [InlineKeyboardButton("✅ Estoy de Acuerdo", callback_data="aceptar_pago_saldo")],  # Callback manejado
        [InlineKeyboardButton("🔙 Volver Atrás", callback_data="volver_metodos_pago")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Editar el mensaje de los métodos de pago
    await query.message.edit_text(
        mensaje,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

    # Responder al callback para evitar el timeout
    await query.answer()

async def recibir_captura_saldo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    user = update.message.from_user
    chat_id = user.id
    username = user.username or "Usuario desconocido"
    foto = update.message.photo[-1]  # Toma la foto de mayor resolución disponible
    
    # Obtener la fecha y hora actual
    fecha_actual = datetime.now().strftime("%d/%m/%Y")  # Formato: Día/Mes/Año
    
    # Reenvía la captura al creador del bot
    creador_id = MY_ID  # Cambia por tu ID de chat
    mensaje = (
        f"📸 <b>Captura de Pago por Saldo</b>\n\n"
        f"👤 <b>Usuario:</b> @{username}\n"
        f"🆔 <b>ID:</b> {chat_id}\n"
        f"📅 <b>Fecha:</b> {fecha_actual}\n\n"
        "Por favor, revisa y responde si aceptas o rechazas el pago."
    )
    botones = [
        [
            InlineKeyboardButton("✅ Aprobar", callback_data=f"aprobar:{chat_id}"),
            InlineKeyboardButton("❌ Rechazar", callback_data=f"rechazar:{chat_id}"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(botones)
    await context.bot.send_photo(chat_id=creador_id, photo=foto.file_id, caption=mensaje, reply_markup=reply_markup, parse_mode="HTML")

    # Confirmación al usuario
    await update.message.reply_text("📸 <b>¡Captura recibida!</b>\n\n"
                                    "Gracias por enviarla, estamos revisando tu pago. Por favor, espera nuestra confirmación.",
                                    parse_mode="HTML")

async def recibir_captura(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    username = user.username if user.username else "Sin nombre de usuario"
    user_id = user.id
    chat_id = update.message.chat.id

    # Verificar si el mensaje contiene una foto
    if not update.message.photo:
        await update.message.reply_text(
            "❌ <b>Error:</b> Solo se acepta una captura de pantalla como imagen.\n\n"
            "📸 <i>Por favor, envía una captura de pantalla que cumpla con los siguientes requisitos:</i>\n\n"
            "1. ⏰ <b>La hora debe ser visible.</b>\n\n"
            "2. 🖼 <b>No debe estar recortada ni editada.</b>\n\n"
            "3. 📜 <b>Debe mostrar claramente los detalles del pago.</b>\n\n"
            "🙌 Gracias por tu cooperación.",
            parse_mode="HTML"
        )
        return  # Detenemos el flujo hasta recibir una imagen

    # Si se recibe una foto, se almacena y se continúa el flujo normal
    solicitudes_pendientes[user_id] = {
        "chat_id": chat_id,
        "username": username,
        "photo_id": update.message.photo[-1].file_id  # Se guarda la foto en el diccionario
    }

    # Obtener la fecha actual
    fecha_actual = datetime.now().strftime("%d/%m/%Y")  # Formato: Día/Mes/Año
    
    # Crear un teclado para que el administrador apruebe o rechace la captura
    caption = (
        f"📤 <b>Nueva captura recibida</b>\n\n"
        f"👤 <b>Usuario:</b> {username}\n"
        f"🆔 <b>ID:</b> {user_id}\n"
        f"📅 <b>Fecha:</b> {fecha_actual}\n\n"
        "📋 <i>Por favor, revisa la imagen para confirmar que cumple con los requisitos.</i>"
    )
    keyboard = [
        [InlineKeyboardButton("Aprobar ✅", callback_data=f"aprobar:{user_id}")],
        [InlineKeyboardButton("Rechazar ❌", callback_data=f"rechazar:{user_id}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        # Enviar la foto al creador para su aprobación
        await context.bot.send_photo(
            chat_id=MY_ID,
            photo=update.message.photo[-1].file_id,
            caption=caption,
            parse_mode="HTML",
            reply_markup=reply_markup
        )
        await update.message.reply_text(
            "📤 <b>Tu comprobante ha sido enviado para revisión.</b>\n\n"
            "⏳ Te notificaremos pronto sobre el estado de tu solicitud.",
            parse_mode="HTML"
        )
    except Exception as e:
        await update.message.reply_text("⚠️ Se está presentando problemas en la conexión.")
        print(f"Error al enviar la foto: {e}")
        
# Manejo de aprobación/rechazo
async def manejar_autorizacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    try:
        # Verificar que el dato en el callback es válido
        action, user_id = query.data.split(":")
        user_id = int(user_id)

        # Verificar si el usuario existe en las solicitudes pendientes
        if user_id not in solicitudes_pendientes:
            await query.answer("La solicitud ya no está disponible.", show_alert=True)
            print(f"User ID {user_id} no encontrado en solicitudes_pendientes.")
            return

        # Obtener datos de la solicitud
        solicitud = solicitudes_pendientes.pop(user_id)
        chat_id = solicitud["chat_id"]
        username = solicitud["username"]

        # Enlace del grupo de WhatsApp
        whatsapp_link = "https://chat.whatsapp.com/BJdVwIrcdd756HDe2JG1Hk"

        if action == "aprobar":
            mensaje = (
                f"✅ ¡Tu solicitud ha sido aprobada, <b>{username}</b>! 🎉\n\n"
                f"¡Estás listo para unirte a nuestro grupo de WhatsApp! 😊\n\n"
                f"Puedes unirte al grupo haciendo clic en el siguiente enlace:\n"
                f"{whatsapp_link}\n\n"
                "¡Te esperamos! 🙌"
            )
            await context.bot.send_message(chat_id=chat_id, text=mensaje, parse_mode="HTML")
            await query.edit_message_caption(f"Solicitud de {username} aprobada. ✅")
            await query.answer("Solicitud aprobada correctamente.")
        elif action == "rechazar":
            mensaje_rechazo = (
                f"❌ Lamentablemente, tu solicitud de pago fue rechazada, <b>{username}</b>.\n\n"
                "No te preocupes, ¡puedes intentarlo de nuevo! 🧐💪\n\n"
                "Por favor verifica que el pago haya sido realizado correctamente y que hallas cumplido con los requisitos de la captura de pantalla.\n\n "
                "<b>¡Estamos aquí para ayudarte! 😊</b>"
            )
            await context.bot.send_message(chat_id=chat_id, text=mensaje_rechazo, parse_mode="HTML")
            await query.edit_message_caption(f"Solicitud de {username} rechazada. ❌")
            await query.answer("Solicitud rechazada correctamente.")
        else:
            await query.answer("Acción no válida.")
    except Exception as e:
        print(f"Error en manejar_autorizacion: {e}")
        await query.answer("Se está presentando problemas en la conexión.", show_alert=True)

async def manejar_mensajes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❗ Por favor, utiliza los botones proporcionados para interactuar con el bot. 😊",
        parse_mode="HTML"
    )

async def mensaje_error(update: Update, context: CallbackContext):
    user = update.effective_user
    # Enviar mensaje de error con emojis
    error_message = (
        "🚫❌ ¡Ups! No es necesario escribir nada, por favor sigue las instrucciones. 👇👀\n"
        "📋 Si tienes alguna duda, por favor consulta las opciones del menú. 💬\n"
        "🙌 Gracias por tu cooperación. 😄"
    )
    await update.message.reply_text(error_message)
    
async def tutorial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tutorial_message = (
        "📚 <b>¡Bienvenido al tutorial de <u>Empleos Bot</u>! 🤖</b>\n\n"
        "🔹 <b>¿Cómo usar el bot?</b>\n"
        "1️⃣ No necesitas escribir nada en el teclado, todo se maneja a través de botones.\n"
        "2️⃣ Simplemente toca los botones que aparecen en la pantalla para navegar por las opciones.\n\n"
        "🔹 <b>Opciones disponibles:</b>\n"
        "🔘 <b>Comenzar:</b> Inicia el proceso para acceder a las oportunidades laborales.\n"
        "🔘 <b>Más Información:</b> Descubre más sobre los beneficios de usar <b>Empleos Bot</b>.\n"
        "🔘 <b>Como usar el bot:</b> Aquí estás, aprendiendo cómo interactuar con nosotros.\n\n"
        "💡 <b>Recuerda:</b> ¡Todo está diseñado para que sea lo más fácil posible! 😊\n"
        "👉 Simplemente selecciona una opción y el bot te guiará paso a paso sin necesidad de escribir. 🚀"
    )

    # Crear botón "Volver Atrás"
    keyboard = [
        [InlineKeyboardButton("🔙 Volver Atrás", callback_data="volver_inicio")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Verificar si el update es de tipo mensaje o callback_query
    if update.message:
        # Si es un mensaje, usamos reply_html
        await update.message.reply_html(tutorial_message, reply_markup=reply_markup)
    elif update.callback_query:
        # Si es un callback_query, editamos el mensaje o enviamos la respuesta
        await update.callback_query.answer()  # Responde al callback
        await update.callback_query.edit_message_text(tutorial_message, reply_markup=reply_markup, parse_mode="HTML")
