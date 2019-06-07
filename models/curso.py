from db import db
from datetime import datetime
from models.contenido import Contenido
from models.asignatura import Asignatura
from models.institucion import Institucion
from models.alumno import Alumno
from models.profesor import Profesor
from models.grado import Grado
from models.curso_base import CursoBase
from models.categoria import Categoria
from models.habilidad import Habilidad
 
import mongoengine_goodjson as gj
class Curso(gj.Document):
    nombre = db.StringField(verbose_name="Nombre curso", max_length=200)
    fecha_creacion = db.DateTimeField(default=datetime.now)
    contenidos = db.ListField(db.EmbeddedDocumentField(Contenido))
    asignatura = db.ReferenceField(Asignatura)
    institucion = db.ReferenceField(Institucion)
    profesor = db.ReferenceField(Profesor)
    categoria = db.ReferenceField(Categoria)
    alumnos = db.ListField(db.ReferenceField(Alumno))
    activo = db.BooleanField(default=True)
    version = db.StringField(default="1.0")
    curso_base = db.ReferenceField(CursoBase)
    descripcion = db.StringField()
    aprobacion = db.IntField( default=0 )
    imagen = db.StringField()
    habilidades = db.ListField(db.ReferenceField(Habilidad))
    meta = {'strict': False }
    
    def __str__(self):
        return self.nombre
    
    
    def to_dict(self, full=True):
        data = {
            "id": str(self.id),
            "nombre": self.nombre,
            "fecha_creacion": str(self.fecha_creacion),
            "profesor": self.profesor.to_dict(),
            "activo": self.activo,
            "version": self.version,
            "descripcion": self.descripcion,
            "imagen": self.imagen,
            "curso_base": self.curso_base.to_dict(),
            "categoria": self.categoria.to_dict()
        }
        if full:
            data.update({
                "contenidos":  [x.to_dict() for x in self.contenidos],
                "asignatura":  self.asignatura.to_dict(),
                "alumnos":     [x.to_dict() for x in self.alumnos],
                "aprobacion":  self.aprobacion,
                "curso_base":  self.curso_base.to_dict(),
                "habilidades": [x.to_dict() for x in self.habilidades]
            })
        return data