from db import db
from datetime import datetime
from models.pregunta import Pregunta
from models.institucion import Institucion
 
import mongoengine_goodjson as gj
class CursoBase(gj.Document):
    nombre = db.StringField(verbose_name="Nombre curso", max_length=200)
    descripcion = db.StringField(max_length=200)
    fecha_creacion = db.DateTimeField(default=datetime.now)
    preguntas = db.ListField(db.EmbeddedDocumentField(Pregunta))
    institucion = db.ReferenceField(Institucion)
    meta = {'strict': False}

    def __str__(self):
        return self.nombre