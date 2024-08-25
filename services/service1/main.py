from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from typing import Optional, Dict

app = FastAPI()

# Configuración del logger
logger = logging.getLogger("servicio 1")
logging.basicConfig(level=logging.INFO)

# Simulación de una base de datos en memoria
bd_items: Dict[int, Dict] = {}

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

@app.get("/")
def read_root():
    logger.info("Petición recibida en servicio 1")
    return {"message": "Hola desde servicio 1"}

@app.get("/health")
def health_check():
    logger.info("Servicio 1 funcionando correctamente")
    return {"status": "Funcionando"}

# Nuevo método POST para crear un ítem
@app.post("/items/")
def create_item(item: Item):
    item_id = len(bd_items) + 1
    bd_items[item_id] = item.dict()
    logger.info(f"Item creado: {item.dict()}")
    return {"item_id": item_id, "item": item.dict()}

# Nuevo método DELETE para eliminar un ítem por ID
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id in bd_items:
        deleted_item = bd_items.pop(item_id)
        logger.info(f"Item eliminado: {deleted_item}")
        return {"message": "Item eliminado", "item": deleted_item}
    else:
        logger.warning(f"No se pudo eliminar item_id: {item_id}")
        raise HTTPException(status_code=404, detail="Item no encontrado")
