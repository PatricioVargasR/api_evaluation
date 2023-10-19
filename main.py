from fastapi import FastAPI
import sqlite3
from pydantic import BaseModel, EmailStr

## Rama original ya terminada

# Crea la base de datos
conn = sqlite3.connect("contactos.db")

app = FastAPI()

class Contacto(BaseModel):
    email : EmailStr
    nombres : str
    telefono : str

# Rutas para las operaciones CRUD

@app.post("/contactos")
async def crear_contacto(contacto: Contacto):
    """Crea un nuevo contacto."""
    connection = conn.cursor()
    connection.execute('INSERT INTO contactos (email, nombre, telefono) VALUES (?, ?, ?)',
              (contacto.email, contacto.nombres, contacto.telefono))
    conn.commit()
    return contacto

@app.get("/contactos")
async def obtener_contactos():
    """Obtiene todos los contactos."""
    c = conn.cursor()
    c.execute('SELECT * FROM contactos')
    response = []
    for row in c:
        response.append(row)
    return response

@app.get("/contactos/{email}")
async def obtener_contacto(email: str):
    """Obtiene un contacto por su email."""
    # Consulta el contacto por su email
    co = conn.cursor()
    co.execute('SELECT * FROM contactos WHERE email = ?', (email,))
    for row in co:
        contacto = row
    return contacto

@app.put("/contactos/{email}")
async def actualizar_contacto(email: EmailStr, contacto: Contacto):
    """Actualiza un contacto."""
    c = conn.cursor()
    c.execute('UPDATE contactos SET nombre = ?, telefono = ? WHERE email = ?',
              (contacto.nombres, contacto.telefono, email))
    conn.commit()
    return contacto


@app.delete("/contactos/{email}")
async def eliminar_contacto(email: str):
    """Elimina un contacto."""
    print(email)
    connection = conn.cursor()
    connection.execute(f"DELETE FROM contactos WHERE email = ?", (email,))
    conn.commit()
    return {"Borrado con exito"}
