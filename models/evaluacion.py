from db import db
from datetime import datetime
from models.institucion import Institucion
from models.alumno import Alumno
from models.curso import Curso
from models.respuesta import Respuesta
import mongoengine_goodjson as gj

class Evaluacion(gj.Document):
    alumno = db.ReferenceField(Alumno)
    institucion = db.ReferenceField(Institucion)
    curso = db.ReferenceField(Curso)
    respuestas = db.ListField(db.EmbeddedDocumentField(Respuesta))
    acierto = db.IntField(default=0)
    meta = {'strict': False}

    def to_dict(self):
        contenidos_respuesta = []
        for respuesta in self.respuestas:
            contenidos_respuesta.append(respuesta.to_dict())
        return{
            "id": str(self.id),
            "alumno": self.alumno.to_dict(),
            "curso": self.curso.to_dict(),
            "respuestas": contenidos_respuesta,
            "acierto": self.acierto
        }