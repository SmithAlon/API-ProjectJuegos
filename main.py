from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel, EmailStr
import bcrypt
from datetime import datetime

# Inicializar FastAPI
app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexión a MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['your_database_name']
users_collection = db['usuarios']

# Modelos
class UserBase(BaseModel):
    username: str
    password: str

class UserRegister(UserBase):
    email: EmailStr

class UserLogin(UserBase):
    pass

# Funciones de utilidad
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

# Endpoints
@app.post("/usuarios", status_code=201)
async def register_user(user: UserRegister):
    # Verificar si el usuario ya existe
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(
            status_code=400,
            detail="El nombre de usuario ya está registrado"
        )

    # Crear documento de usuario
    user_doc = {
        "username": user.username,
        "email": user.email,
        "password": hash_password(user.password),
        "created_at": datetime.utcnow()
    }

    try:
        users_collection.insert_one(user_doc)
        return {
            "username": user.username,
            "email": user.email
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/login")
async def login(user: UserLogin):
    # Buscar usuario
    db_user = users_collection.find_one({"username": user.username})
    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Usuario o contraseña incorrectos"
        )
    
    # Verificar contraseña
    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(
            status_code=401,
            detail="Usuario o contraseña incorrectos"
        )

    # Devolver datos del usuario
    return {
        "username": db_user["username"],
        "email": db_user["email"]
    }

# Endpoint de verificación
@app.get("/usuarios")
async def check_server():
    return {"status": "ok"}