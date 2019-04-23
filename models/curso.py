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
    aprobacion = db.IntField( default=0 )
    imagen = db.StringField()
    meta = {'strict': False }
    
    def __str__(self):
        return self.nombre
    
    def to_dict(self):
        preguntas = []
        for pregunta in self.preguntas:
            preguntas.append(pregunta.to_dict())
        
        alumnos = []
        for alumno in self.alumnos:
            alumnos.append(alumno.to_dict())
        return{
            "id": str(self.id),
            "nombre": self.nombre,
            "fecha_creacion": str(self.fecha_creacion),
            "preguntas": preguntas,
            "asignatura": self.asignatura.to_dict(),
            "profesor": self.profesor.to_dict(),
            "alumnos": alumnos,
            "grado": self.grado.to_dict(),
            "activo": self.activo,
            "version": self.version,
            "descripcion": self.descripcion,
            "aprobacion": self.aprobacion,
            "imagen": self.imagen
        }