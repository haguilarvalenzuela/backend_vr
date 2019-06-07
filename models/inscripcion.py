from db import db
from datetime import datetime
from models.alumno import Alumno
from models.curso import Curso
from models.historial import Historial
import mongoengine_goodjson as gj

TIPOS_ESTADO_INSCRIPCION = [
    ("ENVIADA", "ENVIADA"),
    ("REVISION", "REVISION"),
    ("ACEPTADA", "ACEPTADA"),
    ("RECHAZADA", "RECHAZADA")
    ]

class Inscripcion(gj.Document):
    alumno = db.ReferenceField(Alumno)
    curso = db.ReferenceField(Curso)
    estado = db.StringField(choices=TIPOS_ESTADO_INSCRIPCION)
    historial = db.ListField(db.EmbeddedDocumentField(Historial))
    meta = {'strict': False}

    def to_dict(self):
        historiales=[]
        for historial in self.historial:
            historiales.append(historial.to_dict())
        return{
            "id": str(self.id),
            "alumno": self.alumno.to_dict(),
            "curso": self.curso.to_dict(),
            "estado": self.estado,
            "historial": historiales
        }