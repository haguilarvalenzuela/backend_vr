from db import db
from datetime import datetime
from models.institucion import Institucion
import mongoengine_goodjson as gj

class Asignatura(gj.Document):
    nombre = db.StringField(verbose_name="Nombre Asignatura", max_length=200)
    institucion = db.ReferenceField(Institucion)
    activo = db.BooleanField(default=True)

    meta = {'strict': False}

    def __str__(self):
        return self.nombre

    def to_dict(self):
        return {
                "nombre": self.nombre,
                "institucion": self.institucion.nombre,
                "activo": self.activo}