#Aquí se haran las pruebas para los endpoints de espacios
import pytest
from fastapi.testclient import TestClient
from main import app
from database import SessionLocal, Base, engine
from models import Espacio

client = TestClient(app)

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_crear_espacio(test_db):
    response = client.post("/espacios/", json={
        "nombre": "Cancha de Futbol",
        "descripcion": "Cancha de futbol 5"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Cancha de Futbol"
    assert data["descripcion"] == "Cancha de futbol 5"

def test_obtener_espacios(test_db):
    response = client.get("/espacios/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_obtener_espacio_por_id(test_db):
    response = client.get("/espacios/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

def test_actualizar_espacio(test_db):
    response = client.put("/espacios/1", json={
        "nombre": "Cancha de Futbol Actualizada",
        "descripcion": "Cancha de futbol 5 actualizada"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Cancha de Futbol Actualizada"

def test_eliminar_espacio(test_db):
    response = client.delete("/espacios/1")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Espacio eliminado"