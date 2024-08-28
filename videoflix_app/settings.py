import os
import certifi
from pathlib import Path
from dotenv import load_dotenv

# .env-Datei laden
load_dotenv()

# Zertifikatspfad festlegen
os.environ['SSL_CERT_FILE'] = certifi.where()

# Basisverzeichnis festlegen
BASE_DIR = Path(__file__).resolve().parent.parent

# Sicherheitsrelevante Einstellungen
SECRET_KEY = os.getenv('SECRET_KEY', 'your-default-secret-key')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Hosts-Einstellungen
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'jan-woll.developerakademie.org',
    'videoflix.jan-woll.de'
]

# CORS-Einstellungen
CORS_ALLOWED_ORIGINS = [
    # 'https://localhost:4200',
    'https://jan-woll.developerakademie.org',
    'https://videoflix.jan-woll.de'
]

CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_ALLOW_ALL = True

# Installierte Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'streaming',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'django_rq',
    'user',
]

# Django RQ Einstellungen für Redis
RQ_QUEUES = {
    'default': {
        'HOST': os.getenv('REDIS_HOST', 'localhost'),
        'PORT': int(os.getenv('REDIS_PORT', 6379)),
        'DB': int(os.getenv('REDIS_DB', 0)),
        'DEFAULT_TIMEOUT': int(os.getenv('REDIS_DEFAULT_TIMEOUT', 360)),
    },
}

# Benutzerdefiniertes User Model
AUTH_USER_MODEL = 'user.CustomUser'

# REST Framework Einstellungen
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

# Middleware-Einstellungen
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL-Konfiguration
ROOT_URLCONF = 'videoflix_app.urls'

# Templates-Einstellungen
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Caching Einstellungen
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv('REDIS_CACHE_LOCATION', "redis://127.0.0.1:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "videoflix",
    }
}

# WSGI-Anwendung
WSGI_APPLICATION = 'videoflix_app.wsgi.application'

# Datenbank-Einstellungen
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / os.getenv('DB_NAME', 'db.sqlite3'),
    }
}

# Passwortvalidierung
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationale Einstellungen
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Statische Dateien
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Medien-Dateien
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Standard AutoField
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# E-Mail Einstellungen
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'your-default-email-host')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', 'False') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'your-default-email-user')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'your-default-email-password')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'your-default-from-email')
DOMAIN = os.getenv('DOMAIN', 'localhost:8000')
DOMAIN_FRONTEND = os.getenv('DOMAIN_FRONTEND', 'https://localhost:4200')


CSRF_TRUSTED_ORIGINS = [
'https://videoflix.jan-woll.de',
'https://jan-woll.developerakademie.org',
]

# ACCESS_CONTROL_ALLOW_ORIGIN = 'https://videoflix.jan-woll.de','https://jan-woll.developerakademie.org'
# ACCES_CONTROL_ALLOW_HEADERS = 'Content-Type, Authorization'
# ACCES_CONTROL_METHODS = 'GET, POST, PUT, DELETE, OPTIONS'

CORS_ALLOW_HEADERS = [
    'Content-Type',
    'Authorization',
]