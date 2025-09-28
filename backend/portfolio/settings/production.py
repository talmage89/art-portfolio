from .base import *

DEBUG = False

DOMAIN = env("PROD_DOMAIN", default="")
BACKEND_DOMAIN = env("PROD_BACKEND_DOMAIN", default="")

BASE_URL = f"https://{DOMAIN}"

ALLOWED_HOSTS = [BACKEND_DOMAIN]

# Assumes backend is subdomain
SESSION_COOKIE_DOMAIN = f".{DOMAIN}"
SESSION_COOKIE_AGE = 1209600
SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "Lax"

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [f"https://{DOMAIN}"]

# Assumes backend is subdomain
CSRF_COOKIE_DOMAIN = f".{DOMAIN}"
CSRF_TRUSTED_ORIGINS = [
    f"https://{BACKEND_DOMAIN}",
    f"https://{DOMAIN}",
]
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "Lax"

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
    "https://storage.googleapis.com",
)
CSP_FONT_SRC = ("'self'",)
CSP_FRAME_SRC = ("'none'",)
CSP_FRAME_ANCESTORS = ("'none'",)
CSP_OBJECT_SRC = ("'none'",)
CSP_MEDIA_SRC = ("'none'",)
CSP_FORM_ACTION = ("'self'",)
CSP_WORKER_SRC = ("'none'",)
