import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from main import app
from db import get_db
from db import Base
from models import Rol


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    # insertar roles necesarios para los tests
    roles = [
        Rol(id_rol=1, nombre_rol="administrador"),
        Rol(id_rol=2, nombre_rol="empleado"),
        Rol(id_rol=3, nombre_rol="cliente")
    ]

    db.add_all(roles)
    db.commit()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

#test cliente, permite simular como si fuera peticiones HTTP reales
@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()