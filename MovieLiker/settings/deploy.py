from .base import *


def read_secret(secret_name):
    file = open('/run/secrets/' + secret_name)
    secret = file.read()
    secret = secret.rstrip().lstrip()
    file.close()
    return secret


SECRET_KEY = read_secret('DJANGO_SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = ["158.247.221.120"]


# Database: Mariadb
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django',
        'USER': 'django',
        'PASSWORD': read_secret('MYSQL_ROOT_PASSWORD'),
        'HOST': 'mariadb',
        'PORT': '3306',
    }
}


# Sending Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = read_secret('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = read_secret('EMAIL_HOST_PASSWORD')
