from db import db
from datetime import datetime
from models.institucion import Institucion
import mongoengine_goodjson as gj

class Categoria(gj.Document):
    nombre = db.StringField(verbose_name="Nombre Categoria", max_length=200)
    activo = db.BooleanField(default=True)
    imagen = db.StringField()
    meta = {'strict': False}

    def __str__(self):
        return self.nombre

    def to_dict(self):
        return {
            "id": str(self.id),
            "nombre": self.nombre,
            "activo": self.activo,
            "imagen": self.imagen
        }