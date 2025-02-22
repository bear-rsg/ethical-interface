"""
Settings that are specific to this particular instance of the project.
This can contain sensitive information (such as keys) and should not be shared with others.

REMEMBER: If modfiying the content of this file, reflect the changes in local_settings.example.py
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create a SECRET_KEY.
# Online tools can help generate this for you, e.g. https://www.miniwebtool.com/django-secret-key-generator/
SECRET_KEY = ''

# Set to True if in development, or False is in production
DEBUG = True/False

# Set to ['*'] if in development, or specific IP addresses and domains if in production
ALLOWED_HOSTS = ['*']/['ethical-interface.bham.ac.uk']

# Provide the email address for the site admin (e.g. the researcher/research team)
ADMIN_EMAIL = '...@bham.ac.uk'

# Set the database name below
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'ethical-interface.sqlite3'),
        'TEST': {
            'NAME': os.path.join(BASE_DIR, 'ethical-interface_TEST.sqlite3'),
        },
    }
}
