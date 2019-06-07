from db import db
from datetime import datetime

class Respuesta(db.EmbeddedDocument):
    correcta = db.BooleanField(default=False)
    numero_pregunta = db.IntField()
    data = db.StringField()
    meta = {'strict': False}

    def to_dict(self):
        return{
            "correcta": self.correcta,
            "numero_pregunta": self.numero_pregunta,
            "data": self.data
        }