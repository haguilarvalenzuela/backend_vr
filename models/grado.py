from db import db
from datetime import datetime
from models.institucion import Institucion
from models.profesor import Profesor 

import mongoengine_goodjson as gj
class Grado(gj.Document):
    institucion = db.ReferenceField(Institucion)
    nivel = db.IntField()
    identificador = db.StringField(max_length=5)
    activo = db.BooleanField(default=True)
    profesor = db.ReferenceField(Profesor)

    def __str__(self):
        return str(self.nivel)+"°"+self.identificador

    def getGrado(self):
        return str(self.nivel)+"°"+self.identificador
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "nivel": self.nivel,
            "identificador": self.identificador,
            "activo": self.activo
        }