# C:\Users\hp\Downloads\Projects\Django\car_rental_backend\car_rental\settings\__init__.py
import os

# Default to development if DJANGO_ENV is not set
env = os.getenv('DJANGO_ENV', 'development')

if env == 'production':
    from .prod import *
else:
    from .dev import *