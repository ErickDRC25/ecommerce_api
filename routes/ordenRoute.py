from config.db import engine,OrdenesTable,DetalleOrdenesTable,CarritoTable,DetalleCarritoTable,ProductosTable,UsuariosTable
from fastapi import APIRouter,HTTPException,Depends
from utils.security import obtener_usuario_actual
from sqlalchemy import select,func,asc,desc
from services.servicescrud import obtener,insertar,actualizar,eliminar
from status.status import inexistente,no_procesable,no_permisos,retorno_mssg_accion
from datetime import datetime,time
from schemas.ordenSchema import OrdenEstado
ordenroute=APIRouter()

@ordenroute.post("/crear/orden",tags=['Orden'])
def crear_orden(user=Depends(obtener_usuario_actual)):
    idusuario= int(user['id'])
    
    with engine.begin() as conn:
        carrito=obtener(conn,CarritoTable,CarritoTable.c.usuario_id,idusuario)
        if carrito is None:
            inexistente("Carrito")
            
        detalles_existentes=conn.execute(DetalleCarritoTable.select().where(DetalleCarritoTable.c.carrito_id==carrito.id)).fetchall()
        if not detalles_existentes:
            inexistente("carrito")
        total=0
        for row in detalles_existentes:
            producto=obtener(conn,ProductosTable,ProductosTable.c.id,row.producto_id)
            if producto is None:
                inexistente("producto")
            
            if row.cantidad > producto.stock:
                no_procesable(f"La cantidad: {row.cantidad} - sobrepasa el stock: {producto.stock}")
                
            precio_producto = producto.precio
            subtotal= row.cantidad * precio_producto
            total+=subtotal
        
        orden_creada={
            "usuario_id":idusuario,
            "total":round(total,2),
            "fecha":datetime.now(),
        }
        
        resultado=insertar(conn,OrdenesTable,orden_creada)
        orden_id=resultado.lastrowid
        
        
        
        for row in detalles_existentes:
            
            
            producto=obtener(conn,ProductosTable,ProductosTable.c.id,row.producto_id)
            
            
            precio_producto=producto.precio
            
            subtotal=row.cantidad * precio_producto
            
            
            orden_detalle_creado={
                "orden_id":orden_id,
                "producto_id":row.producto_id,
                "precio_unitario":precio_producto,
                "cantidad":row.cantidad,
                "subtotal":subtotal
            }
            insertar(conn,DetalleOrdenesTable,orden_detalle_creado)
            stockactualizado={
                "stock": producto.stock - row.cantidad
            }
            actualizar(conn,ProductosTable,ProductosTable.c.id,row.producto_id,stockactualizado)
        
        eliminar(conn,DetalleCarritoTable,DetalleCarritoTable.c.carrito_id,carrito.id)
        eliminar(conn,CarritoTable,CarritoTable.c.id,carrito.id)
        
        return{
            "message":"Orden creada correctamente",
            "orden_id":orden_id,
            "total":round(total,2)
        }


@ordenroute.get("/mis-ordenes",tags=["Orden"])
def mis_ordenes(user=Depends(obtener_usuario_actual)):
    idusuario=int(user['id'])
    with engine.connect() as conn:
        resultado= conn.execute(OrdenesTable.select().where(OrdenesTable.c.usuario_id==idusuario)).fetchall()
        mostrar={
            "Titulo":"Mis ordenes",
            "Contenido":[]
        }
        
        for row in resultado:
            mostrar["Contenido"].append({
                "Codigo_orden":row.id,
                "Total":row.total,
                "Fecha":row.fecha
            })
        return  mostrar 
    

@ordenroute.get("/mi-orden/{idOrden}",tags=["Orden"])
def mi_orden(idOrden:int , user=Depends(obtener_usuario_actual)):
    idusuario=int(user['id'])
    
    with engine.connect() as conn:
        orden=conn.execute(OrdenesTable.select().where((OrdenesTable.c.id==idOrden)&(OrdenesTable.c.usuario_id==idusuario))).first()
        if orden is None:
            inexistente("orden")
        
        
        
        mostrar={
            "Codigo_orden":orden.id,
            "Contenido":[]
        }
        
        
        join=DetalleOrdenesTable.join(
            ProductosTable,DetalleOrdenesTable.c.producto_id==ProductosTable.c.id
        )
        query=select(
            ProductosTable.c.nombre.label("producto"),
            DetalleOrdenesTable.c.cantidad,
            DetalleOrdenesTable.c.precio_unitario,
        ).select_from(join).where(DetalleOrdenesTable.c.orden_id == idOrden)
        
        resultado=conn.execute(query).fetchall()
        
        for row in resultado:
            mostrar["Contenido"].append({
                "Producto":row.producto,
                "Cantidad":row.cantidad,
                "Precio_unitario":row.precio_unitario,
                "Subtotal":row.precio_unitario * row.cantidad
            })
        
        return mostrar
    

@ordenroute.get("/ordenes/admin",tags=["Admin - orden"])
def ordenes_admin(user=Depends(obtener_usuario_actual)):    
    rolusuario= user['rol']
    
    if rolusuario != "admin":
        no_permisos()
        
    with engine.connect() as conn:
        join=OrdenesTable.join(
            UsuariosTable,OrdenesTable.c.usuario_id==UsuariosTable.c.id
        )
        
        query=select(
            OrdenesTable.c.id.label("codigo_orden"),
            UsuariosTable.c.nombre.label("usuario"),
            OrdenesTable.c.total,
            OrdenesTable.c.fecha,
            OrdenesTable.c.estado
        ).select_from(join)
        
        resultado=conn.execute(query).fetchall()
        
        return [row._asdict() for row in resultado]
    
@ordenroute.put("/actualizar/estado/{idOrden}",tags=["Admin - orden"])
def actualizar_estado(idOrden:int , data:OrdenEstado , user=Depends(obtener_usuario_actual)):
    rolusuario=user['rol']
    estados_validos=['pendiente', 'pagado', 'enviado', 'entregado', 'cancelado']
    if rolusuario != "admin":
        no_permisos()
    
    with engine.begin() as conn:
        orden=obtener(conn,OrdenesTable,OrdenesTable.c.id,idOrden)
        if orden is None:
            inexistente("orden")
        
        if data.estado not in estados_validos:
            no_procesable("Estado invalido - Estados validos : pendiente , pagado , enviado, entregado, cancelado")
        
        estado_actualizado={
            "estado":data.estado
        }
        
        actualizar(conn,OrdenesTable,OrdenesTable.c.id,idOrden,estado_actualizado)
        return retorno_mssg_accion("Estado","actualizado")
    

    
@ordenroute.get("/dashboard/ventas-total",tags=["Dashboard Admin"])
def ventas_total(user=Depends(obtener_usuario_actual)):
    rolusuario=user['rol']
    if rolusuario!= "admin":
        no_permisos()
        
    with engine.connect() as conn:
        resultado=conn.execute(select(func.sum(OrdenesTable.c.total))).scalar()
        return {
            "Ventas_Totales": resultado
        }
        
@ordenroute.get("/dashboard/total-ordenes",tags=["Dashboard Admin"])
def total_ordenes(user=Depends(obtener_usuario_actual)):
    rolusuario=user['rol']
    if rolusuario != "admin":
        no_permisos()
        
    with engine.connect() as conn:
        resultado= conn.execute(select(func.count()).select_from(OrdenesTable)).scalar()
        return {
            "Total_Ordenes":resultado
        }

@ordenroute.get("/dashboard/total-usuario",tags=["Dashboard Admin"])
def total_usuarios(user=Depends(obtener_usuario_actual)):
    rolusuario= user['rol']
    if rolusuario!= "admin":
        no_permisos()
        
    with engine.connect() as conn:
        resultado=conn.execute(select(func.count()).select_from(UsuariosTable)).scalar()
        return {
            "Total_Usuarios":resultado
        }

@ordenroute.get("/dashboard/producto-mas-vendido",tags=["Dashboard Admin"])
def producto_mas_vendido(user=Depends(obtener_usuario_actual)):
    rolusuario=user['rol']
    if rolusuario != "admin":
        no_permisos()
    
    with engine.connect() as conn:
        resultado=conn.execute(
            select(DetalleOrdenesTable.c.producto_id,ProductosTable.c.nombre.label("producto"),func.sum(DetalleOrdenesTable.c.cantidad).label("total_vendido"))
            .join(ProductosTable,DetalleOrdenesTable.c.producto_id==ProductosTable.c.id)
            .group_by(DetalleOrdenesTable.c.producto_id)
            .order_by(desc("total_vendido"))
            .limit(1)
        ).first()
        
        if resultado is None:
            raise HTTPException(status_code=404,detail="No existe producto mas vendido")
        
        mostrar={
            "titulo":"Producto mas vendido",
            "producto_id":resultado.producto_id,
            "producto": resultado.producto,
            "cantidad": resultado.total_vendido
            
            
        }
        return mostrar
@ordenroute.get("/dashboard/top-clientes",tags=["Dashboard Admin"])
def top_clientes(user=Depends(obtener_usuario_actual)):
    rolusuario= user['rol']
    if rolusuario != "admin":
        no_permisos()
    
    with engine.connect() as conn:
        resultado=conn.execute(
            select(UsuariosTable.c.id.label("codigo_usuario") , UsuariosTable.c.nombre.label("cliente") , func.count(OrdenesTable.c.usuario_id).label("total_compras"))
            .join(OrdenesTable,UsuariosTable.c.id==OrdenesTable.c.usuario_id)
            .group_by("codigo_usuario","cliente")
            .order_by(desc("total_compras"))
            .limit(3)
        )
        mostrar={
            "Titulo":"TOP 3 Clientes con compras en la tienda",
            "Contenido":[]
        }
        for i,row in enumerate(resultado,1):
            
            mostrar["Contenido"].append({
                "top": i,
                "codigo_cliente": row.codigo_usuario,
                "cliente": row.cliente,
                "total_compras": row.total_compras
            })
            
        
        return mostrar

@ordenroute.get("/dashboard/ventas-estados/{estado}",tags=["Dashboard Admin"])
def ventas_x_estados(estado:str,user=Depends(obtener_usuario_actual)):
    rolusuario=user['rol']
    if rolusuario != "admin":
        no_permisos()
    estados_validos=['pendiente', 'pagado', 'enviado', 'entregado', 'cancelado']
    
    if estado.lower() not in estados_validos:
            no_procesable("Estado invalido - Estados validos : pendiente , pagado , enviado, entregado, cancelado")
            
    with engine.connect() as conn:
        join=OrdenesTable.join(UsuariosTable,OrdenesTable.c.usuario_id == UsuariosTable.c.id)
        query=select(
            OrdenesTable.c.id,
            OrdenesTable.c.usuario_id,
            UsuariosTable.c.nombre,
            OrdenesTable.c.total,
            OrdenesTable.c.fecha,
            OrdenesTable.c.estado
        ).select_from(join).where(OrdenesTable.c.estado==estado)
        resultado = conn.execute(query).fetchall()
        
        mostrar={
            "Titulo":f"Ordenes en estado: {estado}",
            "Contenido":[]
            
        }
        
        for row in resultado:
            mostrar["Contenido"].append({
                "Codigo_orden":row.id,
                "Codigo_usuario":row.usuario_id,
                "Usuario":row.nombre,
                "Total":row.total,
                "Fecha":row.fecha,
                "Estado":row.estado
            })
            
        return mostrar

@ordenroute.get("/dashboard/ventas-fecha/{fecha}",tags=["Dashboard Admin"])
def ventas_x_fecha(fecha:datetime , user=Depends(obtener_usuario_actual) ):
    rolusuario=user['rol']
    if rolusuario != "admin":
        no_permisos()
    
    inicio_dia=datetime.combine(fecha,time.min)
    fin_dia=datetime.combine(fecha,time.max)
    with engine.connect() as conn:
     
        
        join=UsuariosTable.join(OrdenesTable, OrdenesTable.c.usuario_id == UsuariosTable.c.id)
        query= select(
            OrdenesTable.c.id,
            OrdenesTable.c.usuario_id,
            UsuariosTable.c.nombre,
            OrdenesTable.c.total,
            OrdenesTable.c.fecha,
            OrdenesTable.c.estado
        ).select_from(join).where(OrdenesTable.c.fecha.between(inicio_dia,fin_dia))
        resultado=conn.execute(query).fetchall()
        
        return [row._asdict() for row in resultado]
        
