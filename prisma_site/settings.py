"""Configurações do projeto Prisma."""

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY", "django-insecure-local-development-key-change-me"
)
DEBUG = os.getenv("DJANGO_DEBUG", "1") == "1"
ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,[::1],testserver"
    ).split(",")
    if host.strip()
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "portfolio.apps.PortfolioConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "prisma_site.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

WSGI_APPLICATION = "prisma_site.wsgi.application"
ASGI_APPLICATION = "prisma_site.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Limites defensivos. O proxy/web server de produção também deve limitar o corpo HTTP.
DATA_UPLOAD_MAX_MEMORY_SIZE = 2_621_440
FILE_UPLOAD_MAX_MEMORY_SIZE = 5_242_880
DATA_UPLOAD_MAX_NUMBER_FIELDS = 100

# Limite básico em aplicação; use cache compartilhado e proteção de borda em produção.
CONTACT_RATE_LIMIT = int(os.getenv("CONTACT_RATE_LIMIT", "8"))
CONTACT_RATE_WINDOW = int(os.getenv("CONTACT_RATE_WINDOW", "600"))

# Endurece cookies quando DJANGO_SECURE=1 for configurado no ambiente de produção.
SECURE_MODE = os.getenv("DJANGO_SECURE", "0") == "1"
CSRF_COOKIE_SECURE = SECURE_MODE
SESSION_COOKIE_SECURE = SECURE_MODE
SECURE_SSL_REDIRECT = SECURE_MODE
SECURE_HSTS_SECONDS = (
    int(os.getenv("DJANGO_HSTS_SECONDS", "0")) if SECURE_MODE else 0
)
SECURE_HSTS_INCLUDE_SUBDOMAINS = (
    os.getenv("DJANGO_HSTS_INCLUDE_SUBDOMAINS", "0") == "1"
)
SECURE_HSTS_PRELOAD = os.getenv("DJANGO_HSTS_PRELOAD", "0") == "1"
if os.getenv("DJANGO_BEHIND_HTTPS_PROXY", "0") == "1":
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

