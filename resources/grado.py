from flask import Flask, Blueprint, jsonify, request
from models.grado import Grado
from models.curso import Curso
from models.alumno import Alumno
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json

def init_module(api):
    api.add_resource(GradoItem, '/grados/<id>')
    api.add_resource(Grados, '/grados')
    api.add_resource(GradosDetalle, '/grados_detalle')

class GradoItem(Resource):
    def get(self, id):
        response = []
        grado = Grado.objects(id=id).first()
        if grado != None:
            response = grado.to_dict()
        return response

    def delete(self, id):
        grado = Grado.objects(id=id).first()
        grado.activo = False
        grado.save()
        return{'Response':'borrado'}


class Grados(Resource):
    def get(self):
        response = []
        for grado in Grado.objects().all():
            if grado.activo:
                response.append(grado.to_dict())
        return response
    
    def post(self):
        data = request.data.decode()
        data = json.loads(data)
        grado = Grado()
        grado.nivel = data['nivel']
        grado.identificador = data['identificador']
        grado.save()
        return {'Response': 'exito'}

class GradosDetalle(Resource):
    def get(self):
        response = []
        grados = Grado.objects().all()
        for grado in grados:
            if grado.activo:
                cursosGrado = Curso.objects(grado=grado.id).count()
                alumnosGrados = 0 
                for alumno in Alumno.objects(grado = grado.id).all():
                    if alumno.activo:
                        alumnosGrados = alumnosGrados +1

                cursos = Curso.objects(grado=grado.id).all()
                aprobacion = 0
                for curso in cursos:
                    aprobacion = aprobacion + curso.aprobacion
                
                if cursosGrado>0:
                    aporbacion = aprobacion / cursosGrado
                response.append({
                    'id': str(grado.id),
                    'nivel': grado.nivel,
                    'identificador': grado.identificador,
                    'cant_cursos': cursosGrado,
                    'cant_alumnos': alumnosGrados,
                    'aprobacion': aprobacion
                })
        return response
