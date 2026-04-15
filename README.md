# Veterinaria API

Este proyecto es una API REST para gestionar servicios, usuarios y atenciones de mascotas en una veterinaria.

## Requisitos
- Python 3.8+
- FastAPI
- Uvicorn
- Pydantic

## Instalación

1. Clona el repositorio:
   ```bash
   git clone <url-del-repo>
   cd prueba-app
   ```
2. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta el servidor:
   ```bash
   uvicorn main:app --reload
   ```

## Endpoints principales

- `POST /usuarios/registro` — Registrar usuario
- `POST /usuarios/login` — Login de usuario
- `POST /servicios` — Agregar servicio
- `GET /servicios` — Listar servicios
- `POST /atenciones` — Agregar atención
- `GET /atenciones/por-duenio/{duenio}` — Atenciones y costo total por dueño

## Ejemplos de formatos JSON

### Registro de usuario
```json
{
   "correo": "usuario@ejemplo.com",
   "contrasena": "123456"
}
```

### Login de usuario
```json
{
   "correo": "usuario@ejemplo.com",
   "contrasena": "123456"
}
```

### Agregar servicio
```json
{
   "nombre": "Vacunación",
   "costo": 250.0
}
```

### Agregar atención
```json
{
   "correo": "usuario@ejemplo.com",
   "duenio": "Juan Perez",
   "mascota": "Firulais",
   "servicio": "Vacunación",
   "fecha": "2026-04-14"
}
```

## Notas
- La base de datos es SQLite y se crea automáticamente.
- No se implementa autenticación JWT, solo validación básica de usuario.
