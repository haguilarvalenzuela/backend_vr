from db import db
from datetime import datetime
from models.alternativa import Alternativa

TIPOS_PREGUNTA = [
    ("TEXTO", "TEXTO"),
    ("PREGUNTA", "PREGUNTA"),
    ("VERDADERO_FALSO", "VERDADERO_FALSO"),
    ("COMPLETAR_TEXTO", "COMPLETAR_TEXTO"),
    ("UNIR_IMAGENES", "UNIR_IMAGENES"),
    ("UNIR_TEXTOS", "UNIR_TEXTOS"),
    ("UNIR_IMAGEN_TEXTO", "UNIR_IMAGEN_TEXTO"),
    ]
class Pregunta(db.EmbeddedDocument):
    texto = db.StringField()
    tipo_pregunta = db.StringField(choices=TIPOS_PREGUNTA)
    alternativas = db.ListField(db.EmbeddedDocumentField(Alternativa))
    meta = {'strict': False}