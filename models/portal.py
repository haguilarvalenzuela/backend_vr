from db import db
from models.institucion import Institucion
from models.seccion import Seccion
import mongoengine_goodjson as gj
from PIL import Image
import mongoengine as me

class Portal(gj.Document):
    titulo = db.StringField(max_length=50)
    #logo = me.ImageField()
    institucion = db.ReferenceField(Institucion)
    seccion = db.ListField(db.ReferenceField(Seccion))