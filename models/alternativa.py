from db import db
from datetime import datetime

class Alternativa(db.EmbeddedDocument):
    texto = db.StringField()
    texto_secundario = db.StringField()
    correcta = db.BooleanField(default=False)
    meta = {'strict': False}

    def to_dict(self):
        return{
            "texto": self.texto,
            "correcta": self.correcta
        }