import os
from dotenv import load_dotenv
import pandas as pd
import boto3
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import aiohttp
import asyncio
from moto import mock_aws
from datetime import datetime
import pytz

# Carga las variables de entorno
load_dotenv()

# Crea la aplicación FastAPI
app = FastAPI()

# Lee el archivo CSV
try:
    df = pd.read_csv('campos.csv')
except Exception as e:
    print(f"Error al leer el archivo CSV: {e}")
    raise e

# Crea el cliente de S3
@mock_aws
def create_s3_client():
    return boto3.client('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))

# Función asíncrona para descargar las imágenes
async def download_image(session, url):
    async with session.get(url) as response:
        return await response.read()

# Para cada fila en el DataFrame
async def download_images():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for index, row in df.iterrows():
            id_del_campo, lat, lon, dim = row
            url = f"https://api.nasa.gov/planetary/earth/imagery?lon={lon}&lat={lat}&dim={dim}&date={datetime.now(pytz.UTC).strftime('%Y-%m-%d')}&api_key={os.getenv('API_KEY')}"
            tasks.append(download_image(session, url))
        images = await asyncio.gather(*tasks)
    return images

# Guarda las imágenes en S3
def save_images(images):
    s3 = create_s3_client()
    for i, image in enumerate(images):
        id_del_campo = df.iloc[i]['id_del_campo']
        try:
            s3.put_object(Body=image, Bucket=os.getenv('NOMBRE_DEL_BUCKET'), Key=f"{id_del_campo}/{datetime.now(pytz.UTC).strftime('%Y-%m-%d')}_imagery.png")
        except Exception as e:
            print(f"Error al guardar la imagen en S3: {e}")
            raise e

# Ejecuta las funciones
images = asyncio.run(download_images())
save_images(images)

@app.get("/imagenes/{id_del_campo}")
def read_image(id_del_campo: str):
    # Devuelve la imagen del bucket de S3
    try:
        # Aquí necesitamos obtener la imagen de S3 y guardarla localmente para poder devolverla con FileResponse
        with open(f"{id_del_campo}_{datetime.now(pytz.UTC).strftime('%Y-%m-%d')}_imagery.png", 'wb') as f:
            s3 = create_s3_client()
            s3.download_fileobj(os.getenv('NOMBRE_DEL_BUCKET'), f"{id_del_campo}/{datetime.now(pytz.UTC).strftime('%Y-%m-%d')}_imagery.png", f)
        return FileResponse(path=f"{id_del_campo}_{datetime.now(pytz.UTC).strftime('%Y-%m-%d')}_imagery.png", media_type="image/png")  # Corrección del tipo MIME a "image/png"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener la imagen: {e}")
