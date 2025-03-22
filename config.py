import os
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")

    SECRET_KEY = os.environ.get("SECRET_KEY")

    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")


    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")

    WTF_CSRF_ENABLED = os.environ.get("WTF_CSRF_ENABLED")

    SECURITY_TOKEN_AUTHENTICATION_HEADER = os.environ.get("SECURITY_TOKEN_AUTHENTICATION_HEADER")

    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER")

    STATIC_FOLDER = os.environ.get("STATIC_FOLDER")

    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

    JWT_BLACKLIST_ENABLED = os.environ.get("JWT_BLACKLIST_ENABLED")

    JWT_BLACKLIST_TOKEN_CHECKS =  os.environ.get("JWT_BLACKLIST_TOKEN_CHECKS")

    SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE")

    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
class DevelopmentConfig(Config):
    DEBUG = True
