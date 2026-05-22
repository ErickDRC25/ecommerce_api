from config.db import engine,CategoriasTable
from fastapi import APIRouter,Depends
from utils.security import obtener_usuario_actual
from status.status import no_permisos,campo_obligatorio,retorno_mssg_accion,inexistente,existente
from schemas.categoriaSchema import CategoriaCreate
from services.servicescrud import insertar,listar,obtener,eliminar,obtener_campo_repetido,actualizar
categoriaroute=APIRouter()

@categoriaroute.post("/crear/categoria",tags=["Admin - categoria"])
def crear_categoria(data:CategoriaCreate,user=Depends(obtener_usuario_actual)):
    rolusuario=user['rol']
    if rolusuario != "admin":
        no_permisos()
        
    if not data.nombre or data.nombre.strip()=="":
        campo_obligatorio("nombre")
        
    with engine.begin() as conn:
        
        categoria_nueva={"nombre":data.nombre.capitalize()}
        categoria_existente=obtener(conn,CategoriasTable,CategoriasTable.c.nombre,data.nombre)
        if categoria_existente is not None:
            existente(f"nombre de la categoria {categoria_existente.nombre}")
            
        insertar(conn,CategoriasTable,categoria_nueva)
        
        
        
        return retorno_mssg_accion("Categoria","creada")
    
@categoriaroute.get("/listar/categoria",tags=["Categoria"])
def listar_categoria():
    with engine.connect() as conn:  
        resultado=listar(conn,CategoriasTable)
        return [row._asdict() for row in resultado]
    
@categoriaroute.get("/obtener/categoria/{idCategoria}",tags=["Categoria"])
def obtener_categoria(idCategoria:int):
    with engine.connect() as conn:
        resultado = obtener(conn,CategoriasTable,CategoriasTable.c.id,idCategoria)
        if resultado is None:
            inexistente("Categoria")
        return resultado._asdict()
    
    
@categoriaroute.put("/actualizar/categoria/{idCategoria}",tags=["Admin - categoria"])
def actualizar_categoria(idCategoria:int,data:CategoriaCreate , user=Depends(obtener_usuario_actual)):
    rolusuario= user['rol']
    if rolusuario != "admin":
        no_permisos()
        
    if not data.nombre or data.nombre.strip()=="":
        campo_obligatorio()
        
    with engine.begin() as conn:
        categoria_actualizado={
            "nombre":data.nombre.capitalize()
        }
        
        
        categoria_existente=obtener_campo_repetido(conn,CategoriasTable,CategoriasTable.c.nombre,data.nombre,CategoriasTable.c.id,idCategoria)
        if categoria_existente is not None:
            existente(f"nombre de la categoria {categoria_existente.nombre}")
            
        actualizar(conn,CategoriasTable,CategoriasTable.c.id,idCategoria,categoria_actualizado)
        return retorno_mssg_accion("Categoria","actualizado")

    
@categoriaroute.delete("/eliminar/categoria/{idCategoria}",tags=["Admin - categoria"])
def eliminar_categoria(idCategoria:int,user=Depends(obtener_usuario_actual)):
    rolusuario=user['rol']
    if rolusuario != "admin":
        no_permisos()
        
    with engine.begin() as conn:
        eliminar(conn,CategoriasTable,CategoriasTable.c.id,idCategoria)
        return retorno_mssg_accion(f"Categoria " , "eliminado")