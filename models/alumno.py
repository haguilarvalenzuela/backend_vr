from db import db
from datetime import datetime
from models.institucion import Institucion
from models.grado import Grado
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import mongoengine_goodjson as gj
import mongoengine as me
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)
from flask import (
    Blueprint,
    request,
    render_template,
    flash,
    redirect,
    url_for,
    current_app,
    abort,
    Response,
    jsonify
    )

class Alumno(gj.Document, UserMixin):
    nombres = db.StringField()
    apellido_paterno = db.StringField(max_length=20)
    apellido_materno = db.StringField(max_length=20)
    email = db.EmailField()
    telefono = db.StringField(max_length=20)
    nombre_usuario = db.StringField(max_length=20)
    password = db.StringField(max_length=255)
    matricula = db.StringField(max_length=20)
    institucion = db.ReferenceField(Institucion)
    grado = db.ReferenceField(Grado)
    imagen = db.StringField()
    activo = db.BooleanField(default=True)
    primera_vez = db.BooleanField(default = True)
    meta = {'strict': False}

    def __str__(self):
        return self.nombres

    def to_dict(self):
        if self.grado == None:
            return {
                "id": str(self.id),
                "nombres": self.nombres,
                "apellido_paterno": self.apellido_paterno,
                "apellido_materno": self.apellido_materno,
                "email": self.email,
                "telefono": self.telefono,
                "nombre_usuario": self.nombre_usuario,
                "matricula": self.matricula,
                #"grado": self.grado.to_dict(),
                "imagen": self.imagen,
                "activo": self.activo,
                "primera_vez": self.primera_vez
            }
        else:
            return {
                "id": str(self.id),
                "nombres": self.nombres,
                "apellido_paterno": self.apellido_paterno,
                "apellido_materno": self.apellido_materno,
                "email": self.email,
                "telefono": self.telefono,
                "nombre_usuario": self.nombre_usuario,
                "matricula": self.matricula,
                "grado": self.grado.to_dict(),
                "imagen": self.imagen,
                "activo": self.activo,
                "primera_vez": self.primera_vez
            }

    def encrypt_password(self, password_to_encrypt):
        self.password = generate_password_hash(password_to_encrypt)

    def check_password(self, password_to_check):
        return check_password_hash(self.password, str(password_to_check).strip())
    
    @classmethod
    def get_by_email_or_username(cls, email_or_usernmane):
        text_id = email_or_usernmane.lower()
        if '@' in text_id:
            return cls.objects.filter(email=text_id).first()
        return cls.objects.filter(username=text_id).first()

    @classmethod
    def get_by_id(cls, user_id):
        return cls.objects(id=user_id).first()
    
    # token alive 10 hours
    def get_token(self, seconds_live=36000):
        token = Serializer(current_app.config.get("TOKEN_SALT"),
                           expires_in=seconds_live)
        return str(token.dumps({'id': str(self.id)}))

    @classmethod
    def load_from_token(cls, token):
        s = Serializer(current_app.config.get("TOKEN_SALT"))
        if token[0:2] == "b'" and token[-1:] == "'":
            token = token[2:-1]
        try:
            data = s.loads(token)
            return cls.get_by_id(data['id'])
        except SignatureExpired:
            # the token has ben expired
            return None
        except BadSignature:
            # the token ist'n valid
            return None