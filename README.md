# API Project Juegos

Esta API proporciona endpoints para gestionar información relacionada con juegos.

## Configuración inicial

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd api-ProjectJuegos
```

2. Instalar dependencias:
```bash
npm install
```

3. Configurar variables de entorno:
- Crear archivo `.env` en la raíz del proyecto
- Añadir las siguientes variables:
```
PORT=3000
DB_URL=<tu-url-de-base-de-datos>
```

## Ejecutar la API

### Modo desarrollo:
```bash
npm run dev
```

### Modo producción:
```bash
npm start
```

## Endpoints disponibles

### Juegos
- `GET /api/games` - Obtener todos los juegos
- `GET /api/games/:id` - Obtener juego por ID
- `POST /api/games` - Crear nuevo juego
- `PUT /api/games/:id` - Actualizar juego
- `DELETE /api/games/:id` - Eliminar juego

## Consumo desde Frontend

### Ejemplo con Fetch:
```javascript
// Obtener todos los juegos
fetch('http://localhost:3000/api/games')
    .then(response => response.json())
    .then(data => console.log(data));

// Crear nuevo juego
fetch('http://localhost:3000/api/games', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        title: 'Nuevo Juego',
        genre: 'Acción',
        year: 2023
    })
});
```

### Ejemplo con Axios:
```javascript
// Obtener todos los juegos
axios.get('http://localhost:3000/api/games')
    .then(response => console.log(response.data));

// Crear nuevo juego
axios.post('http://localhost:3000/api/games', {
    title: 'Nuevo Juego',
    genre: 'Acción',
    year: 2023
});
```