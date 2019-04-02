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
    acierto = db.IntField()
    meta = {'strict': False}