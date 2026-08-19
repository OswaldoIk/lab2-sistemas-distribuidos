from fastapi import FastAPI
import sqlite3
import httpx
from datetime import datetime

app = FastAPI()

DB_PATH = "servidor2.db"
NOMBRE_SERVIDOR = "Servidor 2"
IP_SERVIDOR = "192.168.56.20"
PEER_IP = "192.168.56.10"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            dato TEXT,
            fecha TEXT,
            origen TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.get("/identidad")
def identidad():
    return {"servidor": NOMBRE_SERVIDOR, "ip": IP_SERVIDOR}

@app.get("/estado")
def estado():
    return {"servidor": NOMBRE_SERVIDOR, "estado": "activo"}

@app.post("/registro")
def registrar(nombre: str, dato: str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO registros (nombre, dato, fecha, origen) VALUES (?, ?, ?, ?)",
        (nombre, dato, datetime.now().isoformat(), NOMBRE_SERVIDOR)
    )
    conn.commit()
    conn.close()
    return {"mensaje": "registrado", "atendido_por": NOMBRE_SERVIDOR}

@app.get("/registros")
def consultar():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute("SELECT id, nombre, dato, fecha, origen FROM registros")
    filas = cur.fetchall()
    conn.close()
    return {
        "atendido_por": NOMBRE_SERVIDOR,
        "registros": [
            {"id": r[0], "nombre": r[1], "dato": r[2], "fecha": r[3], "origen": r[4]}
            for r in filas
        ]
    }

@app.get("/estado_peer")
def estado_peer():
    try:
        r = httpx.get(f"http://{PEER_IP}:8000/estado", timeout=3.0)
        return {
            "consultado_desde": NOMBRE_SERVIDOR,
            "peer_ip": PEER_IP,
            "peer_respuesta": r.json()
        }
    except Exception as e:
        return {
            "consultado_desde": NOMBRE_SERVIDOR,
            "peer_ip": PEER_IP,
            "error": f"No se pudo contactar al peer: {str(e)}"
        }
