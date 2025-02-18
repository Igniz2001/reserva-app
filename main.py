#Este es el script principal de la aplicación

from fastapi import FastAPI
from routes import users, spaces, reservations

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "¡La aplicación está funcionando!"}

app.include_router(users.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(spaces.router, prefix="/espacios", tags=["Espacios"])
app.include_router(reservations.router, prefix="/reservas", tags=["Reservas"])