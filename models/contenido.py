from db import db
from datetime import datetime
from models.pregunta import Pregunta

class Contenido(db.EmbeddedDocument):
    texto = db.StringField()
    preguntas = db.ListField(db.EmbeddedDocumentField(Pregunta))
    identificador = db.IntField()
    meta = {'strict': False}

    def to_dict(self):
        preguntas = []
        for pregunta in self.preguntas:
            preguntas.append(pregunta.to_dict())
        return{
            "texto": self.texto,
            "preguntas": preguntas,
            "identificador": self.identificador
        }