from fastapi import APIRouter
from schemas.loginSchema import Login
from status.status import campo_obligatorio,credenciales_inc
from config.db import engine,UsuariosTable
from services.servicescrud import obtener
from services.servicehash import verify_password
from utils.jwt import crear_token

loginroute=APIRouter()

@loginroute.post("/auth/login",tags=["Login"])
def login(data:Login):
    
    if not data.email or data.email.strip()=="":
        campo_obligatorio("email")
    
    if not data.password or data.password.strip()=="":
        campo_obligatorio("password")
        
    with engine.begin() as conn:
        usuario=obtener(conn,UsuariosTable,UsuariosTable.c.email,data.email)
        if usuario is None:
            credenciales_inc()
        
        if not verify_password(data.password , usuario.password):
            credenciales_inc()
        
        token= crear_token({
            "id":usuario.id,
            "rol":usuario.rol
        })
        
        return {
            "access_token":token,
            "token_type":"bearer"
        }
        