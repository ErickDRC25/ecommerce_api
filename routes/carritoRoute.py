from config.db import engine,UsuariosTable,CarritoTable,DetalleCarritoTable,ProductosTable
from fastapi import APIRouter,Depends,HTTPException
from schemas.carritoSchema import Carrito,CarritoActualizar
from utils.security import obtener_usuario_actual
from status.status import campo_obligatorio,inexistente,no_procesable,existente,retorno_mssg_accion
from services.servicescrud import obtener,actualizar,insertar,eliminar
from datetime import datetime
from sqlalchemy import select,delete
carritorouter=APIRouter()

@carritorouter.post("/agregar/carrito",tags=['Carrito'])
def agregar_carrito(data:Carrito , user=Depends(obtener_usuario_actual)):
    idusuario=int(user['id'])
    with engine.begin() as conn:
        total=0
        carrito=obtener(conn,CarritoTable,CarritoTable.c.usuario_id,idusuario)
        if carrito is  None:
            for row in data.productos:
                producto_id=row.producto_id
                cantidad=row.cantidad
                
                producto=obtener(conn,ProductosTable,ProductosTable.c.id,producto_id)
                if producto is None:
                    inexistente("producto")
                
                if cantidad > producto.stock:
                    no_procesable(f"La cantidad: {cantidad} - sobrepasa el stock: {producto.stock}")
                    
                # subtotal=cantidad*producto.precio
                # total+=subtotal    
                    
                
            crear_carrito={
                    "usuario_id":idusuario,
                    "fecha":datetime.now()
                }
            resultado=insertar(conn,CarritoTable,crear_carrito)
            id_carrito=resultado.lastrowid
                
           
            for row in data.productos:
                producto_id=row.producto_id
                cantidad=row.cantidad
                
                producto=obtener(conn,ProductosTable,ProductosTable.c.id,producto_id)
                # subtotal=cantidad*producto.precio
                
                detalle_carrito_nuevo={
                    "carrito_id":id_carrito,
                    "producto_id":producto_id,
                    "cantidad":cantidad
                }
                
               
                
                insertar(conn,DetalleCarritoTable,detalle_carrito_nuevo)
        else:        
            for row in data.productos:
                producto_id=row.producto_id    
                cantidad=row.cantidad
                detalle_existente = conn.execute(
                        DetalleCarritoTable.select().where(
                            (DetalleCarritoTable.c.carrito_id == carrito.id) &
                            (DetalleCarritoTable.c.producto_id == producto_id)
                        )
                    ).first()
                
                if detalle_existente is not None:
                    suma_cantidad = detalle_existente.cantidad + cantidad
                    producto=obtener(conn,ProductosTable,ProductosTable.c.id,detalle_existente.producto_id)
                    
                    if suma_cantidad>producto.stock:
                        no_procesable(f"Ya tienes este producto en tu carrito ,  supera el stock real del producto q es: {producto.stock}") 
                    
                    actualizar_cantidad={
                    "cantidad":suma_cantidad
                    }
                    actualizar(conn,DetalleCarritoTable,DetalleCarritoTable.c.id,detalle_existente.id,actualizar_cantidad)
                    retorno_mssg_accion("Producto ya existente en carrito","se aumento 1 a la cantidad ")
                    continue
                
                producto=obtener(conn,ProductosTable,ProductosTable.c.id,producto_id)
                if producto is None:
                        inexistente("producto")
                
                if cantidad > producto.stock:
                    no_procesable(f"La cantidad: {cantidad} - sobrepasa el stock: {producto.stock}")

                detalle_carrito_nuevo={
                        "carrito_id":carrito.id,
                        "producto_id":producto_id,
                        "cantidad":cantidad
                    }
                insertar(conn,DetalleCarritoTable,detalle_carrito_nuevo)
            
        join=CarritoTable.join(
                UsuariosTable,CarritoTable.c.usuario_id==UsuariosTable.c.id
            ).join(
                DetalleCarritoTable,DetalleCarritoTable.c.carrito_id==CarritoTable.c.id
            ).join(
                ProductosTable,ProductosTable.c.id==DetalleCarritoTable.c.producto_id
            )
            
        query=select(
                ProductosTable.c.nombre.label("producto"),
                DetalleCarritoTable.c.cantidad,
                ProductosTable.c.precio,
            ).select_from(join).where(CarritoTable.c.usuario_id==idusuario)
            
        resultado=conn.execute(query).fetchall()
        total=0
            
        mostrar={
                "Titulo":"Mi carrito",
                "Contenido":[]
            }
            
        for row in resultado:
                subtotal=row.cantidad * row.precio
                mostrar["Contenido"].append({
                    "producto":row.producto,
                    "cantidad":row.cantidad,
                    "precio":row.precio,
                    "subtotal":subtotal
                })
                total+=subtotal
            
        mostrar["Total"]=total
            
        return mostrar
        
        
@carritorouter.get("/ver/mi-carrito",tags=['Carrito'])
def mi_carrito(user=Depends(obtener_usuario_actual)):
    idusuario=int(user['id'])
    with engine.connect() as conn:
        join=DetalleCarritoTable.join(
            CarritoTable,DetalleCarritoTable.c.carrito_id==CarritoTable.c.id
            ).join(
                ProductosTable,DetalleCarritoTable.c.producto_id==ProductosTable.c.id
            )
            
        query=select(
            ProductosTable.c.nombre.label("producto"),
            DetalleCarritoTable.c.cantidad,
            ProductosTable.c.precio,
        ).select_from(join).where(CarritoTable.c.usuario_id==idusuario)
        
        resultado=conn.execute(query).fetchall()
        
        if not resultado:
            inexistente("Carrito")
            
        
        
        productos={
            "Productos":[],
        }
        
        total=0
        for row in resultado:
            subtotal=row.cantidad * row.precio
            productos["Productos"].append({
                "producto":row.producto,
                "cantidad":row.cantidad,
                "subtotal":subtotal
            })
            
            total+=subtotal

        mostrar={
            "Titulo":"Mi carrito",
            "Contenido":productos,
            "Total":total
            
        }
        return mostrar
            
            
@carritorouter.put("/actualizar/carrito/{idDetalle}",tags=['Carrito'])
def actualizar_cantidad(idDetalle:int ,data:CarritoActualizar,user=Depends(obtener_usuario_actual)):
    idusuario=int(user['id'])
    with engine.begin() as conn:
        carrito=obtener(conn,CarritoTable,CarritoTable.c.usuario_id,idusuario)
        if carrito is None:
            raise HTTPException(status_code=404,detail="No tienes carrito")
        
        
        detalle_carrito=conn.execute(DetalleCarritoTable.select().where((DetalleCarritoTable.c.id==idDetalle)&(DetalleCarritoTable.c.carrito_id==carrito.id))).first()
        if detalle_carrito is None:
            raise HTTPException(status_code=404,detail="No tienes productos en carrito")
        
        producto=obtener(conn,ProductosTable,ProductosTable.c.id,detalle_carrito.producto_id)
        if producto is None:
            raise HTTPException(status_code=404,detail="Producto no existente")
        
        if data.cantidad > producto.stock:
            no_procesable(f"La cantidad: {detalle_carrito.cantidad} - sobrepasa el stock: {producto.stock}")
            
        actualizar_detalle={
                "cantidad":data.cantidad
            }
            
        actualizar(conn,DetalleCarritoTable,DetalleCarritoTable.c.id,idDetalle,actualizar_detalle)
        
        return retorno_mssg_accion("Cantidad","actualizada")

@carritorouter.delete("/eliminar/producto/carrito/{idDetalle}",tags=["Carrito"])
def eliminar_producto_carrito(idDetalle:int , user=Depends(obtener_usuario_actual)):
    idusuario=int(user['id'])
    with engine.begin() as conn:
        carrito=obtener(conn,CarritoTable,CarritoTable.c.usuario_id,idusuario)
        if carrito is None:
            raise HTTPException(status_code=404,detail="No tienes carrito")
        
        detalle_carrito=conn.execute(DetalleCarritoTable.select().where((DetalleCarritoTable.c.id==idDetalle)&(DetalleCarritoTable.c.carrito_id==carrito.id))).first()
        if detalle_carrito is None:
            raise HTTPException(status_code=404,detail="No existe el producto en tu carrito")
        
        eliminar(conn,DetalleCarritoTable,DetalleCarritoTable.c.id,idDetalle)
        return retorno_mssg_accion("Producto","eliminado del carrito")
        
@carritorouter.delete("/vaciar/carrito",tags=['Carrito'])
def vaciar_carrito( user=Depends(obtener_usuario_actual)):
    idusuario=int(user['id'])
    
    with engine.begin() as conn:
        carrito=obtener(conn,CarritoTable,CarritoTable.c.usuario_id,idusuario)
        if carrito is None:
            raise HTTPException(status_code=404,detail="No tienes carrito")
        
        eliminar(conn,DetalleCarritoTable,DetalleCarritoTable.c.carrito_id,carrito.id)
        return retorno_mssg_accion("Los productos del carrito", "han sido eliminados")