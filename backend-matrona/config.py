# config.py (mejor: carga desde env vars)
from datetime import timedelta

SECRET_KEY = "cambia_esto_por_un_valor_muy_largo_y_random"  # ⚠️ poner en ENV en producción
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # ajustar según necesidad
