from fastapi import APIRouter,Depends
from config.db import engine,UsuariosTable
from schemas.usuarioSchema import UsuarioCreate
from status.status import campo_obligatorio,retorno_mssg_accion,existente,no_permisos
from services.servicescrud import insertar,obtener,listar
from services.servicehash import hash_password,verify_password
from utils.security import obtener_usuario_actual
usuariorouter=APIRouter()

@usuariorouter.post("/crear/usuario",tags=['Usuario'])
def crear_usuario(data:UsuarioCreate):
    if not data.nombre or data.nombre.strip()=="":
        campo_obligatorio("nombre")
    if not data.email or data.email.strip()=="":
        campo_obligatorio("email")
    if not data.password or data.password.strip()=="":
        campo_obligatorio("password")
    
    with engine.begin() as conn:
        usuario=obtener(conn,UsuariosTable,UsuariosTable.c.email,data.email)
        if usuario is not None:
            existente("email")
        usuario_nuevo={
            "nombre":data.nombre.capitalize(),
            "email":data.email,
            "password":hash_password(data.password)
        }
        resultado=insertar(conn,UsuariosTable,usuario_nuevo)
        return retorno_mssg_accion("Usuario","creado")
    

@usuariorouter.get("/perfil/usuario",tags=['Usuario'])
def perfil_usuario(user=Depends(obtener_usuario_actual)):
    idusuario=int(user['id'])
    
    with engine.connect() as conn:
        usuario=obtener(conn,UsuariosTable,UsuariosTable.c.id,idusuario)
        return{
            "Codigo_Usuario":usuario.id,
            "Nombre":usuario.nombre,
            "Email":usuario.email,
            "Password":"*************************"
        }
        
        
@usuariorouter.get("/usuarios",tags=['Admin - usuario'])
def listar_usuarios(user=Depends(obtener_usuario_actual)):
    rolusuario=user['rol']
    if rolusuario != "admin":
        no_permisos()
        
    with engine.connect() as conn:
        resultado=listar(conn,UsuariosTable)
        
        usuarios=[]
        for fila in resultado:
            usuarios.append({
                "id_usuario":fila.id,
                "usuario":fila.nombre,
                "email":fila.email,
                "password":"********",
                "rol":fila.rol
            })

    return usuarios
            
        
        
    

        