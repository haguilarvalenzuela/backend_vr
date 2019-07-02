from flask import Flask, Blueprint, jsonify, request, send_file
from models.curso import Curso
from models.alumno import Alumno
from models.profesor import Profesor
from models.administrador import Administrador
from models.evaluacion import Evaluacion
from models.respuesta import Respuesta
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
from libs.auth import token_required
from functools import wraps
from bson.objectid import ObjectId
import json
import os
from PIL import Image
from os.path import dirname, abspath

def init_module(api):
    api.add_resource(CursoCargar, '/recursos/<id_recurso>')
    api.add_resource(CursoEvalaucionAlumno, '/recursos/<id_recurso>/respuestas')
    api.add_resource(PreguntaImagen, '/preguntas/<id>')

class CursoEvalaucionAlumno(Resource):
    def put(self,id_recurso):
        if not 'auth-token' in request.headers:
            return {'response': 'no_token'},401
        user = None
        token = request.headers.get('auth_token')
        user = Alumno.load_from_token(token)
        if user == None:
            return {'response': 'user_invalid'},401
        curso = Curso.objects(id=id_recurso).first()
        if curso==None:
            return {'response': 'resource_invalid'},404
        data = request.data.decode()
        data = json.loads(data)
        alumno = user
        if not 'respuestas' in data or len(data['respuestas'])==0:
            return {'response': 'invalid_data'},404
        respuestas = data['respuestas']
        evaluacion = Evaluacion()
        evaluacion.alumno = alumno.id
        evaluacion.curso = curso.id
        for respuesta in respuestas:
            respuesta_aux = Respuesta()
            respuesta_aux.numero_pregunta = respuesta['numero_pregunta']
            respuesta_aux.correcta = respuesta['correcta']
            respuesta_aux.data = respuesta['respuesta']
            evaluacion.respuestas.append(respuesta_aux)
            evaluacion.acierto = 0
            if 'progreso' in data:
                evaluacion.acierto = data['progreso'] 
        evaluacion.save()
        return {"Response":200}

class CursoCargar(Resource):
    def get(self, id_recurso):
        if not 'auth-token' in request.headers:
            return {'response': 'no_token'},401
        user = None
        token = request.headers.get('auth_token')
        user = Alumno.load_from_token(token)
        user_prof = Profesor.load_from_token(token)
        user_admin = Administrador.load_from_token(token)
        if user == None and user_admin == None and user_prof == None:
            return {'response': 'user_invalid'},401
    
        if len(id_recurso.encode('utf-8')) != 24:
            return {'response': 'bad_request'},400
        curso = Curso.objects(id=id_recurso).first()
        if curso==None:
            return {'response': 'resource_invalid'},404
        response = {}
        response['id'] = str(curso.id)
        response['nombre'] = curso.nombre
        response['fecha_creacion'] = str(curso.fecha_creacion)
        response['asignatura'] = curso.asignatura.to_dict()
        response['profesor'] = curso.profesor.to_dict()

        contenidos = []
        for contenido in curso.contenidos:
            preguntas = []
            for pregunta in contenido.preguntas:
                print(pregunta.tipo_pregunta)
                if pregunta.tipo_pregunta == "ALTERNATIVA" or pregunta.tipo_pregunta == "VERDADERO_FALSO":
                    opciones = []
                    for opcion in pregunta.alternativas:
                        opciones.append({
                            "texto": opcion.texto,
                            "correcta": opcion.correcta
                        })
                    preguntas.append({
                        "tipo": pregunta.tipo_pregunta,
                        "imagen": pregunta.imagen,
                        "indice": pregunta.numero,
                        "texto": pregunta.texto,
                        "opciones": opciones
                    })
                if pregunta.tipo_pregunta == "TEXTO":
                    preguntas.append({
                        "tipo": pregunta.tipo_pregunta,
                        "imagen": pregunta.imagen,
                        "indice": pregunta.numero,
                        "texto": pregunta.texto
                    })
                if pregunta.tipo_pregunta == "UNIR_IMAGENES" or pregunta.tipo_pregunta == "UNIR_TEXTOS" or pregunta.tipo_pregunta == "UNIR_IMAGEN_TEXTO":
                    opciones = []
                    for opcion in pregunta.alternativas:
                        opciones.append({
                            "data": opcion.texto,
                            "data_secundaria": opcion.texto_secundario
                        })
                    preguntas.append({
                        "tipo": pregunta.tipo_pregunta,
                        "imagen": pregunta.imagen,
                        "indice": pregunta.numero,
                        "texto": pregunta.texto,
                        "opciones": opciones
                    })
            contenidos.append({
                "identificador" : contenido.identificador,
                "preguntas" : preguntas
            })
        response['contenidos'] = contenidos
        return response

class PreguntaImagen(Resource):    
    def get(self,id):
        return send_file('uploads/preguntas/'+id+'_thumbnail.jpg')

    def post(self,id):

         #Para los test
        directory_root = dirname(dirname(abspath(__file__)))
        upload_directory = os.path.join(
            str(directory_root), "flaskr/uploads/preguntas")
        imagen = Image.open(request.files['imagen'].stream).convert("RGB")
        imagen.save(os.path.join(upload_directory, str(id)+".jpg"))
        imagen.thumbnail((500, 500))
        imagen.save(os.path.join(upload_directory, str(id)+'_thumbnail.jpg'))
