from flask import Flask, Blueprint, jsonify, request,current_app, send_file
from models.curso import Curso
from models.curso_base import CursoBase
from models.evaluacion import Evaluacion
from models.grado import Grado
from models.asignatura import Asignatura
from models.institucion import Institucion
from models.profesor import Profesor
from models.alumno import Alumno
from models.pregunta import Pregunta
from models.alternativa import Alternativa
from models.inscripcion import Inscripcion
from models.inscripcion import TIPOS_ESTADO_INSCRIPCION as TEI
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
from pprint import pprint
import json
from PIL import Image
import os


def init_module(api):
    api.add_resource(CursoItem, '/cursos/<id>')
    api.add_resource(Cursos, '/cursos')
    api.add_resource(CursosAdmin, '/cursos_admin')
    api.add_resource(CursoDetallePut, '/curso_detalle_put')
    api.add_resource(CursosActivos, '/cursos_activos/<id>')
    api.add_resource(CursosCerrados, '/cursos_desactivados/<id>')
    api.add_resource(CursosBase, '/cursos_base')
    api.add_resource(CursoBaseItem, '/curso_base/<id>')
    api.add_resource(CursoDetalle, '/curso_detalle/<id>')
    api.add_resource(CursoAlumnos, '/cursos_alumnos')
    api.add_resource(CursoAlumno, '/sacar_alumno_curso')
    api.add_resource(CursosGrado, '/cursos_grado/<id_grado>/<id_alumno>')
    api.add_resource(CursoAgregarAlumnos, '/agregar_alumnos_curso/<id>')
    api.add_resource(CursoImagenItem, '/curso_imagen/<id>')
    api.add_resource(CursoImagenDefaultItem, '/curso_imagen_default/<id>')
    api.add_resource(CursosDeGrado, '/cursos_de_grado/<id>')

class CursoAgregarAlumnos(Resource):
    def post(self,id):
        curso = Curso.objects(id=id).first()
        alumnos = Alumno.objects(grado = curso.grado).all()
        for alumno in alumnos:
            if not alumno in curso.alumnos:
                if alumno.activo:
                    curso.alumnos.append(alumno)
        curso.save()
        return {'Response': 'exito'}

class CursoItem(Resource):
    def get(self, id):
        return json.loads(Curso.objects(id=id).first().to_json())
    
    def put(self, id):
        curso = Curso.objects(id=id).first()
        curso.activo = False
        curso.save()
        return {'Response':'exito'}

    def delete(self, id):
        curso = Curso.objects(id=id).first()
        curso.activo = False
        curso.save()
        return{'Response':'exito'}

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
        cant_estudiantes = 0
        for alumno in curso.alumnos:
            if alumno.activo:
                cant_estudiantes = cant_estudiantes +1
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

                else:
                    for pregunta in curso.preguntas:
                        respuestas.append({
                            "correcta" : 'no_hizo',
                            "pregunta" : 0
                        })
                        #contador_respuestas = contador_respuestas + 1
                alumnos.append({
                    "id": str(alumno.id),
                    "nombre" :alumno_detalle.nombres,
                    "nombre_usuario":alumno_detalle.nombre_usuario,
                    "respuestas" : respuestas,
                    "progreso": progreso 
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

        grado_nivel = ""
        grado_identificador = ""
        asignatura=""
        if curso.grado != None:
            grado_nivel = str(curso.grado.nivel)
            grado_identificador = curso.grado.identificador
        if curso.asignatura != None:
            asignatura = curso.asignatura.nombre

        return {
                "nombre_curso": curso.nombre,
                "descripcion": curso.descripcion,
                "cant_estudiantes": cant_estudiantes,
                "progreso": curso.aprobacion,
                "nombre_asignatura": asignatura ,
                "grado_nivel": grado_nivel,
                "grado_identificador": grado_identificador,
                "codigo_curso": str(curso.id),
                "curso_base": curso.curso_base.nombre,
                "version": curso.version,
                "alumnos": alumnos,
                "preguntas": preguntas,
                "imagen": curso.imagen
            }

class Cursos(Resource):
    def get(self):
        response =[]
        for curso in Curso.objects().all():
            response.append(curso.to_dict())
        return response


    def post(self):
        data = request.data.decode()
        data = json.loads(data)
        print(data)
        asignatura = Asignatura.objects(id= data['asignatura']).first()
        profesor = Profesor.objects(id=data['profesor']).first()
        grado = Grado.objects(id=data['grado']).first()
        curso_base = CursoBase.objects(id=data['curso_base']).first()
        curso = Curso()
        curso.nombre = data['nombre']
        curso.grado = grado.id

        for pregunta_base in curso_base.preguntas:
            pregunta = Pregunta()
            pregunta.texto = pregunta_base['texto']
            pregunta.tipo_pregunta = pregunta_base['tipo_pregunta']
            for alternativa_base in pregunta_base['alternativas']:
                alternativa = Alternativa()
                alternativa.texto = alternativa_base['texto']
                alternativa.correcta = alternativa_base['correcta']
                pregunta.alternativas.append(alternativa)
            curso.preguntas.append(pregunta)

        curso.asignatura = asignatura.id
        curso.profesor = profesor.id
        curso.activo = True
        curso.curso_base = curso_base.id
        curso.descripcion = data['descripcion']
        curso.save()

        print(str(curso.id))
        return {'Response': 'exito', 'id': str(curso.id), 'id_base': str(curso_base.id)}

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
            profesor = ""
            grado = ""
            asignatura = ""
            if curso.profesor != None:
                profesor = curso.profesor.nombres+" "+curso.profesor.apellido_paterno
            if curso.grado != None:
                grado = curso.grado.getGrado()
            if curso.asignatura != None:
                asignatura = curso.asignatura.nombre
            diccionario_aux ={
                "id": str(curso.id),
                "nombre": curso.nombre,
                "cant_estudiantes": len(curso.alumnos),
                "profesor": profesor,
                "nombre_asignatura": asignatura,
                "grado": grado,
                "codigo_curso": str(curso.id),
                "curso_base": curso.curso_base.nombre,
                "version": curso.version,
                "creacion": str(curso.fecha_creacion),
                "activo": curso.activo,
                "imagen": curso.imagen
            }
            resultado.append(diccionario_aux)
        return resultado

class CursosActivos(Resource):
    def get(self, id):
        cursos = []
        for curso in Curso.objects(activo=True,profesor=id).all():
            cursos.append(curso.to_dict())
        return cursos

class CursosCerrados(Resource):
    def get(self, id):
        cursos = []
        for curso in Curso.objects(activo=False,profesor=id).all():
            cursos.append(curso.to_dict())
        return cursos

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

class CursoAlumno(Resource):
    def post(self):
        data = request.data.decode()
        data = json.loads(data)
        curso = Curso.objects(id=data['id_curso']).first()
        alumno = Alumno.objects(id=data['id_alumno']).first()
        curso.alumnos.remove(alumno)
        curso.save()
        return {'Response': 'exito'}


class CursosGrado(Resource):
    def get(self, id_grado, id_alumno):

        inscripciones = Inscripcion.objects(alumno=id_alumno).all()

        response = Curso.objects(grado=id_grado, alumnos__ne=id_alumno).all()
        cursos = []

        for curso in response:
            flag = False
            for inscripcion in inscripciones:
                if(curso.id == inscripcion.curso.id):
                    flag = True
            if(flag==False):
                cursos.append({
                    'id': str(curso.id),
                    'nombre': curso.nombre,
                    'fecha_creacion': str(curso.fecha_creacion),
                    'asignatura': str(curso.asignatura),
                    'profesor': str(curso.profesor)
                    })
            
        return cursos

class CursoImagenItem(Resource):
    def post(self,id):
        imagen = Image.open(request.files['imagen'].stream).convert("RGB")
        imagen.save(os.path.join("./uploads/cursos", str(id)+".jpg"))
        imagen.thumbnail((500, 500))
        imagen.save(os.path.join("./uploads/cursos", str(id)+'_thumbnail.jpg'))
        curso = Curso.objects(id=id).first()
        curso.imagen = str(id)
        curso.save()
        return {'Response': 'exito'}
    
    def get(self,id):
        return send_file('uploads/cursos/'+id+'_thumbnail.jpg')

class CursoImagenDefaultItem(Resource):
    def get(self,id):
        curso = Curso.objects(id=id).first()
        print(curso)
        curso_base = CursoBase.objects(id=curso.curso_base.id).first()
        imagen = Image.open("./uploads/cursos/"+str(curso_base.id)+".jpg")
        imagen.save(os.path.join("./uploads/cursos", str(id)+".jpg"))
        imagen.thumbnail((500, 500))
        imagen.save(os.path.join("./uploads/cursos", str(id)+'_thumbnail.jpg'))
        curso = Curso.objects(id=id).first()
        curso.imagen = str(id)
        curso.save()
        return {'Response': 'exito'}

class CursosDeGrado(Resource):
    def get(self,id):
        response =[]
        grado = Grado.objects(id=id).first()
        for curso in Curso.objects().all():
            if curso.grado == grado:
                response.append(curso.to_dict())
        return response
