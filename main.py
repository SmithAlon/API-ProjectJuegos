from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel, EmailStr
import bcrypt
import hashlib
from datetime import datetime
import os
from base64 import b64encode

# Add these constants at the top of the file after imports
USERNAME_SALT = b64encode(b'fixed_salt_for_usernames_123').decode('utf-8')
EMAIL_SALT = b64encode(b'fixed_salt_for_emails_456').decode('utf-8')
# Add after existing salt constants
PASSWORD_SALT = b64encode(b'fixed_salt_for_passwords_789').decode('utf-8')

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
db = client['JuegosProject']
users_collection = db['usuarios']

# Modelos
class UserBase(BaseModel):
    username: str
    password: str

class UserRegister(UserBase):
    email: EmailStr

class UserLogin(BaseModel):
    username: str
    password: str
    passwordLength: int | None = None  # Make it optional since it's not always needed

# Funciones de utilidad
def hash_username(username: str) -> str:
    return hashlib.sha256((username + "fixed_salt_for_usernames_123").encode()).hexdigest()

def hash_email(email: str) -> str:
    return hashlib.sha256((email + "fixed_salt_for_emails_456").encode()).hexdigest()

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
    except Exception as e:
        print(f"Password verification error: {str(e)}")
        return False

def verify_username(plain_username: str, hashed_username: str) -> bool:
    return hash_username(plain_username) == hashed_username

def verify_email(plain_email: str, hashed_email: str) -> bool:
    return hash_email(plain_email) == hashed_email

def validate_password(password: str) -> bool:
    if not password or len(password) < 8:
        return False
    return True

@app.post("/usuarios", status_code=201)
async def register_user(user: UserRegister):
    print(f"Registration attempt for username: {user.username}")
    
    # Verificar si el usuario ya existe
    hashed_username = hash_username(user.username)
    if users_collection.find_one({"username": hashed_username}):
        raise HTTPException(
            status_code=400,
            detail="El nombre de usuario ya está registrado"
        )

    # Hash the password
    hashed_password = hash_password(user.password)
    print(f"Password hashed successfully for user: {user.username}")

    # Crear documento de usuario
    user_doc = {
        "username": hashed_username,
        "email": hash_email(user.email),
        "password": hashed_password,
        "created_at": datetime.utcnow()
    }

    try:
        users_collection.insert_one(user_doc)
        print(f"User registered successfully: {user.username}")
        return {
            "username": user.username,
            "email": user.email
        }
    except Exception as e:
        print(f"Error during user registration: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/login")
async def login(user: UserLogin):
    try:
        print("\n=== Login Request Received ===")
        print(f"Username attempting login: {user.username}")
        
        # Hash username for lookup
        hashed_username = hash_username(user.username)
        print(f"Hashed username for lookup: {hashed_username}")
        
        # Find user in database
        db_user = users_collection.find_one({"username": hashed_username})
        print(f"User found in database: {bool(db_user)}")
        
        if not db_user:
            raise HTTPException(
                status_code=401,
                detail="Usuario o contraseña incorrectos"
            )
        
        # Debug password verification
        print(f"Stored hashed password: {db_user['password']}")
        print(f"Attempting to verify password: {user.password}")
        is_valid = verify_password(user.password, db_user["password"])
        print(f"Password verification result: {is_valid}")
        
        if not is_valid:
            raise HTTPException(
                status_code=401,
                detail="Usuario o contraseña incorrectos"
            )

        return {
            "username": user.username,
            "email": db_user.get("email", ""),
            "message": "Login exitoso"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error during login: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor"
        )

# Add this endpoint to check users in the database
@app.get("/debug/users")
async def debug_users():
    users = list(users_collection.find({}, {
        "username": 1,
        "email": 1,
        "_id": 0
    }))
    return {"users": users}

# Endpoint de verificación
@app.get("/usuarios")
async def check_server():
    return {"status": "ok"}