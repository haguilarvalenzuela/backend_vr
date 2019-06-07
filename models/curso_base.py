from db import db
from datetime import datetime
from models.contenido import Contenido
from models.institucion import Institucion
from models.categoria import Categoria
from models.habilidad import Habilidad
 
import mongoengine_goodjson as gj
class CursoBase(gj.Document):
    nombre = db.StringField(verbose_name="Nombre curso", max_length=200)
    descripcion = db.StringField()
    fecha_creacion = db.DateTimeField(default=datetime.now)
    contenidos = db.ListField(db.EmbeddedDocumentField(Contenido))
    institucion = db.ReferenceField(Institucion)
    categoria = db.ReferenceField(Categoria)
    habilidades = db.ListField(db.ReferenceField(Habilidad)) 

    imagen = db.StringField()
    meta = {'strict': False}

    def __str__(self):
        return self.nombre
    
    def to_dict(self):
        contenidos = []
        for contenido in self.contenidos:
            contenidos.append(contenido.to_dict())

        habilidades = []
        for habilidad in self.habilidades:
            habilidades.append(habilidad.to_dict())

        return{
            "id": str(self.id),
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "fecha_creacion": str(self.fecha_creacion),
            "contenidos": contenidos,
            "imagen": self.imagen,
            "categoria": self.categoria.to_dict(),
            "habilidades": habilidades
        }