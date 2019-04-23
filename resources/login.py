from flask import Flask, Blueprint, jsonify, request
from models.alumno import Alumno
from models.administrador import Administrador
from models.profesor import Profesor
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json

def init_module(api):
    api.add_resource(Login, '/login')
    api.add_resource(Logout, '/logout')


class Login(Resource):
    def post(self):
        data = request.data.decode()
        data = json.loads(data)
        
        if data['tipo'] == 'ADMINISTRADOR':
            administrador = Administrador.objects(email = data['email']).first()
            if administrador == None :
                return {'respuesta': 'no_existe'}
            else:
                #if(administrador.password == data['password']):
                if(administrador.check_password(data['password'])):
                    return {'respuesta':{'id':str(administrador.id), 'institucion': str(administrador.institucion.id) } , 'tipo': 'ADMINISTRADOR'}
                else:
                    return {'respuesta': 'no_existe'}
        if data['tipo'] == 'PROFESOR':
            profesor = Profesor.objects(email = data['email']).first()
            if profesor == None :
                return {'respuesta': 'no_existe'}
            if not profesor.activo:
                return {'respuesta': 'no_existe'}
            else:
                if(profesor.password == data['password']):
                    return { 'respuesta': json.loads(profesor.to_json()), 'tipo': 'PROFESOR'}
                else:
                    return {'respuesta': 'no_existe'}

        if data['tipo'] == 'ALUMNO':
            alumno = Alumno.objects(email= data['email']).first()
            if alumno == None:
                return {'respuesta': 'no_existe'}
            if not alumno.activo:
                return {'respuesta': 'no_existe'}
            else:
                if(alumno.check_password(data['password'])):
                    return {'respuesta': json.loads(alumno.to_json()), 'tipo': 'ALUMNO'}
                else:
                    return {'respuesta': 'no_existe'}

class Logout(Resource):
    def post(self):
        return {'respuesta': True}