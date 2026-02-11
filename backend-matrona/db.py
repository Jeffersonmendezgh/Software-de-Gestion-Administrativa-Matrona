# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URL



engine = create_engine(DATABASE_URL, pool_recycle=3600, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base() #clase base para todos los modelos sqlalchemy

def get_db():
    db = SessionLocal()#nueva sesion en db
    try:
        yield db #yield entrega la sesion al endpoint
    finally:
        db.close()#cierra siempre la session