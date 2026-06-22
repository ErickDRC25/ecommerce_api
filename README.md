# Ecommerce Backend API - FastAPI

Backend desarrollado con FastAPI y SQLAlchemy para un sistema ecommerce con autenticación JWT, carrito de compras, órdenes, dashboard administrativo y control de stock.

Frontend relacionado (React + Tailwind): [tienda-react](https://github.com/ErickDRC25/tienda-react)

---

# Demo en producción

- API en vivo: [https://ecommerce-api-l7i1.onrender.com](https://ecommerce-api-l7i1.onrender.com)
- Documentación Swagger: [https://ecommerce-api-l7i1.onrender.com/docs](https://ecommerce-api-l7i1.onrender.com/docs)
- Frontend en vivo: [https://tienda-react-phi-liard.vercel.app](https://tienda-react-phi-liard.vercel.app)

> El backend está en un plan gratuito de Render, así que puede tardar unos segundos en "despertar" si no ha recibido tráfico recientemente.

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
├── database/        # dump del esquema (schema.sql) y certificado SSL
├── routes/
├── schemas/
├── services/
├── status/
├── utils/
├── app.py
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
git clone https://github.com/ErickDRC25/ecommerce_api.git
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

## 5. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```bash
SECRET_KEY="tu_clave_secreta"
ALGORITHM='HS256'
ACCESS_TOKEN_EXPIRED=30
DB_URL=mysql+pymysql://usuario:password@host:puerto/nombre_db
```

> Si tu base de datos requiere SSL (como ocurre con proveedores en la nube tipo Aiven), agrega `?ssl_ca=ruta/al/certificado.pem` al final del `DB_URL`.

---

## 6. Crear la base de datos

El proyecto asume que las tablas ya existen (no se crean automáticamente al iniciar la API). Para recrearlas:

1. Crea una base de datos vacía en tu motor MySQL
2. Importa el dump incluido en `database/schema.sql` (incluye estructura y datos de ejemplo)

---

## 7. Ejecutar servidor

```bash
uvicorn app:app --reload
```

---

#  Documentación Swagger

FastAPI genera documentación automática.

## Swagger UI (local)

```bash
http://127.0.0.1:8000/docs
```

---

# Despliegue

Este proyecto está desplegado usando:

- **Render** — hosting del backend (Free tier)
- **Aiven** — base de datos MySQL en la nube (Free tier)
- **Vercel** — hosting del frontend (Hobby/Free tier)

---

# Próximos pasos

- Restringir CORS al dominio real del frontend (actualmente abierto con `allow_origins=["*"]` por ser un proyecto de práctica)
- Endpoint para que un admin delegue el rol de admin a otro usuario
- Tests automatizados

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
- Despliegue en la nube (Render, Aiven, Vercel) y variables de entorno por ambiente

---

# Autor

Erick Diego Romero Cruz