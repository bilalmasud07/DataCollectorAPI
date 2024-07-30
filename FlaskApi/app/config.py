import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg://CyberCube:Cube.159@localhost:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'