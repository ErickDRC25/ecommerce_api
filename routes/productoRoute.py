from fastapi import APIRouter,Depends,HTTPException
from schemas.productoSchema import ProductoCreate
from config.db import engine,ProductosTable,CategoriasTable
from utils.security import obtener_usuario_actual
from status.status import no_permisos,campo_obligatorio,existente,inexistente,retorno_mssg_accion
from services.servicescrud import obtener,obtener_campo_repetido,actualizar,eliminar,insertar,listar,buscar_nombre
from sqlalchemy import select

productoroute=APIRouter()


@productoroute.post("/crear/producto",tags=["Admin - producto"])
def crear_producto(data:ProductoCreate , user=Depends(obtener_usuario_actual)):
    rolusuario=user['rol']
    if rolusuario != "admin":
        no_permisos()
        
    if not data.nombre or data.nombre.strip()=="":
        campo_obligatorio()
    
    if not data.descripcion or data.descripcion.strip()=="":
        campo_obligatorio()
        
    if  data.precio is None:
        campo_obligatorio()
    
    if data.stock is None:
        campo_obligatorio()
    
    if data.categoria_id is None:
        campo_obligatorio()
        
    with engine.begin() as conn:
        producto_existente=obtener(conn,ProductosTable,ProductosTable.c.nombre,data.nombre)
        
        if producto_existente is not None:
            existente("producto")
         
        categoria_existente=obtener(conn,CategoriasTable,CategoriasTable.c.id,data.categoria_id)
        if categoria_existente is None:
            inexistente("categoria")
        
        producto_nuevo={
            "nombre":data.nombre.capitalize(),
            "descripcion":data.descripcion,
            "precio":data.precio,
            "stock":data.stock,
            "categoria_id":data.categoria_id
        }   
        insertar(conn,ProductosTable,producto_nuevo)
        return retorno_mssg_accion("Producto","creado")

@productoroute.get("/listar/productos",tags=["Producto"])
def listar_producto():
    with engine.connect() as conn:
        resultado=listar(conn,ProductosTable)
        return [row._asdict() for row in resultado]
    
@productoroute.get("/obtener/producto/{idProducto}",tags=["Producto"])
def obtener_producto(idProducto:int):
    with engine.connect() as conn:
        resultado=obtener(conn,ProductosTable,ProductosTable.c.id,idProducto)
        if resultado is None:
            inexistente("producto")
        return resultado._asdict()
    
@productoroute.put("/actualizar/producto/{idProducto}",tags=["Admin - producto"])
def actualizar_producto(idProducto:int , data:ProductoCreate , user=Depends(obtener_usuario_actual)):
    rolusuario=user['rol']
    if rolusuario != "admin":
        no_permisos()
        
    with engine.begin() as conn:
        producto_existente=obtener_campo_repetido(conn,ProductosTable,ProductosTable.c.nombre,data.nombre,ProductosTable.c.id,idProducto)
        if producto_existente is not None:
            existente("producto")
        
        categoria_existente=obtener(conn,CategoriasTable,CategoriasTable.c.id,data.categoria_id)
        if categoria_existente is None:
            inexistente("categoria")
            
        producto_actualiado={
            "nombre":data.nombre.capitalize(),
            "descripcion":data.descripcion,
            "precio":data.precio,
            "stock":data.stock,
            "categoria_id":data.categoria_id
        }
        
        actualizar(conn,ProductosTable,ProductosTable.c.id,idProducto,producto_actualiado)
        return retorno_mssg_accion("Producto","actualizado")
    
@productoroute.delete("/eliminar/producto/{idProducto}",tags=["Admin - producto"])
def eliminar_producto(idProducto:int , user=Depends(obtener_usuario_actual)):
    rolusuario=user["rol"]
    if rolusuario != "admin":
        no_permisos()
        
    with engine.begin() as conn:
        producto_existente=obtener(conn,ProductosTable,ProductosTable.c.id,idProducto)
        if producto_existente is None:
            inexistente("producto")
            
        eliminar(conn,ProductosTable,ProductosTable.c.id,idProducto)
        return  retorno_mssg_accion("Producto","eliminado")


@productoroute.get("/producto/categoria",tags=["Producto"])
def producto_categoria():
    with engine.connect() as conn:
        tablaunida= ProductosTable.join(CategoriasTable,ProductosTable.c.categoria_id==CategoriasTable.c.id)
        query=select(
            ProductosTable.c.nombre.label("Producto"),
            CategoriasTable.c.nombre.label("Categoria")
        ).select_from(tablaunida)
        
        resultado=conn.execute(query).fetchall()
        return [ row._asdict() for row in resultado]
    

@productoroute.get("/producto/paginacion",tags=["Producto"])
def paginacion_producto(limit:int=5 , offset:int= 0):
    with engine.connect() as conn:
        query=ProductosTable.select().limit(limit).offset(offset)
        resultado=conn.execute(query).fetchall()
        
        return [ row._asdict() for row in resultado]
    
@productoroute.get("/productos/categoria/{idCategoria}",tags=["Producto"])
def productos_xCategoria(idCategoria:int):
    with engine.connect() as conn:
       
        join=ProductosTable.join(CategoriasTable,ProductosTable.c.categoria_id==CategoriasTable.c.id)
        query=select(
            CategoriasTable.c.nombre.label("categoria"),
            ProductosTable.c.id,
            ProductosTable.c.nombre.label("producto")).select_from(join).where(CategoriasTable.c.id==idCategoria)
        
        resultado=conn.execute(query).fetchall()
        if not resultado:
            inexistente(f"La categoria no contiene productos, estado: ")
        
        mostrar={
            "Categoria":resultado[0].categoria,
            "Productos":[]
        }
        
        for row in resultado:
            mostrar["Productos"].append({
                "producto_id": row.id,
                "producto":row.producto
            })
        
        return mostrar
    
@productoroute.get("/buscar/producto/automatico/{palabra}",tags=["Producto"])
def buscar_producto_automatico(palabra:str):
    with engine.connect() as conn:
        resultado=buscar_nombre(conn,ProductosTable,ProductosTable.c.nombre,palabra)
        return [row.nombre for row in resultado]
            

@productoroute.get("/producto/bajo-stock",tags=["Admin - producto"])
def producto_bajo_stock(user=Depends(obtener_usuario_actual)):
    rolusuario=user["rol"]
    if rolusuario != "admin":
        no_permisos()
        
    with engine.connect() as conn:
        resultado=conn.execute(ProductosTable.select().where(ProductosTable.c.stock<5)).fetchall()
        if not resultado:
            raise HTTPException(status_code=404,detail="No hay productos con bajo stock")
        
        mostrar={
            "Titulo":"Productos con bajo stock",
            "Productos":[]
        }
        
        for row in resultado:
            mostrar["Productos"].append({
                "id_producto":row.id,
                "producto":row.nombre
            })
        
        return mostrar
    
@productoroute.get("/listar/productos/categorias",tags=["Categoria"])
def listar_productos_conCategoria():
    
    with engine.connect() as conn:
        join=CategoriasTable.join(ProductosTable,ProductosTable.c.categoria_id==CategoriasTable.c.id)
        query=select(
            ProductosTable.c.id,
            ProductosTable.c.nombre.label("producto"),
            ProductosTable.c.descripcion,
            ProductosTable.c.precio,
            ProductosTable.c.stock,
            CategoriasTable.c.id.label("categoria_id"),
            CategoriasTable.c.nombre.label("categoria")
        ).select_from(join)
        
        resultado=conn.execute(query).fetchall()
        
        return[ row._asdict() for row in resultado]
    