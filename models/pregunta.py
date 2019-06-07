from db import db
from datetime import datetime
from models.alternativa import Alternativa
from models.habilidad import Habilidad

TIPOS_PREGUNTA = [
    ("TEXTO", "TEXTO"),
    ("ALTERNATIVA", "ALTERNATIVA"),
    ("VERDADERO_FALSO", "VERDADERO_FALSO"),
    ("COMPLETAR_TEXTO", "COMPLETAR_TEXTO"),
    ("UNIR_IMAGENES", "UNIR_IMAGENES"),
    ("UNIR_TEXTOS", "UNIR_TEXTOS"),
    ("UNIR_IMAGEN_TEXTO", "UNIR_IMAGEN_TEXTO"),
    ]
class Pregunta(db.EmbeddedDocument):
    texto = db.StringField()
    tipo_pregunta = db.StringField()
    alternativas = db.ListField(db.EmbeddedDocumentField(Alternativa))
    habilidad = db.ReferenceField(Habilidad)
    numero = db.IntField()
    imagen = db.StringField()
    meta = {'strict': False}

    def to_dict(self):
        habilidad = ""
        if self.habilidad != None:
            habilidad = self.habilidad.to_dict()
        alternativas = []
        for alternativa in self.alternativas:
            alternativas.append(alternativa.to_dict())
        return{
            "texto": self.texto,
            "tipo_pregunta": self.tipo_pregunta,
            "alternativas": alternativas,
            "habilidad": habilidad,
            "numero": self.numero
        }