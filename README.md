# Ecommerce Backend API - FastAPI

Backend desarrollado con FastAPI y SQLAlchemy para un sistema ecommerce con autenticación JWT, carrito de compras, órdenes, dashboard administrativo y control de stock.

---

# Tecnologías utilizadas

- Python
- FastAPI
- SQLAlchemy
- MySQL
- JWT Authentication
- Passlib (hash de contraseñas)
- Swagger UI
- Uvicorn

---

#  Funcionalidades principales

##  Autenticación
- Login con JWT
- Roles de usuario
- Protección de rutas
- Middleware con token bearer

---

##  Productos
- Crear productos
- Listar productos
- Actualizar productos
- Eliminar productos
- Control de stock

---

## Categorías
- CRUD completo de categorías
- Validación de nombres repetidos

---

## Carrito de compras
- Agregar productos
- Actualizar cantidades
- Eliminar productos
- Vaciar carrito
- Validación de stock

---

## Órdenes
- Crear órdenes desde carrito
- Generación automática de detalle de orden
- Descuento automático de stock
- Historial de órdenes
- Ver detalle de orden

---

## Dashboard Admin
- Ventas totales
- Total de órdenes
- Total de usuarios
- Producto más vendido
- Top clientes
- Filtro por estado
- Filtro por fecha

---

# Estructura del proyecto

```bash
project/
│
├── config/
├── routes/
├── schemas/
├── services/
├── status/
├── utils/
├── main.py
└── requirements.txt
```

---

# Autenticación

La API utiliza JWT Bearer Token.

Ejemplo:

```bash
Authorization: Bearer TOKEN
```

---

# Instalación

## 1. Clonar repositorio

```bash
git clone https://github.com/TU/TU-REPO.git
```

---

## 2. Crear entorno virtual

```bash
python -m venv venv
```

---

## 3. Activar entorno virtual

### Windows

```bash
venv\Scripts\activate
```


---

## 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 5. Ejecutar servidor

```bash
uvicorn main:app --reload
```

---

#  Documentación Swagger

FastAPI genera documentación automática.

## Swagger UI

```bash
http://127.0.0.1:8000/docs
```

---

# Aprendizajes del proyecto

Durante este proyecto practiqué:

- Arquitectura backend
- SQLAlchemy Core
- Relaciones entre tablas
- Manejo de transacciones
- JWT Authentication
- CRUDs complejos
- Validaciones
- Dashboard administrativo
- Manejo de stock
- Lógica de negocio ecommerce

---





# Autor

Erick Diego Romero Cruz

