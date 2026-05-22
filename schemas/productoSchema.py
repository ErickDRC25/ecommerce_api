from pydantic import BaseModel

class ProductoCreate(BaseModel):
    nombre:str
    descripcion:str
    precio:float
    stock:int
    categoria_id:int