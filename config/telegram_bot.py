import os
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from database import SessionLocal
from service.producto_service import ProductoService

service = ProductoService()


def menu_teclado():
    teclado = [
        ["💾 /agregar", "✏️ /actualizar"],
        ["❌ /eliminar", "👁️ /productos"],
        ["💲 /valor", "🚨 /stockbajo"]
    ]
    return ReplyKeyboardMarkup(teclado, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    respuesta = (
        "🛒 *Bienvenido al Inventario de Doña Rosa*\n\n"
        "Seleccione una opción del menú:\n\n"
        "💾 /agregar codigo nombre precio cantidad\n"
        "✏️ /actualizar nombre cantidad\n"
        "❌ /eliminar nombre\n"
        "👁️ /productos\n"
        "💲 /valor\n"
        "🚨 /stockbajo"
    )
    await update.message.reply_text(
        respuesta,
        parse_mode="Markdown",
        reply_markup=menu_teclado()
    )


async def productos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = SessionLocal()
    try:
        productos_lista = service.obtener_productos(db)
        if not productos_lista:
            respuesta = "📦 No hay productos en el inventario."
        else:
            respuesta = "🛒🍇🥑 *PRODUCTOS* 🛒\n\n"
            for p in productos_lista:
                alerta = " ⚠️" if p.stock_critico() else ""
                respuesta += (
                    f"🛒 *{p.nombre}*{alerta}\n"
                    f"   Cantidad: {p.cantidad}\n"
                    f"   Precio: ${p.precio}\n"
                    f"   Total: ${p.precio * p.cantidad}\n\n"
                )
    finally:
        db.close()
    await update.message.reply_text(
        respuesta,
        parse_mode="Markdown",
        reply_markup=menu_teclado()
    )


async def valor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = SessionLocal()
    try:
        productos_lista = service.obtener_productos(db)
        total_general = service.valor_total_inventario(db)

        if not productos_lista:
            respuesta = "📦 No hay productos en el inventario."
        else:
            respuesta = "💲 *Valor del Inventario*\n\n"
            for p in productos_lista:
                subtotal = p.precio * p.cantidad
                respuesta += (
                    f"🛒 *{p.nombre}*\n"
                    f"   Cantidad: {p.cantidad} | Precio: ${p.precio}\n"
                    f"   Subtotal: ${subtotal}\n\n"
                )
            respuesta += "━━━━━━━━━━━━━━━━━━\n"
            respuesta += f"💰 *Total general: ${total_general}*"
    finally:
        db.close()
    await update.message.reply_text(
        respuesta,
        parse_mode="Markdown",
        reply_markup=menu_teclado()
    )


async def stockbajo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = SessionLocal()
    try:
        bajos = service.obtener_productos_stock_bajo(db)
        if not bajos:
            respuesta = "✅ No hay productos con stock bajo."
        else:
            respuesta = "🚨 *Productos por agotarse:*\n\n"
            for p in bajos:
                respuesta += f"⚠️ *{p.nombre}*\n   Cantidad: {p.cantidad}\n\n"
    finally:
        db.close()
    await update.message.reply_text(
        respuesta,
        parse_mode="Markdown",
        reply_markup=menu_teclado()
    )


async def agregar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = SessionLocal()
    try:
        comando = update.message.text
        respuesta = service.agregar_producto_telegram(db, comando)
    finally:
        db.close()
    await update.message.reply_text(
        f"💾 {respuesta}",
        reply_markup=menu_teclado()
    )


async def actualizar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = SessionLocal()
    try:
        comando = update.message.text
        respuesta = service.actualizar_producto_telegram(db, comando)
    finally:
        db.close()
    await update.message.reply_text(
        f"✏️ {respuesta}",
        reply_markup=menu_teclado()
    )


async def eliminar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = SessionLocal()
    try:
        comando = update.message.text
        respuesta = service.eliminar_producto_telegram(db, comando)
    finally:
        db.close()
    await update.message.reply_text(
        f"❌ {respuesta}",
        reply_markup=menu_teclado()
    )


def iniciar_bot():
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    print(f"Token cargado: {token[:10]}...")

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("productos", productos))
    app.add_handler(CommandHandler("valor", valor))
    app.add_handler(CommandHandler("stockbajo", stockbajo))
    app.add_handler(CommandHandler("agregar", agregar))
    app.add_handler(CommandHandler("actualizar", actualizar))
    app.add_handler(CommandHandler("eliminar", eliminar))

    print("Bot de Telegram iniciado correctamente")
    app.run_polling()