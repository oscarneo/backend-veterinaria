from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import date
import sqlite3

app = FastAPI()

# Database setup
conn = sqlite3.connect('veterinaria.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS servicios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    costo REAL NOT NULL
)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    correo TEXT NOT NULL UNIQUE,
    contrasena TEXT NOT NULL
)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS atenciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    correo TEXT NOT NULL,
    duenio TEXT NOT NULL,
    mascota TEXT NOT NULL,
    servicio TEXT NOT NULL,
    fecha TEXT NOT NULL
)''')
conn.commit()

# Pydantic models
class ServicioIn(BaseModel):
    nombre: str
    costo: float

class ServicioOut(BaseModel):
    id: int
    nombre: str
    costo: float


class UsuarioRegistro(BaseModel):
    correo: str
    contrasena: str

class UsuarioLogin(BaseModel):
    correo: str
    contrasena: str

class AtencionIn(BaseModel):
    correo: str
    duenio: str
    mascota: str
    servicio: str
    fecha: date

class AtencionOut(BaseModel):
    id: int
    duenio: str
    mascota: str
    servicio: str
    fecha: date

# Endpoints
@app.post("/servicios", response_model=ServicioOut)
def agregar_servicio(servicio: ServicioIn):
    cursor.execute("INSERT INTO servicios (nombre, costo) VALUES (?, ?)", (servicio.nombre, servicio.costo))
    conn.commit()
    servicio_id = cursor.lastrowid
    return {"id": servicio_id, **servicio.dict()}

@app.get("/servicios", response_model=List[ServicioOut])
def listar_servicios():
    cursor.execute("SELECT id, nombre, costo FROM servicios")
    servicios = cursor.fetchall()
    return [{"id": s[0], "nombre": s[1], "costo": s[2]} for s in servicios]


# Endpoint para registrar usuario
@app.post("/usuarios/registro")
def registrar_usuario(usuario: UsuarioRegistro):
    try:
        cursor.execute("INSERT INTO usuarios (correo, contrasena) VALUES (?, ?)", (usuario.correo, usuario.contrasena))
        conn.commit()
        return {"ok": True, "msg": "Usuario registrado"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

# Endpoint para login de usuario
@app.post("/usuarios/login")
def login_usuario(usuario: UsuarioLogin):
    cursor.execute("SELECT contrasena FROM usuarios WHERE correo = ?", (usuario.correo,))
    row = cursor.fetchone()
    if row and row[0] == usuario.contrasena:
        return {"ok": True}
    else:
        return {"ok": False, "error": "Credenciales incorrectas"}

# Actualizar endpoint de agregar atención para incluir correo
@app.post("/atenciones", response_model=AtencionOut)
def agregar_atencion(atencion: AtencionIn):
    # Verificar que el usuario existe
    cursor.execute("SELECT id FROM usuarios WHERE correo = ?", (atencion.correo,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    cursor.execute(
        "INSERT INTO atenciones (correo, duenio, mascota, servicio, fecha) VALUES (?, ?, ?, ?, ?)",
        (atencion.correo, atencion.duenio, atencion.mascota, atencion.servicio, atencion.fecha.isoformat())
    )
    conn.commit()
    atencion_id = cursor.lastrowid
    return {"id": atencion_id, **atencion.dict()}

# Endpoint para mostrar atenciones de todas las mascotas por dueño y el costo total
@app.get("/atenciones/por-duenio/{duenio}")
def atenciones_por_duenio(duenio: str):
    cursor.execute("""
        SELECT a.mascota, a.servicio, a.fecha, s.costo
        FROM atenciones a
        JOIN servicios s ON a.servicio = s.nombre
        WHERE a.duenio = ?
    """, (duenio,))
    rows = cursor.fetchall()
    atenciones = []
    total = 0.0
    for mascota, servicio, fecha, costo in rows:
        atenciones.append({
            "mascota": mascota,
            "servicio": servicio,
            "fecha": fecha,
            "costo": costo
        })
        total += costo
    return {"duenio": duenio, "atenciones": atenciones, "costo_total": total}
