"""
WSGI config for blog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

import accessToken
import mqtt_control

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")

accessToken.CreateThread()
mqtt_control.CreateThread()

application = get_wsgi_application()
