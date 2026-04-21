from sqlalchemy.orm import Session
from models.producto import Producto
from repository.producto_repository import ProductoRepository

# Equivalente a ProductoService.java
class ProductoService:

    def __init__(self):
        self.repo = ProductoRepository()

    # ---------------------------------------------------------------
    # Métodos para la API REST
    # ---------------------------------------------------------------

    def obtener_productos(self, db: Session):
        return self.repo.find_all(db)

    def obtener_producto_por_id(self, db: Session, id: int):
        return self.repo.find_by_id(db, id)

    def crear_producto(self, db: Session, codigo: int, nombre: str, precio: float, cantidad: int):
        if precio <= 0:
            raise ValueError("El precio debe ser mayor que cero.")
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        if self.repo.exists_by_codigo(db, codigo):
            raise ValueError("Ya existe un producto con ese código.")
        if self.repo.exists_by_nombre(db, nombre):
            raise ValueError("Ya existe un producto con ese nombre.")

        producto = Producto(
            codigo=codigo,
            nombre=nombre,
            precio=precio,
            cantidad=cantidad,
            cantidad_inicial=cantidad
        )
        return self.repo.save(db, producto)

    def actualizar_producto(self, db: Session, id: int, nombre: str, precio: float, cantidad: int):
        producto = self.repo.find_by_id(db, id)
        if not producto:
            raise ValueError("Producto no encontrado.")
        if precio <= 0:
            raise ValueError("El precio debe ser mayor que cero.")
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")

        producto.nombre = nombre
        producto.precio = precio
        producto.cantidad = cantidad
        return self.repo.save(db, producto)

    def eliminar_producto(self, db: Session, id: int):
        producto = self.repo.find_by_id(db, id)
        if not producto:
            raise ValueError("Producto no encontrado.")
        self.repo.delete(db, producto)

    def obtener_productos_stock_bajo(self, db: Session):
        return [p for p in self.repo.find_all(db) if p.stock_critico()]

    def valor_total_inventario(self, db: Session) -> float:
        return sum(p.precio * p.cantidad for p in self.repo.find_all(db))

    # ---------------------------------------------------------------
    # Métodos para Telegram
    # ---------------------------------------------------------------

    def obtener_inventario_telegram(self, db: Session) -> str:
        productos = self.repo.find_all(db)
        respuesta = "Inventario Dona Rosa\n\n"
        for p in productos:
            respuesta += f"{p.nombre} - {p.cantidad} | ${p.precio}\n"
        return respuesta

    def obtener_stock_bajo_telegram(self, db: Session) -> str:
        bajos = self.obtener_productos_stock_bajo(db)
        if not bajos:
            return "No hay productos con stock bajo."
        respuesta = "Productos con stock bajo\n\n"
        for p in bajos:
            respuesta += f"{p.nombre} - {p.cantidad}\n"
        return respuesta

    def agregar_producto_telegram(self, db: Session, comando: str) -> str:
        try:
            partes = comando.strip().split()
            if len(partes) < 5:
                return "Formato incorrecto.\nUsa: /agregar codigo nombre precio cantidad"
            codigo = int(partes[1])
            nombre = partes[2]
            precio = float(partes[3])
            cantidad = int(partes[4])
            self.crear_producto(db, codigo, nombre, precio, cantidad)
            return f"Producto agregado correctamente.\nNombre: {nombre}\nPrecio: ${precio}\nCantidad: {cantidad}"
        except ValueError as e:
            return str(e)

    def actualizar_producto_telegram(self, db: Session, comando: str) -> str:
        try:
            partes = comando.strip().split()
            if len(partes) < 3:
                return "Formato incorrecto.\nUsa: /actualizar nombre cantidad"
            nombre = partes[1]
            nueva_cantidad = int(partes[2])
            if nueva_cantidad < 0:
                return "La cantidad no puede ser negativa."
            producto = self.repo.find_by_nombre(db, nombre)
            if not producto:
                return "Producto no encontrado."
            producto.cantidad = nueva_cantidad
            self.repo.save(db, producto)
            respuesta = f"Producto actualizado.\n{producto.nombre} ahora tiene {producto.cantidad} unidades."
            if producto.stock_critico():
                respuesta += f"\nAtencion: {producto.nombre} esta por debajo del stock minimo del 10%."
            return respuesta
        except ValueError:
            return "La cantidad debe ser un número válido."

    def eliminar_producto_telegram(self, db: Session, comando: str) -> str:
        try:
            partes = comando.strip().split()
            if len(partes) < 2:
                return "Formato incorrecto.\nUsa: /eliminar nombre"
            nombre = partes[1]
            producto = self.repo.find_by_nombre(db, nombre)
            if not producto:
                return "Producto no encontrado."
            self.repo.delete(db, producto)
            return f"Producto eliminado correctamente: {producto.nombre}"
        except Exception as e:
            return str(e)