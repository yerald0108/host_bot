from telegram import Update
from telegram.ext import ContextTypes
from bot.utils import start ,mostrar_metodos_pago, mas_informacion, pagar_transferencia, pagar_por_saldo, tutorial


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if not query:
        return

    data = query.data
    print(f"Callback data recibido: {data}")
    
    if data == "mostrar":
        await mostrar_metodos_pago(update, context)
    elif data == "mas_informacion":
        await mas_informacion(update, context)
    elif data == "tutorial":
        await tutorial(update, context)
    elif data in ["volver_inicio", "volver_inicio_info", "volver_inicio_start"]:
        await start(update, context)
    elif data == "volver_metodos_pago":
        await mostrar_metodos_pago(update, context)
    elif data == "pagar_transferencia":
        await pagar_transferencia(update, context)
    elif data == "pagar_saldo":
        await pagar_por_saldo(update, context)
    elif data == "aceptar_pago":  # Aquí debes agregar el manejo de aceptar_pago
        await query.message.reply_text(
            "✅ ¡Has aceptado el pago por transferencia!\n\n"
            "📸 <b>Por favor, envía la captura de pantalla del pago por transferencia.</b>\n\n"
            "✅ <i>Asegúrate de que la captura de pantalla cumpla con los siguientes requisitos:</i>\n\n"
            "1️⃣ ⏰ <b>La hora debe ser visible.</b>\n\n"
            "2️⃣ 🖼 <b>No recortes ni edites la imagen.</b>\n\n"
            "3⃣ 📜 <b>Debe mostrar claramente los detalles del pago.</b>\n\n"
            "⏳ <i>Envía ahora la captura para que podamos verificarla.</i>",
            parse_mode="HTML"
        )
    elif data == "aceptar_pago_saldo":  # Aquí manejamos aceptar_pago_saldo
        await query.message.reply_text(
            "📸 <b>Por favor, envía la captura de pantalla del pago por saldo.</b>\n\n"
            "✅ <i>Asegúrate de que la captura de pantalla cumpla con los siguientes requisitos:</i>\n\n"
            "1️⃣ ⏰ <b>La hora debe ser visible.</b>\n\n"
            "2️⃣ 🖼 <b>No recortes ni edites la imagen.</b>\n\n"
            "3⃣ 📜 <b>Debe mostrar claramente los detalles del pago.</b>\n\n"
            "⏳ <i>Envía ahora la captura para que podamos verificarla.</i>",
            parse_mode="HTML"
        )
    
    else:
        print(f"Callback data desconocido: {data}")
    await query.answer()