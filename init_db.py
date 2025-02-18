from database import engine, Base
import models

# Crea las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Verifica que las tablas se hayan creado
from sqlalchemy import inspect

inspector = inspect(engine)
tables = inspector.get_table_names()
print("Tablas creadas:", tables)