from .common import *

# ======================
# SECURITY CONFIGURATION
# ======================
DEBUG = False

# Generate a proper secret key if not in environment
DEFAULT_SECRET_KEY = 'django-insecure-' + os.urandom(50).hex()
SECRET_KEY = os.getenv('SECRET_KEY', DEFAULT_SECRET_KEY)

ENV_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',') if os.getenv('ALLOWED_HOSTS') else []
ALLOWED_HOSTS = list(set(ENV_HOSTS)) or ['car-rental-pi48.onrender.com']
CSRF_TRUSTED_ORIGINS = [f'https://{host}' for host in ALLOWED_HOSTS if host and host != '*'] + [f'http://{host}' for host in ALLOWED_HOSTS if host and host != '*']

# Strict security for production
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Google AdSense and Analytics
GOOGLE_ADSENSE_PUBLISHER_ID = os.getenv('GOOGLE_ADSENSE_PUBLISHER_ID', '')
GOOGLE_ANALYTICS_PROPERTY_ID = os.getenv('GOOGLE_ANALYTICS_PROPERTY_ID', '')

# =============
# DATABASE CONFIG
# =============
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

# =============
# MEDIA CONFIG
# =============
MEDIA_URL = f"{SUPABASE_URL}/storage/v1/object/public/car-images/"

# =============
# CORS SETTINGS
# =============
CORS_ALLOWED_ORIGINS = [
    "https://sudocarreental.netlify.app",
    "http://127.0.0.1:5501",
] + [f"https://{host}" for host in ALLOWED_HOSTS if host != '*']
CORS_ALLOW_CREDENTIALS = True

# Update TEMPLATES to include debug
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
