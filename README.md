# API Project Juegos

Esta API desarrollada en Python proporciona endpoints para gestionar información relacionada con juegos.

## Configuración inicial

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd api-ProjectJuegos
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
venv\Scripts\activate     # En Windows
```

3. Instalar dependencias:
```bash
pip install fastapi uvicorn sqlalchemy python-dotenv
```

4. Configurar variables de entorno:
- Crear archivo `.env` en la raíz del proyecto
- Añadir las siguientes variables:
```
DATABASE_URL=postgresql://user:password@localhost/dbname
```

## Ejecutar la API

Para iniciar el servidor:
```bash
uvicorn main:app --port 5000
```

## Estructura del Proyecto

### Interfaces (Modelos Pydantic)
```python
class GameBase(BaseModel):
    title: str
    genre: str
    year: int

class GameCreate(GameBase):
    pass

class Game(GameBase):
    id: int
    class Config:
        orm_mode = True
```

## Endpoints disponibles

### Juegos
- `GET /api/games` - Obtener todos los juegos
- `GET /api/games/{game_id}` - Obtener juego por ID
- `POST /api/games` - Crear nuevo juego
- `PUT /api/games/{game_id}` - Actualizar juego
- `DELETE /api/games/{game_id}` - Eliminar juego

## Consumo desde Frontend

### Ejemplo con Python Requests:
```python
import requests

# Obtener todos los juegos
response = requests.get('http://localhost:5000/api/games')
games = response.json()

# Crear nuevo juego
new_game = {
    "title": "Nuevo Juego",
    "genre": "Acción",
    "year": 2023
}
response = requests.post('http://localhost:5000/api/games', json=new_game)
```

### Documentación API
La documentación interactiva estará disponible en:
- Swagger UI: `http://localhost:5000/docs`
- ReDoc: `http://localhost:5000/redoc`