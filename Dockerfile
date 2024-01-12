# Define la imagen base
FROM python:3.9-slim

# Actualiza los paquetes y instala las dependencias necesarias para pyodbc
RUN apt-get update && apt-get install -y g++ unixodbc-dev && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . /app

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Define el comando para ejecutar la aplicación
CMD ["gunicorn", "main:app"]
