# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Install system dependencies required for Pyodbc and curl
RUN apt-get update \
    && apt-get install -y --no-install-recommends gnupg g++ unixodbc-dev curl

# Add Microsoft repository using the new recommended approach
RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /usr/share/keyrings/msprod.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/msprod.gpg] https://packages.microsoft.com/debian/10/prod buster main" > /etc/apt/sources.list.d/mssql-release.list

# Install Microsoft ODBC Driver for SQL Server
RUN apt-get update \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql17

# Clean up the apt cache to reduce image size
RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable
ENV NAME World

# Define el comando para ejecutar la aplicación
CMD ["gunicorn", "main:app"]
