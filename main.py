from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from database import engine, SessionLocal

# Crear tablas
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependencia DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Esquema Pydantic
class ProductoSchema(BaseModel):
    nombre: str
    precio: float
    stock: int

    class Config:
        orm_mode = True

# GET: todos
@app.get("/productos")
def get_productos(db: Session = Depends(get_db)):
    return db.query(models.Producto).all()

# GET: por id
@app.get("/productos/{producto_id}")
def get_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

# POST: crear
@app.post("/productos")
def crear_producto(producto: ProductoSchema, db: Session = Depends(get_db)):
    nuevo = models.Producto(nombre=producto.nombre, precio=producto.precio, stock=producto.stock)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return {"mensaje": "Producto agregado", "producto": nuevo}

# PUT: actualizar
@app.put("/productos/{producto_id}")
def actualizar_producto(producto_id: int, producto: ProductoSchema, db: Session = Depends(get_db)):
    db_producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db_producto.nombre = producto.nombre
    db_producto.precio = producto.precio
    db_producto.stock = producto.stock
    db.commit()
    return {"mensaje": "Producto actualizado", "producto": db_producto}

# DELETE: borrar
@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(db_producto)
    db.commit()
    return {"mensaje": "Producto eliminado"}
