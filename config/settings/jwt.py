"""Settings for JWT authentication."""
import datetime
import os

JWT_AUTH = {
    "JWT_SECRET_KEY": os.getenv("JWT_SECRET_KEY") or os.getenv("DJANGO_SECRET_KEY"),
    "JWT_EXPIRATION_DELTA": datetime.timedelta(hours=6),
    "JWT_ALLOW_REFRESH": os.getenv("JWT_ALLOW_REFRESH", "0").lower() in ("1", "true", "yes"),
    "JWT_REFRESH_EXPIRATION_DELTA": datetime.timedelta(days=1),
    "JWT_AUTH_COOKIE": os.getenv("JWT_AUTH_COOKIE", default="jwt"),
    "JWT_AUTH_COOKIE_SECURE": True,
    "JWT_AUTH_COOKIE_SAMESITE": os.getenv("JWT_AUTH_COOKIE_SAMESITE", default="Lax"),
    "JWT_AUTH_HEADER_PREFIX": os.getenv("JWT_AUTH_HEADER_PREFIX", default="Bearer"),
}
