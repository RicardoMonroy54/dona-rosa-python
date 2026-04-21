# Inventario Dona Rosa Bot - Python

**Sistema de inventario desarrollado con FastAPI, SQLite y Telegram Bot**, diseñado para administrar productos de una tienda de barrio de forma sencilla, rápida y sin instalar aplicaciones adicionales.

## Descripción

Este proyecto es la migración a Python del sistema original desarrollado en Java con Spring Boot. Mantiene la misma lógica de negocio y funcionalidades, adaptadas al ecosistema Python.

La solución implementa un **bot de Telegram** conectado a un backend construido con **FastAPI**, encargado de procesar la lógica de negocio, calcular el valor total del inventario, identificar productos con stock crítico y permitir operaciones de administración como **agregar, actualizar y eliminar productos**.

## Tecnologías utilizadas

- **Python 3.14**
- **FastAPI** - framework web (equivalente a Spring Boot)
- **Uvicorn** - servidor ASGI (equivalente a Tomcat embebido)
- **SQLAlchemy** - ORM (equivalente a Spring Data JPA)
- **SQLite** - base de datos local (equivalente a H2)
- **python-telegram-bot** - integración con Telegram
- **Pydantic** - validación de datos (equivalente a Jakarta Validation)
- **python-dotenv** - variables de entorno (equivalente a application.properties)

## Arquitectura del proyecto

```text
Usuario en Telegram
        │
        ▼
   Telegram Bot
        │
        ▼
  FastAPI Backend
        │
        ▼
  Base de Datos SQLite
```

## Estructura del proyecto

```text
dona-rosa-python/
├── models/
│   ├── __init__.py
│   └── producto.py
├── repository/
│   ├── __init__.py
│   └── producto_repository.py
├── service/
│   ├── __init__.py
│   └── producto_service.py
├── controller/
│   ├── __init__.py
│   └── producto_controller.py
├── config/
│   ├── __init__.py
│   ├── data_loader.py
│   └── telegram_bot.py
├── imagenes/
├── database.py
├── main.py
└── .env
```

## Configuración

En el archivo `.env` configura el token del bot:

```
TELEGRAM_BOT_TOKEN=TU_TOKEN_REAL
```

## Instalación y ejecución

### Requisitos previos

- Python 3.10 o superior
- Cuenta de Telegram
- Bot creado en BotFather

### Pasos para ejecutar

1. Clonar el proyecto
2. Instalar dependencias:

```bash
pip install fastapi uvicorn sqlalchemy python-telegram-bot pydantic python-dotenv
```

3. Configurar el archivo `.env` con el token del bot
4. Ejecutar la aplicación:

```bash
python -m uvicorn main:app --reload
```

5. Abrir Telegram, buscar el bot y probarlo

## Funcionalidades del bot

- **/start** - Muestra los comandos disponibles
- **/productos** - Lista el inventario actual
- **/valor** - Muestra el valor total del inventario
- **/stockbajo** - Lista productos con stock crítico
- **/agregar codigo nombre precio cantidad** - Inserta un producto nuevo
- **/actualizar nombre cantidad** - Actualiza la cantidad de un producto
- **/eliminar nombre** - Elimina un producto del inventario

## API REST

- `GET /productos`
- `GET /productos/{id}`
- `POST /productos`
- `PUT /productos/{id}`
- `DELETE /productos/{id}`
- `GET /productos/stock-bajo`
- `GET /productos/valor-total`

## Reglas de negocio

- No se permiten productos con precio menor o igual a cero
- No se permiten cantidades negativas
- No se permiten productos duplicados por código
- No se permiten productos duplicados por nombre
- El stock crítico se detecta cuando la cantidad actual es menor o igual al 10% de la cantidad inicial
- El valor total se calcula multiplicando precio por cantidad y sumando todos los productos

## Evidencias de funcionamiento

### Inicio del bot
![inicio](imagenes/inicio.png)

### Comando /start
![start](imagenes/start.png)

### Comando /productos y /valor
![productos](imagenes/productos.png)

### Comando /valor
![valor](imagenes/valor.png)

### Comando /stockbajo
![stockbajo](imagenes/stockbajo.png)

### Alerta stock bajo
![stockbajo aviso](imagenes/stockbajo_aviso.png)

### Comando /agregar
![agregar](imagenes/agregar.png)

### Comando /actualizar
![actualizar](imagenes/actualizar.png)

### Comando /eliminar
![eliminar](imagenes/eliminar.png)

## Autor

**Ricardo Monroy**

## Firma de desarrollo

```python
# ---------------------------------------------------------------
# Código migrado de Java a Python por: Ricardo Monroy
# Si no entiendes cómo funciona, no es un bug.
# Probablemente es tecnología demasiado avanzada.
# ---------------------------------------------------------------
```