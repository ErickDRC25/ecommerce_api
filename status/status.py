from fastapi import HTTPException

def campo_obligatorio(campo:str):
    raise HTTPException(status_code=400,detail=f"El campo {campo} es obligatorio")

def existente(campo:str):
    raise HTTPException(status_code=409,detail=f"El {campo} ya existe")

def credenciales_inc():
    raise HTTPException(status_code=401,detail="Credenciales incorrectas")

def retorno_mssg_accion(tabla:str , accion:str):
    return {"message":f"{tabla} {accion} correctamente "}

def no_permisos():
    raise HTTPException(status_code=403,detail="No eres admin ")

def inexistente(campo:str):
    raise HTTPException(status_code=404,detail=f"{campo} inexistente")

def no_procesable(mssg:str):
    raise HTTPException(status_code=422,detail=f"{mssg}")