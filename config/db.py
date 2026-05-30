from sqlalchemy import create_engine,Table,MetaData
import os
from dotenv import load_dotenv
load_dotenv()

DB_URL = os.getenv("DB_URL")

metadata=MetaData()
engine = create_engine(DB_URL)

UsuariosTable=Table('usuarios',metadata,autoload_with=engine)
CarritoTable=Table('carrito',metadata,autoload_with=engine)
DetalleCarritoTable=Table('detalle_carrito',metadata,autoload_with=engine)
ProductosTable=Table('productos',metadata,autoload_with=engine)
CategoriasTable=Table('categorias',metadata,autoload_with=engine)
DetalleOrdenesTable=Table('detalle_ordenes',metadata,autoload_with=engine)
OrdenesTable=Table('ordenes',metadata,autoload_with=engine)