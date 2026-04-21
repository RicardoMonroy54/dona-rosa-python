from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from service.producto_service import ProductoService

# Equivalente a ProductoController.java (@RestController)
router = APIRouter(prefix="/productos", tags=["productos"])
service = ProductoService()


class ProductoRequest(BaseModel):
    codigo: int
    nombre: str
    precio: float
    cantidad: int


class ProductoUpdateRequest(BaseModel):
    nombre: str
    precio: float
    cantidad: int


@router.get("")
def obtener_productos(db: Session = Depends(get_db)):
    return service.obtener_productos(db)


@router.get("/valor-total")
def valor_total(db: Session = Depends(get_db)):
    return {"valor_total": service.valor_total_inventario(db)}


@router.get("/stock-bajo")
def stock_bajo(db: Session = Depends(get_db)):
    return service.obtener_productos_stock_bajo(db)


@router.get("/{id}")
def obtener_producto(id: int, db: Session = Depends(get_db)):
    producto = service.obtener_producto_por_id(db, id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado.")
    return producto


@router.post("")
def crear_producto(request: ProductoRequest, db: Session = Depends(get_db)):
    try:
        return service.crear_producto(db, request.codigo, request.nombre, request.precio, request.cantidad)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id}")
def actualizar_producto(id: int, request: ProductoUpdateRequest, db: Session = Depends(get_db)):
    try:
        return service.actualizar_producto(db, id, request.nombre, request.precio, request.cantidad)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{id}")
def eliminar_producto(id: int, db: Session = Depends(get_db)):
    try:
        service.eliminar_producto(db, id)
        return {"mensaje": "Producto eliminado correctamente."}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))