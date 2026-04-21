import math
from sqlalchemy import Column, Integer, String, Float
from database import Base

# Equivalente a la entidad @Entity Producto.java
class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    codigo = Column(Integer, nullable=False, unique=True)
    nombre = Column(String, nullable=False, unique=True)
    precio = Column(Float, nullable=False)
    cantidad = Column(Integer, nullable=False)
    cantidad_inicial = Column(Integer, nullable=False)

    def stock_critico(self) -> bool:
        return self.cantidad <= math.ceil(self.cantidad_inicial * 0.10)

    def valor_inventario(self) -> float:
        return self.precio * self.cantidad