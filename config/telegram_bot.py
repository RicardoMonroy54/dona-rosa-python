import os
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from database import SessionLocal
from service.producto_service import ProductoService

service = ProductoService()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    respuesta = (
        "Bienvenido al Inventario de Dona Rosa\n\n"
        "Comandos disponibles:\n"
        "/productos\n"
        "/valor\n"
        "/stockbajo\n"
        "/agregar codigo nombre precio cantidad\n"
        "/actualizar nombre cantidad\n"
        "/eliminar nombre"
    )
    await update.message.reply_text(respuesta)


async def productos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = SessionLocal()
    try:
        respuesta = service.obtener_inventario_telegram(db)
    finally:
        db.close()
    await update.message.reply_text(respuesta)


async def valor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = SessionLocal()
    try:
        total = service.valor_total_inventario(db)
    finally:
        db.close()
    await update.message.reply_text(f"Valor total inventario: ${total}")


async def stockbajo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = SessionLocal()
    try:
        respuesta = service.obtener_stock_bajo_telegram(db)
    finally:
        db.close()
    await update.message.reply_text(respuesta)


async def agregar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = SessionLocal()
    try:
        comando = update.message.text
        respuesta = service.agregar_producto_telegram(db, comando)
    finally:
        db.close()
    await update.message.reply_text(respuesta)


async def actualizar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = SessionLocal()
    try:
        comando = update.message.text
        respuesta = service.actualizar_producto_telegram(db, comando)
    finally:
        db.close()
    await update.message.reply_text(respuesta)


async def eliminar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = SessionLocal()
    try:
        comando = update.message.text
        respuesta = service.eliminar_producto_telegram(db, comando)
    finally:
        db.close()
    await update.message.reply_text(respuesta)


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