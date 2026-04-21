from sqlalchemy.orm import Session
from models.producto import Producto
from repository.producto_repository import ProductoRepository

# Equivalente a DataLoader.java (CommandLineRunner)
def cargar_datos(db: Session):
    repo = ProductoRepository()

    if repo.count(db) == 0:
        productos_iniciales = [
            Producto(codigo=1,  nombre="Peras",       precio=4000.0, cantidad=65,  cantidad_inicial=65),
            Producto(codigo=2,  nombre="Limones",     precio=1500.0, cantidad=25,  cantidad_inicial=25),
            Producto(codigo=3,  nombre="Moras",       precio=2000.0, cantidad=30,  cantidad_inicial=30),
            Producto(codigo=4,  nombre="Piñas",       precio=3000.0, cantidad=15,  cantidad_inicial=15),
            Producto(codigo=5,  nombre="Tomates",     precio=1000.0, cantidad=30,  cantidad_inicial=30),
            Producto(codigo=6,  nombre="Fresas",      precio=3000.0, cantidad=12,  cantidad_inicial=12),
            Producto(codigo=7,  nombre="Frunas",      precio=300.0,  cantidad=50,  cantidad_inicial=50),
            Producto(codigo=8,  nombre="Galletas",    precio=500.0,  cantidad=400, cantidad_inicial=400),
            Producto(codigo=9,  nombre="Chocolates",  precio=1200.0, cantidad=500, cantidad_inicial=500),
            Producto(codigo=10, nombre="Arroz",       precio=1200.0, cantidad=60,  cantidad_inicial=60),
        ]

        for producto in productos_iniciales:
            repo.save(db, producto)

        print("Productos iniciales cargados correctamente")