# Sistema Distribuido de Registro y Consulta

Guía de Laboratorio 2 — Comunicación en Sistemas Distribuidos (UMB)

## Arquitectura

Dos servidores independientes, cada uno con la misma API REST (FastAPI + SQLite), conectados mediante una red virtual Host-Only (VirtualBox) y capaces de consultarse entre sí.

| | Servidor 1 | Servidor 2 |
|---|---|---|
| SO | Ubuntu Server 26.04 LTS | Windows Server 2022 Standard |
| Kernel | Linux 7.0.0-30-generic | Windows NT (Build 20348) |
| IP | 192.168.56.10 | 192.168.56.20 |
| Puerto | 8000 | 8000 |

Ver el diagrama completo y el manual de instalación en `Manual_Laboratorio2_Sistemas_Distribuidos.docx`.

## Estructura del repositorio

```
.
├── servidor1/          # Código desplegado en Ubuntu Server
│   ├── main.py
│   └── requirements.txt
├── servidor2/          # Código desplegado en Windows Server
│   ├── main.py
│   └── requirements.txt
└── README.md
```

El código de `servidor1/main.py` y `servidor2/main.py` es idéntico salvo el nombre del servidor y las IPs propia/del peer.

## Ejecución

En cada servidor:

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/identidad` | Nombre e IP del servidor |
| GET | `/estado` | Estado de actividad del servidor |
| POST | `/registro` | Registra información (`nombre`, `dato`) |
| GET | `/registros` | Consulta los registros almacenados |
| GET | `/estado_peer` | Consulta el estado del servidor par vía HTTP |
