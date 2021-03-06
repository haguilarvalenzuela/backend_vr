from flask import Flask, Blueprint, jsonify, request
from models.inscripcion import Inscripcion
from models.historial import Historial
from models.alumno import Alumno
from models.curso import Curso
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
from bson import ObjectId
import json

def init_module(api):
    api.add_resource(InscripcionItem, '/inscripciones/<id>')
    api.add_resource(Inscripciones, '/inscripciones')
    api.add_resource(InscripcionCurso, '/inscripciones/recurso/<id>')
    api.add_resource(InscripcionesAlumno, '/inscripciones/alumno/<id>')
    api.add_resource(InscripcionesCursoAceptar, '/aceptar/inscripciones/recurso/<id>')

class InscripcionesCursoAceptar(Resource):
    def post(self,id):
        curso = Curso.objects(id=id).first()
        for inscripcion in Inscripcion.objects(curso=curso.id).all():
            if inscripcion.estado == "ENVIADA":
                alumno = Alumno.objects(id=inscripcion.alumno.id).first()
                curso.alumnos.append(alumno)
                historial = Historial()
                historial.data = "Solcitud aceptada por profesor "+curso.profesor.nombres+" "+curso.profesor.apellido_paterno+" "+curso.profesor.apellido_materno
                inscripcion.estado= "ACEPTADA"
                inscripcion.historial.append(historial)
                inscripcion.save()
                curso.save()
        return {"Response":"exito"}                

class InscripcionItem(Resource):
    def get(self, id):
        return json.loads(Inscripcion.objects(id=id).first().to_json())

    def delete(self, id):
        inscripcion = Inscripcion.objects(id=id).first()
        inscripcion.delete()
        return{'Response':'borrado'}

    def put(self, id):        
        data = request.data.decode()
        data = json.loads(data)
        inscripcion = Inscripcion.objects(id=id).first()
        
        inscripcion.estado = data['estado']
        historial = Historial()
        historial.data = data['mensaje']
        inscripcion.historial.append(historial)

        if data['estado'] == 'ACEPTADA':
            alumno = Alumno.objects(id=inscripcion.alumno.id).first()
            curso = Curso.objects(id = inscripcion.curso.id).first()
            curso.alumnos.append(alumno)
            curso.save()

        inscripcion.save()
        return{'Response':'exito'}


class Inscripciones(Resource):
    def get(self):
        return json.loads(Inscripcion.objects().all().to_json())

class InscripcionCurso(Resource):
    def get(self, id):
        return json.loads(Inscripcion.objects(curso=id).all().to_json())

    def post(self, id):
        data = request.data.decode()
        data = json.loads(data)

        historial = Historial()
        historial.data = "solicitud enviada por alumno"

        inscripcion = Inscripcion()
        inscripcion.alumno = ObjectId(data['id_alumno'])
        inscripcion.curso = ObjectId(id)
        inscripcion.estado = "ENVIADA"
        inscripcion.historial = [historial]
        inscripcion.save()
        return {'response': 'exito'}

class InscripcionesAlumno(Resource):
    def get(self, id):

        response = []
        historial = []
        inscripciones = Inscripcion.objects(alumno=id).all()


        for inscripcion in inscripciones:
            for obj in inscripcion.historial:
                historial.append({
                    'fecha': str(obj.fecha),
                    'data': obj.data
                    })
            response.append({
                'id': str(inscripcion.id),
                'curso': inscripcion.curso.to_dict(),
                'profesor': inscripcion.curso.profesor.to_dict(),
                'estado': inscripcion.estado,
                'historial': historial
                })

        return response
