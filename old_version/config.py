# -*- coding: utf-8 -*-

DEBUG = True
SECRET_KEY = 'suqa'

# Database settings:
SQLALCHEMY_DATABASE_URI = 'postgresql://tceh:123@localhost/imageboard'
SQLALCHEMY_TRACK_MODIFICATIONS = False

WTF_CSRF_ENABLED = False
