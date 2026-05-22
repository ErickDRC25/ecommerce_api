
def listar(conn:str,tabla:str):
    resultado=conn.execute(tabla.select()).fetchall()
    return resultado



def obtener(conn:str,tabla:str,tabla_columna:str,valor):
    resultado=conn.execute(tabla.select().where(tabla_columna==valor)).first()
    return resultado

def obtener_campo_repetido(conn,tabla:str,tabla_columna_nombre:str,campo_nombre:str,tabla_columna_id:int,campo_id:int):
        resultado= conn.execute(tabla.select().where((tabla_columna_nombre==campo_nombre)&(tabla_columna_id!=campo_id))).first()
        return resultado

def insertar(conn:str,tabla:str,valores:dict):
    resultado=conn.execute(tabla.insert().values(valores))
    return resultado

def eliminar(conn:str, tabla:str , tabla_columna:str,valor):
    resultado=conn.execute(tabla.delete().where(tabla_columna==valor))
    return resultado

def actualizar(conn:str , tabla:str,tabla_columna:str , columna_valor, valores:dict):
    resultado=conn.execute(tabla.update().where(tabla_columna==columna_valor).values(valores))
    return resultado


def buscar_nombre(conn:str , tabla:str , tabla_columna:str  ,valor):
    resultado=conn.execute(tabla.select().where(tabla_columna.like(f"{valor}%"))).fetchall()
    return resultado