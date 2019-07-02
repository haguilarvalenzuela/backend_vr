from flask import Flask, Blueprint, jsonify, request, current_app, send_file
from models.seccion import Seccion
from models.institucion import Institucion
from models.administrador import Administrador
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
from libs.auth import token_required
import json
from PIL import Image
import os
from os.path import dirname, abspath

def init_module(api):
  api.add_resource(Secciones,'/secciones/<id>')
  api.add_resource(SeccionesColegio,'/colegio/secciones')
  api.add_resource(SeccionesColegioInicio,'/colegio/secciones/<id>')
  api.add_resource(SeccionSubir,'/seccion/subir/<id>')
  api.add_resource(SeccionBajar,'/seccion/bajar/<id>')
  api.add_resource(SeccionImagenItem,'/seccion/imagen/<id>')
  api.add_resource(SeccionImagenOriginal,'/seccion/imagen/original/<id>')
  api.add_resource(SeccionImagenDefaultItem,'/seccion/imagen/default/<id>')

class SeccionSubir(Resource):
    @token_required
    def put(self,user,id):
        seccion = Seccion.objects(id=id).first()
        institucion = seccion.institucion.id
        posicion = seccion.posicion
        seccion_anterior = Seccion.objects(institucion=institucion, activo=True, posicion=posicion-1).first()
        seccion.posicion = posicion-1
        seccion_anterior.posicion = posicion
        seccion.save()
        seccion_anterior.save()
        return {'Response':'exito'}

class SeccionBajar(Resource):
    def put(self,id):
        token = request.headers.get('auth-token')
        print(token)
        user = Administrador.load_from_token(token)
        if user == None:
            return {},401
        seccion = Seccion.objects(id=id).first()
        institucion = seccion.institucion.id
        posicion = seccion.posicion
        seccion_siguiente = Seccion.objects(institucion=institucion, activo=True, posicion=posicion+1).first()
        seccion.posicion = posicion+1
        seccion_siguiente.posicion = posicion
        seccion.save()
        seccion_siguiente.save()
        return {'Response':'exito'}

class Secciones(Resource):
    def delete(self,id):
        token = request.headers.get('auth-token')
        user = Administrador.load_from_token(token)
        if user == None:
            return {},401
        seccion = Seccion.objects(id=id).first()
        institucion = seccion.institucion.id
        posicion = seccion.posicion
        seccion.activo = False
        seccion.save()
        secciones = Seccion.objects(institucion=institucion).all()
        for sec in secciones:
            if sec.activo and sec.posicion>posicion:
                sec.posicion = sec.posicion -1
                sec.save()
        return {'Response':'borrado'}
        
class SeccionesColegio(Resource):
    def get(self):
        token = request.headers.get('auth-token')
        user = Administrador.load_from_token(token)
        if user == None:
            return [],401
        institucion = Institucion.objects(id=user.institucion.id).first()   
        secciones = []
        cant_secciones = Seccion.objects(institucion = institucion.id, activo=True).count()
        posicion = 1
        for pos in range (0,cant_secciones) :
            seccion = Seccion.objects(institucion = institucion.id, posicion = pos+1, activo=True).first()
            if seccion != None and seccion.activo:
                secciones.append(seccion.to_dict())
        return secciones
    
    def put(self,id_colegio):
        data = request.data.decode()
        data = json.loads(data)
        seccion = Seccion.objects(id=data['id']).first()
        seccion.titulo = data['titulo']
        seccion.data = data['data']
        seccion.tipo = data['tipo']
        seccion.save()
        return{'Response':'exito'}
    
    def post(self,id_colegio):
        data = request.data.decode()
        data = json.loads(data)
        institucion = Institucion.objects(id=id_colegio).first()
        posicion = Seccion.objects(institucion=institucion.id, activo=True).count()+1
        seccion = Seccion()
        seccion.institucion = institucion.id
        seccion.titulo = data['titulo']
        seccion.data = data['data']
        seccion.tipo = data['tipo']
        seccion.posicion = posicion
        seccion.save()
        return{'Response':'exito', 'id':str(seccion.id)}

class SeccionImagenItem(Resource):
    def post(self,id):
        #upload_directory = os.path.join(current_app.config.get("UPLOAD_FOLDER", "uploads"), 
        #                                "secciones")

        #Para los test
        directory_root = dirname(dirname(abspath(__file__)))
        upload_directory = os.path.join(
            str(directory_root), "flaskr/uploads/secciones")
        imagen = Image.open(request.files['imagen'].stream).convert("RGB")
        image_path = os.path.join(upload_directory, "%s.jpg" % str(id))
        imagen.save(image_path)
        imagen.thumbnail((800, 800))

        image_path = os.path.join(upload_directory, "%s_thumbnail.jpg" % str(id))
        imagen.save(image_path)
        seccion = Seccion.objects(id=id).first()
        seccion.imagen = str(id)
        seccion.save()
        return {'Response': 'exito'}
    
    def get(self,id):
        #upload_directory = os.path.join(current_app.config.get("UPLOAD_FOLDER", "uploads"), 
        #                "secciones")

        #Para los test
        directory_root = dirname(dirname(abspath(__file__)))
        upload_directory = os.path.join(
            str(directory_root), "flaskr/uploads/secciones")
        image_path = os.path.join(upload_directory, "%s_thumbnail.jpg" % str(id))
        return send_file(image_path)

class SeccionImagenOriginal(Resource):
    def get(self,id):
        #upload_directory = os.path.join(current_app.config.get("UPLOAD_FOLDER", "uploads"), 
        #                "secciones")
        #Para los test
        directory_root = dirname(dirname(abspath(__file__)))
        upload_directory = os.path.join(
            str(directory_root), "flaskr/uploads/secciones")
        image_path = os.path.join(upload_directory, "%s.jpg" % str(id))
        return send_file(image_path)

class SeccionImagenDefaultItem(Resource):
    def get(self,id):
        seccion = Seccion.objects(id=id).first()
        seccion.imagen = "default"
        seccion.save()
        return {'Response':'exito'}

class SeccionesColegioInicio(Resource):
    def get(self,id):
        institucion = Institucion.objects(id=id).first()   
        secciones = []
        cant_secciones = Seccion.objects(institucion = institucion.id, activo=True).count()
        posicion = 1
        for pos in range (0,cant_secciones) :
            seccion = Seccion.objects(institucion = institucion.id, posicion = pos+1, activo=True).first()
            if seccion != None and seccion.activo:
                secciones.append(seccion.to_dict())
        return secciones
