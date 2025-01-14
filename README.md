# Autos en Linea Backend 🚀

## Descripción del Proyecto

"Autos en Línea" es una plataforma diseñada para facilitar la compra y venta de vehículos en línea. Este repositorio alberga el código fuente del backend, implementado principalmente en Python, que proporciona las funcionalidades necesarias para gestionar usuarios, vehículos, publicaciones y transacciones.

## Estructura del Repositorio

La estructura principal del repositorio es la siguiente:

- **api/**: Contiene los controladores y rutas de las APIs.
- **app/**: Incluye la configuración de la aplicación y la inicialización de componentes.
- **config/**: Archivos de configuración para diferentes entornos.
- **data/**: Archivos relacionados con la base de datos y modelos de datos.
- **utils/**: Funciones utilitarias y helpers utilizados en la aplicación.
- **main.py**: Punto de entrada principal de la aplicación.
- **requirements.txt**: Lista de dependencias necesarias para ejecutar la aplicación.
- **Dockerfile**: Archivo para la creación de la imagen Docker de la aplicación.


## Uso de las APIs

La aplicación expone una serie de endpoints para interactuar con las diferentes funcionalidades. A continuación, se detallan algunos de los principales endpoints:

- **Autenticación**:
  - `POST /api/auth/login`: Inicia sesión y obtiene un token de autenticación.
  - `POST /api/auth/register`: Registra un nuevo usuario.

- **Gestión de Vehículos**:
  - `GET /api/vehicles`: Obtiene una lista de vehículos disponibles.
  - `POST /api/vehicles`: Crea una nueva entrada de vehículo.
  - `GET /api/vehicles/{id}`: Obtiene detalles de un vehículo específico.
  - `PUT /api/vehicles/{id}`: Actualiza la información de un vehículo.
  - `DELETE /api/vehicles/{id}`: Elimina un vehículo.

- **Gestión de Usuarios**:
  - `GET /api/users`: Obtiene una lista de usuarios.
  - `GET /api/users/{id}`: Obtiene detalles de un usuario específico.
  - `PUT /api/users/{id}`: Actualiza la información de un usuario.
  - `DELETE /api/users/{id}`: Elimina un usuario.

Para una descripción completa de todos los endpoints y sus parámetros, consulte la documentación de la API.


## Guía de las APIs

Puedes descargar la guía completa de las APIs en formato PDF haciendo clic en el siguiente enlace:

[![Descargar Guía de las APIs](https://img.shields.io/badge/Descargar%20Guía%20API-PDF-blue?style=for-the-badge)](https://github.com/CrisisTecno/autos_en_linea_api/data/endpoints-ael-.pdf)

## Uso de las Endpoints con Ejemplos
---

## **Autenticación**
Endpoints relacionados con el manejo de usuarios y su autenticación.

### **1. Login**
- **Endpoint**: `POST /api/auth/login`
- **Descripción**: Permite a los usuarios iniciar sesión y obtener un token de autenticación.
- **Body (JSON)**:
  ```json
  {
    "email": "usuario@example.com",
    "password": "contraseña123"
  }
  ```
- **Respuesta exitosa (200)**:
  ```json
  {
    "token": "jwt_token_generado"
  }
  ```
- **Errores comunes**:
  - 401: Credenciales incorrectas.

---

### **2. Registro**
- **Endpoint**: `POST /api/auth/register`
- **Descripción**: Registra un nuevo usuario en el sistema.
- **Body (JSON)**:
  ```json
  {
    "name": "Nombre Usuario",
    "email": "usuario@example.com",
    "password": "contraseña123"
  }
  ```
- **Respuesta exitosa (201)**:
  ```json
  {
    "message": "Usuario creado exitosamente",
    "user": {
      "id": 1,
      "name": "Nombre Usuario",
      "email": "usuario@example.com"
    }
  }
  ```
- **Errores comunes**:
  - 400: El correo electrónico ya está registrado.

---

## **Gestión de Vehículos**
Endpoints relacionados con la creación, lectura, actualización y eliminación de vehículos.

### **1. Listar Vehículos**
- **Endpoint**: `GET /api/vehicles`
- **Descripción**: Devuelve una lista de todos los vehículos disponibles.
- **Parámetros opcionales**:
  - `brand`: Filtrar por marca (e.g., `brand=Toyota`).
  - `model`: Filtrar por modelo (e.g., `model=Corolla`).
  - `year`: Filtrar por año (e.g., `year=2022`).
- **Respuesta exitosa (200)**:
  ```json
  [
    {
      "id": 1,
      "brand": "Toyota",
      "model": "Corolla",
      "year": 2022,
      "price": 20000,
      "description": "Vehículo en excelentes condiciones."
    },
    {
      "id": 2,
      "brand": "Honda",
      "model": "Civic",
      "year": 2021,
      "price": 19000,
      "description": "Poco uso, único dueño."
    }
  ]
  ```

---

### **2. Crear un Vehículo**
- **Endpoint**: `POST /api/vehicles`
- **Descripción**: Permite registrar un nuevo vehículo.
- **Body (JSON)**:
  ```json
  {
    "brand": "Toyota",
    "model": "Camry",
    "year": 2023,
    "price": 25000,
    "description": "Auto completamente nuevo, sin uso."
  }
  ```
- **Respuesta exitosa (201)**:
  ```json
  {
    "id": 3,
    "brand": "Toyota",
    "model": "Camry",
    "year": 2023,
    "price": 25000,
    "description": "Auto completamente nuevo, sin uso."
  }
  ```
- **Errores comunes**:
  - 400: Parámetros faltantes o inválidos.

---

### **3. Detalles de un Vehículo**
- **Endpoint**: `GET /api/vehicles/{id}`
- **Descripción**: Obtiene los detalles de un vehículo específico.
- **Respuesta exitosa (200)**:
  ```json
  {
    "id": 1,
    "brand": "Toyota",
    "model": "Corolla",
    "year": 2022,
    "price": 20000,
    "description": "Vehículo en excelentes condiciones."
  }
  ```
- **Errores comunes**:
  - 404: Vehículo no encontrado.

---

### **4. Actualizar un Vehículo**
- **Endpoint**: `PUT /api/vehicles/{id}`
- **Descripción**: Actualiza la información de un vehículo específico.
- **Body (JSON)**:
  ```json
  {
    "price": 19500,
    "description": "Recién ajustado, excelente estado."
  }
  ```
- **Respuesta exitosa (200)**:
  ```json
  {
    "id": 1,
    "brand": "Toyota",
    "model": "Corolla",
    "year": 2022,
    "price": 19500,
    "description": "Recién ajustado, excelente estado."
  }
  ```
- **Errores comunes**:
  - 404: Vehículo no encontrado.

---

### **5. Eliminar un Vehículo**
- **Endpoint**: `DELETE /api/vehicles/{id}`
- **Descripción**: Elimina un vehículo de la base de datos.
- **Respuesta exitosa (200)**:
  ```json
  {
    "message": "Vehículo eliminado exitosamente."
  }
  ```
- **Errores comunes**:
  - 404: Vehículo no encontrado.

---

## **Gestión de Usuarios**
Endpoints para la administración de usuarios.

### **1. Listar Usuarios**
- **Endpoint**: `GET /api/users`
- **Descripción**: Obtiene una lista de todos los usuarios registrados (requiere privilegios de administrador).
- **Respuesta exitosa (200)**:
  ```json
  [
    {
      "id": 1,
      "name": "Usuario 1",
      "email": "user1@example.com"
    },
    {
      "id": 2,
      "name": "Usuario 2",
      "email": "user2@example.com"
    }
  ]
  ```

---

### **2. Actualizar un Usuario**
- **Endpoint**: `PUT /api/users/{id}`
- **Descripción**: Actualiza la información de un usuario.
- **Body (JSON)**:
  ```json
  {
    "name": "Nuevo Nombre",
    "email": "nuevo_email@example.com"
  }
  ```
- **Respuesta exitosa (200)**:
  ```json
  {
    "id": 1,
    "name": "Nuevo Nombre",
    "email": "nuevo_email@example.com"
  }
  ```

---

### **3. Eliminar un Usuario**
- **Endpoint**: `DELETE /api/users/{id}`
- **Descripción**: Elimina un usuario de la base de datos.
- **Respuesta exitosa (200)**:
  ```json
  {
    "message": "Usuario eliminado exitosamente."
  }
  ```

---

