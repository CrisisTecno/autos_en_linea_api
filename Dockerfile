# Define la imagen base
# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Install system dependencies required for Pyodbc and Microsoft ODBC Driver
RUN apt-get update && apt-get install -y --no-install-recommends \
        gnupg \
        g++ \
        unixodbc-dev \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql17 \
    # Clean up the apt cache to reduce image size
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define el comando para ejecutar la aplicación
CMD ["gunicorn", "main:app"]
