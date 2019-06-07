from flask import Flask, Blueprint, jsonify, request, current_app, send_file
from models.institucion import Institucion
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from PIL import Image
import os
def init_module(api):
    api.add_resource(InstitucionItem, '/instituciones/<id>')
    api.add_resource(Instituciones, '/instituciones')
    api.add_resource(InstitucionIdentificador, '/institucion/identificador/<identificador>')
    api.add_resource(InstitucionImagenItem, '/institucion/imagen/<id>')
    api.add_resource(InstitucionImagenDefaultItem, '/institucion/imagen/default/<id>')

class InstitucionItem(Resource):
    def get(self, id):
        return json.loads(Institucion.objects(id=id).first().to_json())

class Instituciones(Resource):
    def get(self):
        print(Institucion.objects().all().to_json())
        return json.loads(Institucion.objects().all().to_json())

class InstitucionIdentificador(Resource):
    def get(self,identificador):
        institucion = Institucion.objects(identificador=identificador).first()
        if institucion == None:
            return {'Response': 'fracaso'}
        else:
            return {
                'Response': 'exito',
                'institucion': institucion.to_dict()
            }

class InstitucionImagenItem(Resource):
    def post(self,id):
        upload_directory = os.path.join(current_app.config.get("UPLOAD_FOLDER", "uploads"), 
                                        "instituciones")
        imagen = Image.open(request.files['imagen'].stream).convert("RGB")
        image_path = os.path.join(upload_directory, "%s.jpg" % str(id))
        imagen.save(image_path)
        imagen.thumbnail((400, 400))

        image_path = os.path.join(upload_directory, "%s_thumbnail.jpg" % str(id))
        imagen.save(image_path)
        institucion = Institucion.objects(id=id).first()
        institucion.logo = str(id)
        institucion.save()
        return {'Response': 'exito'}
    
    def get(self,id):
        upload_directory = os.path.join(current_app.config.get("UPLOAD_FOLDER", "uploads"), 
                        "instituciones")
        image_path = os.path.join(upload_directory, "%s.jpg" % str(id))
        return send_file(image_path)

class InstitucionImagenDefaultItem(Resource):
    def get(self,id):
        institucion = Institucion.objects(id=id).first()
        #path = os.path.join(current_app.config.get("UPLOAD_FOLDER"), model.carpeta_archivos)
        institucion.imagen = "default"
        institucion.save()
        return {'Response':'exito'}