# Monitoreo de Campos con Satélites

Este proyecto utiliza imágenes satelitales públicas de la constelación Landsat 8 de NASA para monitorear campos. Las imágenes se proporcionan a través de la API de la Tierra de NASA.

## Requisitos

- Python 3.8+
- Docker
- Una cuenta de AWS y un bucket de S3

## Instalación

1. Clona este repositorio en tu máquina local.
2. Navega al directorio del proyecto.
3. Crea un entorno virtual de Python con `python -m venv venv`.
4. Activa el entorno virtual.
5. Instala las dependencias del proyecto con `pip install -r requirements.txt`.

## Configuración

Crea un archivo `.env` en el directorio raíz del proyecto y añade las siguientes variables de entorno:

```bash
AWS_ACCESS_KEY_ID=tu_access_key_id
AWS_SECRET_ACCESS_KEY=tu_secret_access_key
NOMBRE_DEL_BUCKET=nombre_del_bucket
API_KEY=tu_api_key

Reemplaza tu_access_key_id, tu_secret_access_key, nombre_del_bucket y tu_api_key con tus propias credenciales de AWS y la API de la Tierra de NASA.

Ejecución
Para ejecutar el proyecto, utiliza el siguiente comando:
python main.py

Pruebas
Para ejecutar las pruebas del proyecto, utiliza el siguiente comando desde el directorio raiz:
pytest
