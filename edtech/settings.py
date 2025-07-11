from pathlib import Path
import os
from urllib.parse import urlparse
from dotenv import load_dotenv
from supabase import create_client


BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY = 'django-insecure-9wy1_vxo)x@mudw$t75+d+f-g42y=nc0ku%kx(&(yt&eei)kg&'
SECRET_KEY = 'fez7JZik8RoyWwFNIMYrcsmeL49oAutr4JZqoSYyjzsy7ylxEQ-1-QRKbOb5CI5UL_M'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'localhost', '127.0.0.1',
    'ed-tech-3u7zvn5yf-kishorekumars-projects-f69373c8.vercel.app',
    '.vercel.app',
    'db.supabase.co',
    'db.ogfopexbppxzxnmbsqxe.supabase.co',
    
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'course',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'course.middleware.StudentUserMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'edtech.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], 
        #changed
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

WSGI_APPLICATION = 'edtech.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


load_dotenv()
SUPABASE_STORAGE_URL = os.getenv('SUPABASE_STORAGE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
if not SUPABASE_STORAGE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase URL or Key is missing in environment variables.")

supabase = create_client(SUPABASE_STORAGE_URL, SUPABASE_KEY)



POSTGRES_URL = os.getenv('POSTGRES_URL')
url = urlparse(POSTGRES_URL)
DATABASES = {
    
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres', 
        'USER': 'postgres.ogfopexbppxzxnmbsqxe',
        'PASSWORD': 'edtech0603KK',
        'HOST': 'aws-0-ap-south-1.pooler.supabase.com',
        'PORT': '5432',
    }

    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': url.path[1:],  # Only the database name (e.g., 'postgres')
    #     'USER': url.username,
    #     'PASSWORD': url.password,
    #     'HOST': url.hostname,
    #     'PORT': url.port,
    # }
}



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/' 
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  
STATICFILES_DIRS = [
    BASE_DIR / "static", 
]

MEDIA_URL = '/media/'  
MEDIA_ROOT = BASE_DIR / 'media'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')
# STATIC_URL = 'static/'
# MEDIA_URL =  '/img/'
# MEDIA_ROOT = BASE_DIR/'static'

# STATICFILES_DIRS = [
#     BASE_DIR / "static",
# ]
# # STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
# # Default primary key field type
# # https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# settings.py

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 14400  # Ensures the session does not have a fixed timeout
SESSION_SAVE_EVERY_REQUEST = True  # Prevents extending the session on each request

LOGIN_URL = '/login/'



SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
