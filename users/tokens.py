import jwt
from datetime import datetime, timedelta
from django.conf import settings


def create_jwt_pair_for_user(user):
    """Создание JWT access и refresh токенов"""

    payload_access = {
        "user_id": user.id,
        "exp": datetime.utcnow() + timedelta(minutes=15),
        "type": "access",
    }
    payload_refresh = {
        "user_id": user.id,
        "exp": datetime.utcnow() + timedelta(days=7),
        "type": "refresh",
    }

    access_token = jwt.encode(payload_access, settings.SECRET_KEY, algorithm="HS256")
    refresh_token = jwt.encode(payload_refresh, settings.SECRET_KEY, algorithm="HS256")

    return {"access": access_token, "refresh": refresh_token}
