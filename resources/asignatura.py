from flask import Flask, Blueprint, jsonify, request
from models.asignatura import Asignatura
from models.curso import Curso
from models.institucion import Institucion
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
from bson import ObjectId
import json

def init_module(api):
    api.add_resource(AsignaturaItem, '/asignaturas/<id>')
    api.add_resource(Asignaturas, '/asignaturas')
    api.add_resource(AsignaturasDetalle, '/asignaturas/detalle')
    api.add_resource(AsignaturasColegio, '/asignaturas/colegio/<id_colegio>')


class AsignaturasColegio(Resource):
    def get(self,id_colegio):
        response = []
        asignaturas = Asignatura.objects(institucion=id_colegio).all()
        for asignatura in asignaturas:
            if asignatura.activo:
                cursos_lista = []
                cursos = Curso.objects(asignatura = asignatura.id).all()
                for curso in cursos:
                    cursos_lista.append({
                        'nombre': curso.nombre
                    })
                response.append({
                    'id': str(asignatura.id),
                    'nombre': asignatura.nombre,
                    'cursos': cursos_lista
                })
        return response

    def post(self, id_colegio):
        data = request.data.decode()
        data = json.loads(data)
        asignatura = Asignatura()
        asignatura.nombre = data['nombre']
        institucion = Institucion.objects(id=id_colegio).first()
        asignatura.institucion = institucion.id
        asignatura.save()
        return {'Response': 'exito'}

class AsignaturaItem(Resource):
    def get(self, id):
        return json.loads(Asignatura.objects(id=id).first().to_json())
    
    def put(self, id):
        asignatura = Asignatura.objects(id=id).first()
        cursos = Curso.objects(asignatura = asignatura.id).all()
        for curso in cursos:
            curso.asignatura = None
            curso.save()
        data = request.data.decode()
        data = json.loads(data)
        
        asignatura.nombre = data['nombre']
        asignatura.save()
        return {'Response': 'exito'}
    
    def delete(self, id):
        asignatura = Asignatura.objects(id=id).first()
        asignatura.activo = False
        asignatura.save()
        return{'Response':'borrado'}

class Asignaturas(Resource):
    def get(self):
        asignaturas = Asignatura.objects().all()
        response = []
        for asignatura in asignaturas:
            if asignatura.activo:
                response.append(asignatura.to_dict())
        return response

    def post(self):
        data = request.data.decode()
        data = json.loads(data)
        asignatura = Asignatura()
        asignatura.nombre = data['nombre']
        asignatura.save()
        return {'Response': 'exito'}

class AsignaturasDetalle(Resource):
    def get(self):
        response = []
        asignaturas = Asignatura.objects().all()
        for asignatura in asignaturas:
            if asignatura.activo:
                cursos_lista = []
                cursos = Curso.objects(asignatura = asignatura.id).all()
                for curso in cursos:
                    cursos_lista.append({
                        'nombre': curso.nombre
                    })
                response.append({
                    'id': str(asignatura.id),
                    'nombre': asignatura.nombre,
                    'cursos': cursos_lista
                })
        return response
