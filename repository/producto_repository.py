from sqlalchemy.orm import Session
from models.producto import Producto

# Equivalente a ProductoRepository.java (JpaRepository)
class ProductoRepository:

    def find_all(self, db: Session):
        return db.query(Producto).all()

    def find_by_id(self, db: Session, id: int):
        return db.query(Producto).filter(Producto.id == id).first()

    def find_by_codigo(self, db: Session, codigo: int):
        return db.query(Producto).filter(Producto.codigo == codigo).first()

    def find_by_nombre(self, db: Session, nombre: str):
        return db.query(Producto).filter(
            Producto.nombre.ilike(nombre)
        ).first()

    def exists_by_codigo(self, db: Session, codigo: int) -> bool:
        return db.query(Producto).filter(Producto.codigo == codigo).first() is not None

    def exists_by_nombre(self, db: Session, nombre: str) -> bool:
        return db.query(Producto).filter(
            Producto.nombre.ilike(nombre)
        ).first() is not None

    def save(self, db: Session, producto: Producto):
        db.add(producto)
        db.commit()
        db.refresh(producto)
        return producto

    def delete(self, db: Session, producto: Producto):
        db.delete(producto)
        db.commit()

    def count(self, db: Session) -> int:
        return db.query(Producto).count()