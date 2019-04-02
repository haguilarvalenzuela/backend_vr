from flask import Flask, Blueprint, jsonify, request
from models.alumno import Alumno
from models.curso import Curso
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
from bson import ObjectId
import json

def init_module(api):
    api.add_resource(AlumnoItem, '/alumnos/<id>')
    api.add_resource(Alumnos, '/alumnos')
    api.add_resource(AlumnosColegio, '/alumnos_colegio/<id_institucion>')
    api.add_resource(AlumnoCursos, '/alumno_cursos/<id>')
    api.add_resource(AlumnosCurso, '/alumnos_curso/<id_curso>')
    api.add_resource(AlumnoCurso, '/alumno_curso/<id_curso>/<id_alumno>')



class AlumnoItem(Resource):
    def get(self, id):
        return json.loads(Alumno.objects(id=id).first().to_json())
    
    def delete(self, id):
        alumno = Alumno.objects(id=id).first()
        alumno.delete()
        return{'Response':'borrado'}

    def put(self, id):
        data = request.data.decode()
        data = json.loads(data)

        alumno = Alumno.objects(id=id).first()
        alumno.nombres = data['nombres']
        alumno.apellido_paterno = data['apellido_paterno']
        alumno.apellido_materno = data['apellido_materno']
        alumno.telefono = data['telefono']
        alumno.email = data['email']
        alumno.nombre_usuario = data['nombre_usuario']
        alumno.matricula = data['matricula']
        alumno.save()
        return{'Response':'exito'}

class AlumnoCursos(Resource):
    def get(self, id):
        cursosRespuesta = []
        cursos = Curso.objects().all()
        for curso in cursos:
            if curso.alumnos != None:
                esta_alumno = False
                for alumno in curso.alumnos:
                    if str(alumno.id) == str(id):
                        esta_alumno = True
                if esta_alumno:
                    cursosRespuesta.append({
                        "nombre": curso.nombre,
                        "id": str(curso.id),
                        "asignatura": str(curso.asignatura.id),
                        "version": curso.version,
                        "activo":curso.version
                    }) 
        return cursosRespuesta

    # def get(self):
    #     return json.loads(Alumno.objects(id=id).all().to_json())    

class AlumnosCurso(Resource):
    def get(self, id_curso):
        alumnos_array = []
        alumnos = Alumno.objects().all()
        curso = Curso.objects(id=id_curso).first()

        for alumno_obj in alumnos:
            if(alumno_obj not in curso.alumnos):
                alumnos_array.append({'id':str(alumno_obj.id), 'nombres': alumno_obj.nombres})

        return alumnos_array

class AlumnoCurso(Resource):
    def post(self, id_curso, id_alumno):
        idAlumno = ObjectId(id_alumno)
        curso = Curso.objects(id=id_curso).first()
        curso.alumnos.append(idAlumno)
        curso.save()

        return {'Response': 'exito'}

    def delete(self, id_curso, id_alumno):
        idAlumno = ObjectId(id_alumno)
        alumnos = []
        curso = Curso.objects(id=id_curso).first()
        
        for alumno in curso.alumnos:
            if(idAlumno != alumno.id):
                alumnos.append(alumno.id)

        response = Curso.objects(id=id_curso).update(
            set__alumnos = alumnos
            )
        if(response):
            return {'Response': 'exito'}    

class Alumnos(Resource):

    def post(self):
        data = request.data.decode()
        data = json.loads(data)
        data_personal = data['data_personal']
        data_academico = data['data_academico']

        alumno = Alumno()
        alumno.nombres = data_personal['nombres']
        alumno.apellido_paterno = data_personal['apellido_paterno']
        alumno.apellido_materno = data_personal['apellido_materno']
        alumno.telefono = data_personal['telefono']
        alumno.email = data_personal['email']
        alumno.nombre_usuario = data_academico['nombre_usuario']
        alumno.password = data_academico['password']
        alumno.matricula = data_academico['matricula']
        alumno.institucion = None
        alumno.save()
        return {'Response': 'exito'}

    def get(self):
        return json.loads(Alumno.objects().all().to_json())

class AlumnosColegio(Resource):
    def get(self, id_institucion):
        return json.loads(Alumno.objects(institucion = id_institucion).all().to_json())
