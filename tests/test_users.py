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

def test_obtener_usuario_por_id(test_db):
    response = client.get("/usuarios/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

def test_actualizar_usuario(test_db):
    response = client.put("/usuarios/1", json={
        "nombre_completo": "Juan Perez Actualizado",
        "cedula": "123456789",
        "apartamento": "102",
        "torre": "B"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["nombre_completo"] == "Juan Perez Actualizado"

def test_eliminar_usuario(test_db):
    response = client.delete("/usuarios/1")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Usuario eliminado"