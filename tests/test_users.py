#Aquí se haran las pruebas para los endpoints de usuarios
import pytest
from fastapi.testclient import TestClient
from main import app
from database import SessionLocal, Base, engine
from models import Usuario

client = TestClient(app)

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_crear_usuario(test_db):
    response = client.post("/usuarios/", json={
        "nombre_completo": "Juan Perez",
        "cedula": "123456789",
        "apartamento": "101",
        "torre": "A"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["nombre_completo"] == "Juan Perez"
    assert data["cedula"] == "123456789"

def test_obtener_usuarios(test_db):
    response = client.get("/usuarios/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0