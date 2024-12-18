from .base import *


DOMAIN = env("PRODUCTION_DOMAIN")
FRONTEND_URL = f"https://{DOMAIN}"
BASE_URL = f"https://{DOMAIN}"

DEBUG = False

ALLOWED_HOSTS = [DOMAIN, f"www.{DOMAIN}"]
STATIC_URL = "/static/"
STATIC_ROOT = env("STATIC_ROOT")
MEDIA_URL = "/media/"
MEDIA_ROOT = env("MEDIA_ROOT")

SESSION_COOKIE_DOMAIN = DOMAIN
SESSION_COOKIE_AGE = 1209600
SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_SECURE = True

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [f"https://{DOMAIN}", f"https://www.{DOMAIN}"]
CSRF_COOKIE_DOMAIN = DOMAIN
CSRF_TRUSTED_ORIGINS = [f"https://{DOMAIN}", f"https://www.{DOMAIN}"]
CSRF_COOKIE_SECURE = True

SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 0

X_FRAME_OPTIONS = "DENY"

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
]

CSP_DEFAULT_SRC = ("'none'",)
CSP_CONNECT_SRC = (
    "'self'",
    "https://api.stripe.com",
)
CSP_SCRIPT_SRC = (
    "'self'",
    "'unsafe-inline'",
    "'unsafe-eval'",
)
CSP_STYLE_SRC = (
    "'self'",
    "'unsafe-inline'",
)
CSP_IMG_SRC = (
    "'self'",
    "data:",
)
CSP_FONT_SRC = ("'self'",)
CSP_FRAME_SRC = ("'none'",)
CSP_FRAME_ANCESTORS = ("'none'",)
CSP_OBJECT_SRC = ("'none'",)
CSP_MEDIA_SRC = ("'none'",)
CSP_FORM_ACTION = ("'self'",)
CSP_WORKER_SRC = ("'none'",)
