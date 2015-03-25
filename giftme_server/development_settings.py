# -*- coding: utf-8 -*-
from .settings import *
DEBUG = True
SSLIFY_DISABLE = True
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
TEMPLATE_DEBUG = DEBUG
STRIPE_PUBLISHABLE = "pk_test_iQi63h5Zd5LyKJGOMGUYxRvp"
DATABASES = {
     'default': {
             'ENGINE': 'django.db.backends.postgresql_psycopg2', 
             'NAME': 'language2db',  
             'USER': 'muwawa',
             'PASSWORD': 'FMtf9whG',
             'HOST': '',  
             'PORT': '', 
         }
}
