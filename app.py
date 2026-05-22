from fastapi import FastAPI
from routes.usuarioRouter import usuariorouter
from routes.loginRoute import loginroute
from routes.categoriaRoute import categoriaroute
from routes.productoRoute import productoroute
from routes.carritoRoute import carritorouter
from routes.ordenRoute import ordenroute
app = FastAPI()

app.include_router(usuariorouter)
app.include_router(loginroute)
app.include_router(categoriaroute)
app.include_router(productoroute)
app.include_router(carritorouter)
app.include_router(ordenroute)