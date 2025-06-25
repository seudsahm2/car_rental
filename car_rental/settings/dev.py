
from .common import *

# ======================
# SECURITY CONFIGURATION
# ======================
DEBUG = True

# Generate a proper secret key if not in environment
DEFAULT_SECRET_KEY = 'django-insecure-' + os.urandom(50).hex()
SECRET_KEY = os.getenv('SECRET_KEY', DEFAULT_SECRET_KEY)

DEV_HOSTS = ['localhost', '127.0.0.1']
ENV_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',') if os.getenv('ALLOWED_HOSTS') else []
ALLOWED_HOSTS = list(set(DEV_HOSTS + ENV_HOSTS))
CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'http://127.0.0.1:8000'] + [f"http://{host}" for host in ENV_HOSTS if host]

# Relaxed security for development
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_PROXY_SSL_HEADER = None
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Google AdSense and Analytics
GOOGLE_ADSENSE_PUBLISHER_ID = os.getenv('GOOGLE_ADSENSE_PUBLISHER_ID', '')
GOOGLE_ANALYTICS_PROPERTY_ID = os.getenv('GOOGLE_ANALYTICS_PROPERTY_ID', '')

# =============
# DATABASE CONFIG
# =============
REMOTE_DB = os.getenv('REMOTE_DB', 'False').lower() in ('true', '1', 'yes')

if REMOTE_DB:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('SUPABASE_DB_NAME', 'postgres'),
            'USER': os.getenv('SUPABASE_DB_USER', 'seud'),
            'PASSWORD': os.getenv('SUPABASE_DB_PASSWORD', '12345678'),
            'HOST': os.getenv('SUPABASE_DB_HOST', 'aws-0-eu-north-1.pooler.supabase.com'),
            'PORT': os.getenv('SUPABASE_DB_PORT', '6543'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# =============
# MEDIA CONFIG
# =============
if REMOTE_DB:
    MEDIA_URL = f"{SUPABASE_URL}/storage/v1/object/public/car-images/"

# =============
# CORS SETTINGS
# =============
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://sudocarreental.netlify.app",
] + [f"https://{host}" for host in ALLOWED_HOSTS if host != '*']
CORS_ALLOW_CREDENTIALS = True

# Update TEMPLATES to include debug
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
