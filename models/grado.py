from db import db
from datetime import datetime
from models.institucion import Institucion
 
import mongoengine_goodjson as gj
class Grado(gj.Document):
    institucion = db.ReferenceField(Institucion)
    nivel = db.IntField()
    identificador = db.StringField(max_length=5)
    def __str__(self):
        return str(self.nivel)+"°"+self.identificador

    def getGrado(self):
        return str(self.nivel)+"°"+self.identificador