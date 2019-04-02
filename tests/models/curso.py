from db import db
from datetime import datetime
from models.pregunta import Pregunta
from models.asignatura import Asignatura
from models.institucion import Institucion
from models.alumno import Alumno
from models.profesor import Profesor
from models.grado import Grado
from models.curso_base import CursoBase
 
import mongoengine_goodjson as gj
class Curso(gj.Document):
    nombre = db.StringField(verbose_name="Nombre curso", max_length=200)
    fecha_creacion = db.DateTimeField(default=datetime.now)
    preguntas = db.ListField(db.EmbeddedDocumentField(Pregunta))
    asignatura = db.ReferenceField(Asignatura)
    institucion = db.ReferenceField(Institucion)
    profesor = db.ReferenceField(Profesor)
    alumnos = db.ListField(db.ReferenceField(Alumno))
    grado = db.ReferenceField(Grado)
    activo = db.BooleanField(default=True)
    version = db.StringField(default="1.0")
    curso_base = db.ReferenceField(CursoBase)
    descripcion = db.StringField( max_length=200)
    meta = {'strict': False}

    def __str__(self):
        return self.nombre