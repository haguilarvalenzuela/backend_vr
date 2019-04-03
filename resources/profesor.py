from flask import Flask, Blueprint, jsonify, request
from models.profesor import Profesor
from models.curso import Curso
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json

def init_module(api):
    api.add_resource(ProfesorItem, '/profesores/<id>')
    api.add_resource(Profesores, '/profesores')
    api.add_resource(ProfesorCursos, '/profesor_cursos/<id>')

class ProfesorItem(Resource):
    def get(self, id):
        return json.loads(Profesor.objects(id=id).first().to_json())
    
    def delete(self, id):
        profesor = Profesor.objects(id=id).first()
        profesor.delete()
        return{'Response':'borrado'}

    def put(self, id):        
        data = request.data.decode()
        data = json.loads(data)

        profesor = Profesor.objects(id=id).first()

        if(profesor.check_password(data['current_password'])==False):
            return {'Response': 'no_password'}

        profesor.telefono = data['telefono']
        profesor.email = data['email']
        profesor.nombre_usuario = data['nombre_usuario']
        if(data['password']):
            profesor.encrypt_password(data['password'])

        profesor.save()
        return{'Response':'exito'}


class ProfesorCursos(Resource):
    def get(self, id):
        return json.loads(Curso.objects(profesor=id).all().to_json())



class Profesores(Resource):
    def get(self):
        return json.loads(Profesor.objects().all().to_json())

    def post(self):
        data = request.data.decode()
        data = json.loads(data)
        profesor = Profesor()
        profesor.nombres = data['nombres']
        profesor.apellido_paterno = data['apellido_paterno']
        profesor.apellido_materno = data['apellido_materno']
        profesor.telefono = data['telefono']
        profesor.email = data['email']
        profesor.nombre_usuario = data['nombre_usuario']
        profesor.encrypt_password(data['password'])
        profesor.save()
        return {'Response': 'exito'}