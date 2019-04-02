from flask import Flask, Blueprint, jsonify, request
from models.curso import Curso
from models.curso_base import CursoBase
from models.evaluacion import Evaluacion
from models.grado import Grado
from models.asignatura import Asignatura
from models.institucion import Institucion
from models.profesor import Profesor
from models.alumno import Alumno
from models.pregunta import Pregunta
from models.inscripcion import Inscripcion
from models.inscripcion import TIPOS_ESTADO_INSCRIPCION as TEI
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
from pprint import pprint
import json

def init_module(api):
    api.add_resource(CursoItem, '/cursos/<id>')
    api.add_resource(Cursos, '/cursos')
    api.add_resource(CursosAdmin, '/cursos_admin')
    api.add_resource(CursoDetallePut, '/curso_detalle_put')
    api.add_resource(CursosActivos, '/cursos_activos')
    api.add_resource(CursosCerrados, '/cursos_desactivos')
    api.add_resource(CursosBase, '/cursos_base')
    api.add_resource(CursoBaseItem, '/curso_base/<id>')
    api.add_resource(CursoDetalle, '/curso_detalle/<id>')
    api.add_resource(CursoAlumnos, '/cursos_alumnos')


class CursoItem(Resource):
    def get(self, id):
        return json.loads(Curso.objects(id=id).first().to_json())

class CursoDetallePut(Resource):
    def put(self):
        #Cargar datos dinamicos
        data = request.data.decode()
        data = json.loads(data)
        data = data['data']
        curso = Curso.objects(id=data['codigo_curso']).first()
        curso.nombre = data['nombre']
        curso.descripcion = data['descripcion']
        #for pregunta in data['preguntas']:
        curso.save()

        return {'test': 'test'}

class CursoDetalle(Resource):
    def get(self, id):
        curso = Curso.objects(id=id).first()
        alumnos = []
        for alumno in curso.alumnos:
            alumno_detalle = Alumno.objects(id = alumno.id).first()
            evaluacion = Evaluacion.objects(alumno=alumno_detalle, curso = curso ).first()
            respuestas = []
            cantidad_correctas = 0
            contador_respuestas = 1
            progreso = 0
            if(evaluacion!=None):
                for respuesta in evaluacion.respuestas:
                    if respuesta.correcta:
                        cantidad_correctas = cantidad_correctas + 1
                    respuestas.append({
                        "correcta" : respuesta.correcta,
                        "pregunta" : contador_respuestas
                    })
                    contador_respuestas = contador_respuestas + 1
                progreso =int(cantidad_correctas/len(evaluacion.respuestas)*100)
            alumnos.append({
                "nombre" :alumno_detalle.nombres,
                "respuestas" : respuestas,
                "progreso": progreso 
            })
        inscripciones = []
        inscripciones_curso = Inscripcion.objects(curso = curso).all()
        for inscripcion in inscripciones_curso:
            if inscripcion.estado == "ENVIADA":
                inscripciones.append({
                    "nombre_alumno": inscripcion.alumno.nombres,
                    "apellido_paterno": inscripcion.alumno.apellido_paterno,
                    "apellido_materno": inscripcion.alumno.apellido_materno,
                    "nombre_usuario": inscripcion.alumno.nombre_usuario,
                    "fecha": "15/03/19",
                    "estado": inscripcion.estado
                })
        
        preguntas = []
        contador_preguntas = 1
        for pregunta in curso.preguntas:
            alternativas = []
            id_alternativa = 0
            for alternativa in pregunta.alternativas:
                alternativas.append({
                    "texto" : alternativa.texto,
                    "correcta": alternativa.correcta,
                    "id": id_alternativa
                })
                id_alternativa = id_alternativa + 1
            preguntas.append(
                {
                    "numero_pregunta" : contador_preguntas,
                    "texto_pregunta" : pregunta.texto,
                    "tipo_pregunta": pregunta.tipo_pregunta,
                    "alternativas": alternativas
                }
            )
            contador_preguntas = contador_preguntas + 1
        return {
                "nombre_curso": curso.nombre,
                "descripcion": curso.descripcion,
                "cant_estudiantes": len(curso.alumnos) or 0,
                "progreso": 50,
                "nombre_asignatura": curso.asignatura.nombre ,
                "grado_nivel": curso.grado.nivel or 0,
                "grado_identificador": curso.grado.identificador or "",
                "codigo_curso": str(curso.id) or "",
                "curso_base": curso.curso_base.nombre or "",
                "version": curso.version or "",
                "alumnos": alumnos,
                "inscripciones": inscripciones,
                "preguntas": preguntas
            }

class Cursos(Resource):
    def get(self):

        return json.loads(Curso.objects().all().to_json())

    def post(self):
        data = request.data.decode()
        data = json.loads(data)
        data = data['data']

        cursoBase = CursoBase.objects().first()
        grado = Grado.objects().first()
        asignatura = Asignatura.objects().first()
        institucion = Institucion.objects().first()
        profesor = Profesor.objects().first()
        alumnos = Alumno.objects().first()
        pregunta = []
    

        curso = Curso()
        curso.nombre = data['nombre']
        curso.fecha_creacion = '10/06/2019'
        curso.preguntas = []
        curso.descripcion = data['descripcion']
        curso.asignatura = asignatura.id
        curso.institucion = institucion.id
        curso.profesor = profesor.id
        curso.alumnos = [alumnos.id]
        curso.grado = grado.id
        curso.activo = True
        curso.version = data['version']
        curso.curso_base = cursoBase.id
        curso.save()

        return {'Response': 'Data saved in DB'}

    def put(self):
        #Cargar datos dinamicos
        data = request.data.decode()
        data = json.loads(data)
        idCurso = data['id']
        data = data['data']

        cursoBase = CursoBase.objects(id=data['curso_base']).first()
        grado = Grado.objects(id=data['grado']).first()
        asignatura = Asignatura.objects(id=data['asignatura']).first()
        institucion = Institucion.objects(id=data['institucion']).first()
        profesor = Profesor.objects(id=data['profesor']).first()
        alumnos = Alumno.objects(id=data['alumnos']).first()
        pregunta = Pregunta()

        curso = Curso.objects(id=idCurso).first()
        curso.nombre = data['nombre']
        curso.fecha_creacion = '10/06/2012'
        curso.preguntas = [pregunta]
        curso.asignatura = asignatura.id
        curso.institucion = institucion.id
        curso.profesor = profesor.id
        curso.alumnos = [alumnos.id]
        curso.grado = grado.id
        curso.activo = True
        curso.version = data['version']
        curso.curso_base = cursoBase.id
        curso.save()

        return {'test': 'test'}

class CursosAdmin(Resource):
    def get(self):
        resultado = []
        cursos = Curso.objects().all()
        for curso in cursos:
            diccionario_aux ={
                "id": str(curso.id),
                "nombre": curso.nombre,
                "cant_estudiantes": len(curso.alumnos),
                "profesor": curso.profesor.nombres,
                "nombre_asignatura": curso.asignatura.nombre,
                "grado": curso.grado.getGrado(),
                "codigo_curso": str(curso.id),
                "curso_base": curso.curso_base.nombre,
                "version": curso.version,
                "creacion": str(curso.fecha_creacion)
            }
            resultado.append(diccionario_aux)
        return resultado

class CursosActivos(Resource):
    def get(self):
        resultado = []
        cursos = Curso.objects().all()
        for curso in cursos:
            alumnos = []
            if curso.activo:
                evaluaciones = Evaluacion.objects(curso = curso).all()
                cantidad_aprobacion = 0
                for evaluacion in evaluaciones:
                    cantidad_aprobacion= cantidad_aprobacion + (evaluacion.acierto or 0)
                if cantidad_aprobacion>0:
                    cantidad_aprobacion = cantidad_aprobacion/len(evaluaciones)


                for alumno in curso.alumnos:
                    alumnos.append( {'id': str(alumno.id), 'nombres': alumno.nombres, 'apellido_paterno': alumno.apellido_paterno,
                        'apellido_materno': alumno.apellido_materno, 'email': alumno.email} )

                diccionario_aux ={
                    "id": str(curso.id),
                    "nombre": curso.nombre or "",
                    "descripcion": curso.descripcion or "",
                    "estudiantes": alumnos,
                    "cant_estudiantes": len(curso.alumnos) or 0,
                    "profesor": curso.profesor.nombres or "",
                    "progreso": 50,
                    "asignatura": str(curso.asignatura.id) or "",
                    "nombre_asignatura": curso.asignatura.nombre or "",
                    "grado": curso.grado.getGrado() or "",
                    "codigo_curso": str(curso.id) or "",
                    "curso_base": curso.curso_base.nombre or "",
                    "version": curso.version or ""
                }
                resultado.append(diccionario_aux)
        return resultado

class CursosCerrados(Resource):
    def get(self):
        resultado = []
        cursos = Curso.objects().all()
        for curso in cursos:
            if not(curso.activo):
                evaluaciones = Evaluacion.objects(curso = curso).all()
                cantidad_aprobacion = 0
                for evaluacion in evaluaciones:
                    cantidad_aprobacion= cantidad_aprobacion + evaluacion.acierto
                if cantidad_aprobacion>0:
                    cantidad_aprobacion = cantidad_aprobacion/len(evaluaciones)
                diccionario_aux ={
                    "nombre": curso.nombre,
                    "cant_estudiantes": len(curso.alumnos),
                    "profesor": curso.profesor.nombres,
                    "progreso": cantidad_aprobacion,
                    "asignatura": str(curso.asignatura.id),
                    "nombre_asignatura": curso.asignatura.nombre,
                    "grado": curso.grado.getGrado(),
                    "codigo_curso": str(curso.id),
                    "curso_base": curso.curso_base.nombre,
                    "version": curso.version
                }
                resultado.append(diccionario_aux)
        return resultado

class CursosBase(Resource):
    def get(self):
        return json.loads(CursoBase.objects().all().to_json())

class CursoBaseItem(Resource):
    def get(self, id):
        return json.loads(CursoBase.objects(id=id).first().to_json())

class CursoAlumnos(Resource):
    def get(self):
        cursos = Curso.objects().all()

        results = []
        for curso in cursos:
            if curso.activo:
                for alumno in curso.alumnos:
                    results.append( {'nombres': alumno.nombres, 'apellido_paterno': alumno.apellido_paterno,
                        'apellido_materno': alumno.apellido_materno, 'email': alumno.email, 'nombre_curso': curso.nombre,
                        'asignatura_curso': curso.asignatura.nombre, 'id': str(alumno.id)} )



        return results

