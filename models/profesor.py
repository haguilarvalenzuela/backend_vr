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
    telefono = db.StringField(max_length=20)
    nombre_usuario = db.StringField(max_length=20)
    password = db.StringField(max_length=255)
    institucion = db.ReferenceField(Institucion)
    imagen = db.StringField()
    activo = db.BooleanField(default=True)
    meta = {'strict': False}

    def __str__(self):
        return self.nombres
    
    def to_dict(self):
        return{
            "id": str(self.id),
            "nombres": self.nombres,
            "apellido_paterno": self.apellido_paterno,
            "apellido_materno": self.apellido_materno,
            "email": self.email,
            "telefono": self.telefono,
            "nombre_usuario": self.nombre_usuario,
            "password": self.password,
            "imagen": self.imagen,
            "activo": self.activo
        }


    def encrypt_password(self, password_to_encrypt):
        self.password = generate_password_hash(password_to_encrypt)

    def check_password(self, password_to_check):
        return check_password_hash(self.password, str(password_to_check).strip())