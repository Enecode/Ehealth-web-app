from .general import *

DEBUG = False

chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
new_secret = ''.join(secrets.choice(chars) for i in range(50))
SECRET_KEY = 'new_secret'

ALLOWED_HOSTS = []


