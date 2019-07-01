from flask import Flask, Blueprint, jsonify, request, current_app, send_file
from models.alumno import Alumno
from models.curso import Curso
from models.asignatura import Asignatura
from models.profesor import Profesor
from models.grado import Grado
from models.institucion import Institucion
from models.evaluacion import Evaluacion
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
from bson import ObjectId
import json
from PIL import Image
import os
from os.path import dirname, abspath

def init_module(api):
    api.add_resource(AlumnoItem, '/alumnos/<id>')
    api.add_resource(Alumnos, '/alumnos')
    api.add_resource(AlumnosColegio, '/alumnos/colegio/<id_institucion>')
    api.add_resource(AlumnoCursos, '/alumno/recursos/<id>')
    api.add_resource(AlumnosCurso, '/alumnos/recurso/<id_curso>')
    api.add_resource(AlumnoCurso, '/alumno/recurso/<nombre_usuario>/<id_curso>')
    api.add_resource(AlumnoImagenItem, '/alumno/imagen/<id>')
    api.add_resource(AlumnoImagenDefaultItem, '/alumno/imagen/default/<id>')
    api.add_resource(AlumnosGrado, '/alumnos/curso/<id>')
    api.add_resource(AlumnoImagenZoom, '/imagen/zoom/<id>')
    api.add_resource(AlumnoFinalizarTutorial, '/alumno/finalizar/tutorial/<id>')
    api.add_resource(AlumnoEvaluaciones, '/alumno/evaluaciones/<id>')


class AlumnoEvaluaciones(Resource):
    def get(self,id):
        evaluaciones = []
        alumno = Alumno.objects(id=id).first()
        for evaluacion in Evaluacion.objects(alumno=alumno.id).all():
            evaluaciones.append(evaluacion.to_dict())
        return evaluaciones

class AlumnoFinalizarTutorial(Resource):
    def get(self,id):
        alumno = Alumno.objects(id=id).first()
        alumno.primera_vez = False
        alumno.save()
        return{'Response':'exito'}

class AlumnoItem(Resource):
    def get(self, id):
        return json.loads(Alumno.objects(id=id).first().to_json())
    
    def delete(self, id):
        alumno = Alumno.objects(id=id).first()
        alumno.activo = False
        alumno.save()
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
        grado = Grado.objects(id = data['grado']).first()
        alumno.grado = grado.id
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
                    asignatura = Asignatura.objects(id=curso.asignatura.id).first()
                    profesor = Profesor.objects(id=curso.profesor.id).first()
                    cursosRespuesta.append(curso.to_dict()) 
        return cursosRespuesta

class AlumnosCurso(Resource):
    def get(self, id_curso):
        alumnos_array = []
        curso = Curso.objects(id=id_curso).first()
        for alumno_obj in Alumno.objects().all():
            if alumno_obj.curso == curso:
                alumnos_array.append(alumno_obj.to_dict())
        return alumnos_array

class AlumnosGrado(Resource):
    def get(self,id):
        alumnos = []
        grado = Grado.objects(id=id).first()
        for alumno in Alumno.objects().all():
            if alumno.grado == grado:
                if alumno.activo:
                    alumnos.append(alumno.to_dict())
        return alumnos
class AlumnoCurso(Resource):
    def post(self, id_curso, nombre_usuario):
        alumno = Alumno.objects(nombre_usuario= nombre_usuario).first()
        alumnos = Alumno.objects().all()
        if alumno == None:
            return {'Response': 'no_existe'}
        curso = Curso.objects(id=id_curso).first()
        if not alumno.activo:
            return {'Response': 'no_existe'}

        for alumno_aux in curso.alumnos:
            if alumno_aux.id == alumno.id:
                return {'Response': 'si_pertenece'}
        
        curso.alumnos.append(alumno.id)
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
        alumno = Alumno()
        alumno.nombres = data['data_personal']['nombres']
        alumno.apellido_paterno = data['data_personal']['apellido_paterno']
        alumno.apellido_materno = data['data_personal']['apellido_materno']
        alumno.telefono = data['data_personal']['telefono']
        alumno.email = data['data_personal']['email']
        alumno.imagen = data['data_personal']['imagen']
        alumno.nombre_usuario = data['data_academico']['nombre_usuario']        
        alumno.encrypt_password(data['data_academico']['nombre_usuario'])
        alumno.matricula = data['data_academico']['matricula']
        alumno.institucion = None
        grado = data['data_personal']['grado']
        if grado == 'None':
            alumno.grado = None
        else:    
            grado = Grado.objects(id=grado).first()
            alumno.grado = grado
        alumno.save()
        return {'Response': 'exito', 'id': str(alumno.id)}

    def get(self):
        response = []
        alumnos = Alumno.objects().all()
        for alumno in alumnos:
            if alumno.activo:
                response.append(alumno.to_dict())
        return response

class AlumnosColegio(Resource):
    def get(self, id_institucion):
        institucion = Institucion.objects(id = id_institucion).first()
        alumnos = []

        for alumno in Alumno.objects(institucion = id_institucion).all():
            alumnos.append(alumno.to_dict())
        return alumnos

    def post(self,id_institucion):
        data = request.data.decode()
        data = json.loads(data)
        alumno = Alumno()
        alumno.nombres = data['data_personal']['nombres']
        alumno.apellido_paterno = data['apellido_paterno']
        alumno.apellido_materno = data['apellido_materno']
        alumno.telefono = data['telefono']
        alumno.email = data['email']
        alumno.nombre_usuario = data['nombre_usuario']        
        alumno.encrypt_password(data['nombre_usuario'])
        alumno.matricula = data['matricula']
        institucion = Institucion.objects(id=id_institucion).first()
        alumno.institucion = institucion.id
        grado = Grado.objects(id=data['grado']).first()
        alumno.grado = grado
        alumno.save()
        return {'Response': 'exito', 'id': str(alumno.id)}

class AlumnoImagenItem(Resource):
    def post(self,id):
        #########
        # Se usa el siguiente os.path.join para la aplicación
        #########
        # upload_directory = os.path.join(current_app.config.get("UPLOAD_FOLDER", "uploads"), 
        #                                "alumnos")

        #########
        # Se usa el siguiente os.path.join para los tests
        #########
        directory_root = dirname(dirname(abspath(__file__)))
        upload_directory = os.path.join(str(directory_root), "flaskr/uploads/alumnos")

        imagen = Image.open(request.files['imagen'].stream).convert("RGB")
        image_path = os.path.join(upload_directory, "%s.jpg" % str(id))
        imagen.save(image_path)
        imagen.thumbnail((200, 100))

        image_path = os.path.join(upload_directory, "%s_thumbnail.jpg" % str(id))
        imagen.save(image_path)
        alumno = Alumno.objects(id=id).first()
        alumno.imagen = str(id)
        alumno.save()
        return {'Response': 'exito'}
    
    def get(self,id):
        #########
        # Se usa el siguiente os.path.join para la aplicación
        #########
        # upload_directory = os.path.join(current_app.config.get("UPLOAD_FOLDER", "uploads"),
        #                                "alumnos")

        #########
        # Se usa el siguiente os.path.join para los tests
        #########
        directory_root = dirname(dirname(abspath(__file__)))
        upload_directory = os.path.join(directory_root, "flaskr/uploads/alumnos")
        image_path = os.path.join(upload_directory, "%s_thumbnail.jpg" % str(id))
        return send_file(image_path)

class AlumnoImagenZoom(Resource):
    def get(self,id):
        return send_file('uploads/alumnos/'+id+'.jpg')

class AlumnoImagenDefaultItem(Resource):
    def get(self,id):
        alumno = Alumno.objects(id=id).first()
        #path = os.path.join(current_app.config.get("UPLOAD_FOLDER"), model.carpeta_archivos)
        alumno.imagen = "default"
        alumno.save()
        return {'Response':'exito'}

