from flask import Flask, Blueprint, jsonify, request,current_app, send_file
from models.profesor import Profesor
from models.administrador import Administrador
from models.curso import Curso
from models.institucion import Institucion
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json
from PIL import Image
import os
from os.path import dirname, abspath

def init_module(api):
    api.add_resource(ProfesorItem, '/profesores/<id>')
    api.add_resource(Profesores, '/profesores')
    api.add_resource(ProfesorCursos, '/profesor/recursos/<id>')
    api.add_resource(ProfesorImagenItem, '/profesor/imagen/<id>')
    api.add_resource(ProfesorImagenDefaultItem, '/profesor/imagen/default/<id>')
    api.add_resource(ProfesoresColegio, '/profesores/colegio/<id_institucion>')
    api.add_resource(ProfesoresToken, '/profesores/token/<token>')
    api.add_resource(ProfesorFinalizarTutorial, '/profesor/finalizar/tutorial/<id>')

class ProfesorFinalizarTutorial(Resource):
    def get(self,id):
        profesor = Profesor.objects(id=id).first()
        profesor.primera_vez = False
        profesor.save()
        return{'Response':'exito'}

class ProfesoresColegio(Resource):
    def get(self, id_institucion):
        institucion = Institucion.objects(id = id_institucion).first()
        profesores = []
        for profesor in Profesor.objects(institucion = id_institucion).all():
            profesores.append(profesor.to_dict())
        return profesores

    def post(self, id_institucion):
        data = request.data.decode()
        data = json.loads(data)
        profesor = Profesor()
        profesor.nombres = data['nombres']
        profesor.apellido_paterno = data['apellido_paterno']
        profesor.apellido_materno = data['apellido_materno']
        profesor.telefono = data['telefono']
        profesor.email = data['email']
        profesor.nombre_usuario = data['nombre_usuario']
        profesor.password = data['nombre_usuario']
        institucion = Institucion.objects(id = id_institucion).first()
        profesor.institucion = institucion.id
        profesor.save()
        return {'Response': 'exito' , 'id': str(profesor.id)}

class ProfesorItem(Resource):
    def get(self, id):
        return json.loads(Profesor.objects(id=id).first().to_json())
    
    def delete(self, id):
        profesor = Profesor.objects(id=id).first()
        profesor.activo = False
        profesor.save()
        return{'Response':'borrado'}

    def put(self, id):        
        data = request.data.decode()
        data = json.loads(data)
        profesor = Profesor.objects(id=id).first()
        profesor.nombres = data['nombres']
        profesor.apellido_paterno = data['apellido_paterno']
        profesor.apellido_materno = data['apellido_materno']
        profesor.telefono = data['telefono']
        profesor.email = data['email']
        profesor.nombre_usuario = data['nombre_usuario']
        profesor.save()
        return{'Response':'exito'}


class ProfesorCursos(Resource):
    def get(self, id):
        return json.loads(Curso.objects(profesor=id).all().to_json())



class Profesores(Resource):
    def get(self):
        profesores = []
        for profesor in Profesor.objects().all():
            if profesor.activo:
                profesores.append(profesor.to_dict())
        return profesores


class ProfesoresToken(Resource):
    def post(self,token):
        data = request.data.decode()
        data = json.loads(data)
        token = token
        if Administrador.load_from_token(token) != None:
            profesor = Profesor()
            profesor.nombres = data['nombres']
            profesor.apellido_paterno = data['apellido_paterno']
            profesor.apellido_materno = data['apellido_materno']
            profesor.telefono = data['telefono']
            profesor.email = data['email']
            profesor.nombre_usuario = data['nombre_usuario']
            profesor.encrypt_password(data['nombre_usuario'])
            profesor.save()
            return {'Response': 'exito' , 'id': str(profesor.id)}
        else:
            return {'Response': 'fracaso'}
        

class ProfesorImagenItem(Resource):
    def post(self,id):
        #########
        # Se usa el siguiente os.path.join para los tests
        #########
        directory_root = dirname(dirname(abspath(__file__)))
        upload_directory = os.path.join(str(directory_root), "flaskr/uploads/profesores")

        imagen = Image.open(request.files['imagen'].stream).convert("RGB")
        imagen.save(os.path.join(upload_directory, str(id)+".jpg"))
        imagen.thumbnail((200, 100))
        imagen.save(os.path.join(upload_directory, str(id)+'_thumbnail.jpg'))
        profesor = Profesor.objects(id=id).first()
        profesor.imagen = str(id)
        profesor.save()
        return {'Response': 'exito'}
    
    def get(self,id):
        return send_file('uploads/profesores/'+id+'_thumbnail.jpg')

class ProfesorImagenDefaultItem(Resource):
    def get(self,id):
        profesor = Profesor.objects(id=id).first()
        profesor.imagen = "default"
        profesor.save()
        return {'Response':'exito'}
