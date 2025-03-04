#Aquí se haran las pruebas para los endpoints de reservaciones
import pytest
from fastapi.testclient import TestClient
from main import app
from database import SessionLocal, Base, engine
from models import Reserva, Usuario, Espacio
from datetime import datetime, time

client = TestClient(app)

@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_crear_reserva(test_db):
    # Crear usuario y espacio primero
    client.post("/usuarios/", json={
        "nombre_completo": "Juan Perez",
        "cedula": "123456789",
        "apartamento": "101",
        "torre": "A"
    })
    client.post("/espacios/", json={
        "nombre": "Cancha de Futbol",
        "descripcion": "Cancha de futbol 5"
    })

    response = client.post("/reservas/", json={
        "usuario_id": 1,
        "espacio_id": 1,
        "fecha": datetime.now().isoformat(),
        "hora_inicio": time(10, 0).isoformat(),
        "hora_fin": time(11, 0).isoformat(),
        "estado": "Activa"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["usuario_id"] == 1
    assert data["espacio_id"] == 1

def test_obtener_reservas(test_db):
    response = client.get("/reservas/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_obtener_reserva_por_id(test_db):
    response = client.get("/reservas/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

def test_actualizar_reserva(test_db):
    response = client.put("/reservas/1", json={
        "usuario_id": 1,
        "espacio_id": 1,
        "fecha": datetime.now().isoformat(),
        "hora_inicio": time(11, 0).isoformat(),
        "hora_fin": time(12, 0).isoformat(),
        "estado": "Cancelada"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["estado"] == "Cancelada"

def test_eliminar_reserva(test_db):
    response = client.delete("/reservas/1")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Reserva eliminada"