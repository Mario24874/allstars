# Usa una imagen base oficial de Python
FROM python:3.8-slim-buster

# Establece un directorio de trabajo
WORKDIR /app

# Copia los archivos de requisitos e instala las dependencias
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación
COPY . .

# Expone el puerto en el que se ejecutará la aplicación
EXPOSE 8000

# Ejecuta la aplicación
CMD ["python", "main.py"]

