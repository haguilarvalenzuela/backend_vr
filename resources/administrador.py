from flask import Flask, Blueprint, jsonify, request
from models.administrador import Administrador
from models.asignatura import Asignatura
from models.institucion import Institucion
from models.evaluacion import Evaluacion
from models.curso import Curso

from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json

def init_module(api):
    api.add_resource(AdministradorItem, '/administradores/<id>')
    api.add_resource(Administradores, '/administradores')

def AdminGenerate():
    administrador = Administrador.objects().all()
    if(len(administrador) == 0):
        admin = Administrador()
        admin.nombres = 'admin'
        admin.apellido_paterno = 'paterno'
        admin.apellido_materno = 'materno'
        admin.email = 'admin@admin.cl'
        admin.telefono = '+56999999999'
        admin.nombre_usuario = 'admin'
        admin.encrypt_password('pass')
        admin.save()

class AdministradorItem(Resource):
    def get(self, id):
        return json.loads(Administrador.objects(id=id).first().to_json())

    def put(self,id):
        data = request.data.decode()
        data = json.loads(data)
        administrador = Administrador.objects(id=id).first()
        administrador.nombres = data['nombres']
        administrador.apellido_paterno = data['apellido_paterno']
        administrador.apellido_materno = data['apellido_materno']
        administrador.email = data['email']
        administrador.telefono = data['telefono']
        administrador.nombre_usuario = data['nombre_usuario']
        administrador.encrypt_password(data['password'])
        administrador.save()
        return {'Response': 'exito'}


class Administradores(Resource):
    def get(self):
        print(Administrador.objects().all().to_json())
        return json.loads(Administrador.objects().all().to_json())
		