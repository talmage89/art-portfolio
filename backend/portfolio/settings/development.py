from .base import *

SERVER_IP = os.getenv("SERVER_IP")
PRODUCTION_DOMAIN = os.getenv("PRODUCTION_DOMAIN")


DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", SERVER_IP, PRODUCTION_DOMAIN]
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
