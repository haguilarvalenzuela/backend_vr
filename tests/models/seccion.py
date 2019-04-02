from db import db
from datetime import datetime
import mongoengine_goodjson as gj

TIPOS_SECCIONES = [
    ("BANNER", "BANNER"),
    ("QUIENES_SOMOS", "QUIENES_SOMOS"),
    ("CONTACTO", "CONTACTO"),
    ("SLIDE", "SLIDE"),
    ("CURSOS", "CURSOS"),
    ("INFORMACION_1", "INFORMACION_1"),
    ("INFORMACION_2", "INFORMACION_2"),
    ]
class Seccion(gj.Document):
    titulo = db.StringField(max_length=30)
    descripcion = db.StringField()
    data = db.StringField()
    #imagen = db.ImageField()
    activo = db.BooleanField(default=True)
    tipo = db.StringField(choices=TIPOS_SECCIONES)
    meta = {'strict': False}

    def __str__(self):
        return self.titulo