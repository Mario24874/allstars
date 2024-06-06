import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from main import download_images, save_images, create_s3_client, app
import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo.env
load_dotenv()

# Acceso a las variables de entorno
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
API_KEY = os.getenv('API_KEY')
NOMBRE_DEL_BUCKET = os.getenv('NOMBRE_DEL_BUCKET')

# Mock del DataFrame para pruebas
df = pd.DataFrame({
    'id_del_campo': [1, 2, 3],
    'lat': [37.7749, 34.0522, 40.7128],
    'lon': [-122.4194, -118.2437, -74.0060],
    'dim': [100, 200, 300]
})

@pytest.fixture(scope="function")
def client():
    yield TestClient(app)

@patch("aiohttp.ClientSession.get", new_callable=AsyncMock)
def test_download_images(mock_get, client):
    mock_get.return_value.__aenter__.return_value.__aexit__.return_value = b"mocked_image_data"
    images = asyncio.run(download_images())
    assert len(images) == len(df)
    assert b"mocked_image_data" in images[0]

@patch("main.create_s3_client")
def test_save_images(mock_create_s3_client, client):
    mock_s3 = mock_create_s3_client.return_value
    mock_s3.put_object.side_effect = lambda *args, **kwargs: None
    save_images([b"mocked_image_data"])
    mock_s3.put_object.assert_called_with(
        Body=b"mocked_image_data",
        Bucket=NOMBRE_DEL_BUCKET,
        Key="mock_key"
    )

def test_read_image(client):
    path = "/imagenes/mock_field_id"
    response = client.get(path)
    assert response.status_code == 200
    # Aquí puedes añadir más verificaciones específicas sobre el contenido de la respuesta
