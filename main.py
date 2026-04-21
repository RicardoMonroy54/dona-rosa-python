import threading
import os
from fastapi import FastAPI
from dotenv import load_dotenv
from database import engine, SessionLocal, Base
from models.producto import Producto
from controller.producto_controller import router
from config.data_loader import cargar_datos
from config.telegram_bot import iniciar_bot

# Equivalente a DonaRosaInventarioApplication.java
load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventario Dona Rosa")
app.include_router(router)

@app.on_event("startup")
def startup():
    db = SessionLocal()
    try:
        cargar_datos(db)
    finally:
        db.close()

    hilo_bot = threading.Thread(target=iniciar_bot, daemon=True)
    hilo_bot.start()