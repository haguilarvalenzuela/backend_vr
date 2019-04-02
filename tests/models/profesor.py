from db import db
from datetime import datetime
from models.institucion import Institucion
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import mongoengine_goodjson as gj

class Profesor(gj.Document, UserMixin):
    nombres = db.StringField(max_length=20)
    apellido_paterno = db.StringField(max_length=20)
    apellido_materno = db.StringField(max_length=20)
    email = db.EmailField()
    telefono = db.StringField(max_length=12)
    nombre_usuario = db.StringField(max_length=20)
    password = db.StringField(max_length=255)
    institucion = db.ReferenceField(Institucion)
    meta = {'strict': False}

    def __str__(self):
        return self.nombres


    def encrypt_password(self, password_to_encrypt):
        self.password = generate_password_hash(password_to_encrypt)

    def check_password(self, password_to_check):
        return check_password_hash(self.password, str(password_to_check).strip())