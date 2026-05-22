from pydantic import BaseModel
from typing import List

class ProductoCarrito(BaseModel):
    producto_id:int
    cantidad:int


class Carrito(BaseModel):
    productos:List[ProductoCarrito]
    
class CarritoActualizar(BaseModel):
    cantidad:int
    