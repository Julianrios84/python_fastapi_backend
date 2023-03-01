# Dos formas de ejecutar fastapi
  1. uvicorn main:app
  2. agregar las lineas de codigo
    if __name__ == "__main__":
      uvicorn.run("main:app", port=8000)
    
    y luego correr el comando -> python main.py


# Alembic
1. En la base del proyecto ejecutamos -> alembic init migrations
2. En el archivo 'alembic.ini' eliminamos el contenido de la variable 'sqlalchemy.url'
3. En la carpeta 'migrations/env.py 
  from core.config import settings
  config.set_main_option('sqlalchemy.url', settings.DATABASE_URL)

  from app.database.model.schema import base
  target_metadata = base.metadata

4. Ejecutamos el comando -> alembic revision --autogenerate -m "Nombre de la migracion"