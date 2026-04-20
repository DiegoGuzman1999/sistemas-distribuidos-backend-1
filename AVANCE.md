# AVANCE — sistemas-distribuidos-backend-1

## ¿Qué hace este repositorio?
Es el microservicio de **autenticación**. Se encarga únicamente de login y logout. El frontend le pregunta a este servicio si las credenciales son correctas antes de dejar entrar al usuario.

---

## ¿Por qué está separado del inventario?
Porque es un sistema distribuido con microservicios: cada servicio hace una sola cosa. Si el inventario falla, el login sigue funcionando y viceversa.

---

## Estructura del repositorio

```
sistemas-distribuidos-backend-1/
├── app/
│   ├── __init__.py   ← Crea la app Flask y conecta la BD
│   ├── models.py     ← Define la tabla usuarios
│   └── routes.py     ← Endpoints de login, logout y verificar
├── run.py            ← Punto de entrada para correr el servidor
├── requirements.txt  ← Dependencias Python
├── Dockerfile        ← Imagen Docker del servicio
├── docker-compose.yml← Para correr solo este servicio
└── AVANCE.md         ← Este archivo
```

---

## Endpoints disponibles

| Método | Ruta        | Descripción                              |
|--------|-------------|------------------------------------------|
| GET    | /health     | Verifica que el servicio está corriendo  |
| POST   | /login      | Inicia sesión con usuario y contraseña   |
| POST   | /logout     | Cierra la sesión activa                  |
| GET    | /verificar  | Comprueba si hay una sesión activa       |

### Ejemplo de login
**Request:**
```json
POST /login
{ "username": "admin", "password": "admin123" }
```
**Response exitosa:**
```json
{ "mensaje": "Login exitoso", "username": "admin", "rol": "admin" }
```
**Response fallida:**
```json
{ "error": "Credenciales incorrectas" }
```

---

## Puerto
Este servicio corre en el puerto **5000**.

---

## Historial de cambios

| Fecha      | Rama | Descripción                                    |
|------------|------|------------------------------------------------|
| 2026-04-20 | dev  | Estructura inicial: API Flask de autenticación |
