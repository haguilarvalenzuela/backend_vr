from flask import Flask, Blueprint, jsonify, request
from models.asignatura import Asignatura
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json

def init_module(api):
    api.add_resource(AsignaturaItem, '/asignaturas/<id>')
    api.add_resource(Asignaturas, '/asignaturas')

class AsignaturaItem(Resource):
    def get(self, id):
        return json.loads(Asignatura.objects(id=id).first().to_json())
    
    def put(self, id):
        asignatura = Asignatura.objects(id=id).first()
        data = request.data.decode()
        data = json.loads(data)
        asignatura.nombre = data['nombre']
        asignatura.save()
        return {'Response': 'exito'}
    
    def delete(self, id):
        asignatura = Asignatura.objects(id=id).first()
        asignatura.delete()
        return{'Response':'borrado'}

class Asignaturas(Resource):
    def get(self):
        return json.loads(Asignatura.objects().all().to_json())

    def post(self):
        data = request.data.decode()
        data = json.loads(data)
        asignatura = Asignatura()
        asignatura.nombre = data['nombre']
        asignatura.save()
        return {'Response': 'exito'}
