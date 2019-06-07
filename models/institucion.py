from db import db
from datetime import datetime
import mongoengine_goodjson as gj

class Institucion(gj.Document):
    nombre = db.StringField(verbose_name="Nombre Institucion", max_length=200)
    fecha_creacion = db.DateTimeField(default=datetime.now)
    logo = db.StringField()
    identificador = db.StringField()

    meta = {'strict': False}

    def __str__(self):
        return self.nombre

    def to_dict(self):
        return{
            "id": str(self.id),
            "nombre": self.nombre,
            "fecha_creacion": str(self.fecha_creacion),
            "logo": self.logo,
            "identificador": self.identificador
        }