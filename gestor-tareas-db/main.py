from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# VULNERABILIDAD INTENCIONAL PARA SEMGREP (se conserva para la prueba)
SECRET_API_KEY = "mi_clave_secreta_super_insegura_12345"

# Conexión a MongoDB Atlas
MONGO_URI = "mongodb+srv://serralerolo_db_user:t2KhuMNvqD2w8Qsy@cluster0.5miiieo.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client["gestor_db"]
collection = db["tareas"]

# Montar la carpeta static para que FastAPI sirva el frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

class Tarea(BaseModel):
    titulo: str
    descripcion: str

@app.get("/")
async def home():
    return FileResponse("static/index.html")

@app.get("/tareas")
async def obtener_tareas():
    tareas = []
    for tarea in collection.find():
        tareas.append({"id": str(tarea["_id"]), "titulo": tarea["titulo"], "descripcion": tarea["descripcion"]})
    return tareas

@app.post("/tareas")
async def crear_tarea(tarea: Tarea):
    resultado = collection.insert_one(tarea.dict())
    return {"mensaje": "Tarea creada con éxito", "id": str(resultado.inserted_id)}