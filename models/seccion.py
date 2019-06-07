from db import db
from datetime import datetime
import mongoengine_goodjson as gj
from models.institucion import Institucion

TIPOS_SECCIONES = [
    ("BANNER", "BANNER"),
    ("QUIENES_SOMOS", "QUIENES_SOMOS"),
    ("CONTACTO", "CONTACTO"),
    ("INFORMACION_1", "INFORMACION_1"),
    ("INFORMACION_2", "INFORMACION_2"),
    ("INFORMACION_3", "INFORMACION_3")
    ]
class Seccion(gj.Document):
    titulo = db.StringField(max_length=30)
    descripcion = db.StringField()
    data = db.StringField()
    imagen = db.StringField()
    activo = db.BooleanField(default=True)
    tipo = db.StringField(choices=TIPOS_SECCIONES)
    posicion = db.IntField()
    institucion = db.ReferenceField(Institucion)
    meta = {'strict': False}

    def __str__(self):
        return self.titulo

    def to_dict(self):
        institucion = ""
        if self.institucion != None:
            institucion = self.institucion.to_dict()
        return {
            "id": str(self.id),
            "titulo": self.titulo,
            "data": self.data,
            "imagen": self.imagen,
            "activo": self.activo,
            "tipo": self.tipo,
            "institucion": institucion,
            "posicion": self.posicion
        }

    def asignarPosicion(self,id):
        institucion = Institucion.objects(id=id).first()
        posicion = 0
        for seccion in Seccion.objects(institucion = institucion.id).all():
            if seccion.activo:
                if posicion<seccion.posicion:
                    posicion = seccion.posicion
        self.posicion = posicion+1
        return True 


