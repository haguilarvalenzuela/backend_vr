from flask import Flask, Blueprint, jsonify, request,current_app, send_file
from models.curso import Curso
from models.curso_base import CursoBase
from models.contenido import Contenido
from models.evaluacion import Evaluacion
from models.asignatura import Asignatura
from models.institucion import Institucion
from models.profesor import Profesor
from models.alumno import Alumno
from models.pregunta import Pregunta
from models.alternativa import Alternativa
from models.inscripcion import Inscripcion
from models.categoria import Categoria
from models.habilidad import Habilidad
from models.inscripcion import TIPOS_ESTADO_INSCRIPCION as TEI
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
from pprint import pprint
import json
from PIL import Image
import os


def init_module(api):
    api.add_resource(CursoItem, '/recurso/<id>')
    api.add_resource(Cursos, '/recursos')
    api.add_resource(CursosAdmin, '/recursos/admin')
    api.add_resource(CursoDetallePut, '/recurso/detalle/put')
    api.add_resource(CursosActivos, '/recursos/activos/<id>')
    api.add_resource(CursosCerrados, '/recursos/desactivados/<id>')
    api.add_resource(CursosBase, '/recursosbase')
    api.add_resource(CursoBaseItem, '/recursobase/<id>')
    api.add_resource(CursoDetalle, '/recurso/detalle/<id>')
    api.add_resource(CursoAlumnos, '/recursos/alumnos')
    api.add_resource(CursoAlumno, '/sacar/alumno/recurso')
    api.add_resource(CursoImagenItem, '/recurso/imagen/<id>')
    api.add_resource(CursoImagenDefaultItem, '/recurso/imagen/default/<id>')
    api.add_resource(CursosAdminColegio , '/recursos/admin/colegio/<id_institucion>') 
    api.add_resource(CursosBaseColegio, '/recursosbase/colegio/<id_institucion>')
    api.add_resource(CursosActivosProfesorColegio, '/recursos/activos/profesor/colegio/<id_profesor>/<id_institucion>')
    api.add_resource(CursosDesactivadosProfesorColegio, '/recursos/desactivados/profesor/colegio/<id_profesor>/<id_institucion>')
    api.add_resource(CursosAprobacionGrafico, '/recursos/aprobacion/graficos/<id>')
    api.add_resource(CursosAsignaturaGrafico, '/recursos/asignatura/grafico')
    api.add_resource(CursoDetalleAlumno, '/recurso/detalle/alumno/<id_curso>/<id_alumno>')
    api.add_resource(CursoDisponiblesAlumno, '/recursos/disponibles/alumno/<id_alumno>')

class CursoDisponiblesAlumno(Resource):
    def get(self,id_alumno):
        response = []
        cursos = Curso.objects().all()
        alumno = Alumno.objects(id=id_alumno).first()
        for curso in cursos:
            esta_presente = False
            for alumno_aux in curso.alumnos:
                if alumno_aux.id == alumno.id:
                    esta_presente = True
            if(esta_presente==False):
                if Inscripcion.objects(curso=curso.id,alumno=alumno.id).first() == None:
                    response.append(curso.to_dict())
        return response


class CursoDetalleAlumno(Resource):
    def get(self,id_curso,id_alumno):
        curso = Curso.objects(id=id_curso).first()
        alumno = Alumno.objects(id=id_alumno).first()
        evaluacion = Evaluacion.objects(alumno=alumno.id, curso = curso.id ).first()
        respuesta = []
        alumno = alumno.to_dict()
        respuestas_alumno = []
        if evaluacion!=None:
            for habilidad_respuesta in curso.habilidades:
                preguntas_habilidad = 0
                respuestas_correctas_habilidad = 0
                for contenido in curso.contenidos:
                    for pregunta in contenido.preguntas:
                        if pregunta['habilidad'].id == habilidad_respuesta.id:
                            preguntas_habilidad = preguntas_habilidad+1
                            for respuesta_aux in evaluacion.respuestas:
                                if respuesta_aux.numero_pregunta == pregunta.numero:
                                    if respuesta_aux.correcta:
                                        respuestas_correctas_habilidad = respuestas_correctas_habilidad +1
                                    respuesta_aux = respuesta_aux.to_dict()
                                    respuesta_aux['pregunta'] = pregunta.texto
                                    respuestas_alumno.append(respuesta_aux)

                respuesta.append(
                    {   'respuesta_correctas': respuestas_correctas_habilidad,
                        'cantidad_preguntas': preguntas_habilidad,
                        'habilidad': habilidad_respuesta['nombre']
                    }
                )                      
            alumno['evaluacion'] = True
            alumno['progreso'] = evaluacion.acierto
            alumno['respuestas_data'] = respuestas_alumno
        else:
            for habilidad_respuesta in curso.habilidades:
                preguntas_habilidad = 0
                for contenido in curso.contenidos:
                    for pregunta in contenido.preguntas:
                        if pregunta['habilidad'] == habilidad_respuesta:
                            preguntas_habilidad = preguntas_habilidad+1
                respuesta.append(
                    { 'respuesta_correctas': 0,
                        'cantidad_preguntas': preguntas_habilidad,
                        'habilidad': habilidad_respuesta['nombre']
                    }
                )
            alumno['evaluacion'] = False
            alumno['progreso'] = 0
        
        alumno['respuestas'] = respuesta
        return {
                "curso": curso.to_dict(),
                "alumno": alumno
            }


class CursosAsignaturaGrafico(Resource):
    def get(self):
        labels = []
        data = []
        for asignatura in Asignatura.objects().all():
            labels.append(asignatura.nombre)
            data.append(Curso.objects(asignatura=asignatura.id).count())
        return { 'data': data, 'labels':labels}
class CursosAprobacionGrafico(Resource):
    def get(self,id):
        labels = []
        data = [
            { 'data': [], 'label': 'Aprobación' },
            { 'data': [], 'label': 'Desaprobación' }
        ]
        for curso in Curso.objects().all():
            labels.append(curso.nombre)
            data[0]['data'].append(curso.aprobacion)
            data[1]['data'].append(100-curso.aprobacion)
        return {'labels':labels, 'data':data }


class CursosActivosProfesorColegio(Resource):
    def get(self, id_profesor,id_institucion):
        institucion = Institucion.objects(id=id_institucion).first()
        profesor = Profesor.objects(id=id_profesor).first()
        response = []
        for curso in Curso.objects(activo=True, institucion=institucion.id,profesor=profesor.id).all():
            categoria = Categoria.objects(id=curso.categoria.id).first()
            curso = curso.to_dict()
            curso['categoria'] = categoria.to_dict()
            response.append(curso)
        return response

class CursosDesactivadosProfesorColegio(Resource):
    def get(self, id_profesor,id_institucion):
        institucion = Institucion.objects(id=id_institucion).first()
        profesor = Profesor.objects(id=id_profesor).first()
        response = []
        for curso in Curso.objects(activo=False, institucion=institucion.id,profesor=profesor.id).all():
            categoria = Categoria.objects(id=curso.categoria.id).first()
            curso = curso.to_dict()
            curso['categoria'] = categoria.to_dict()
            response.append(curso)
        return response


class CursosBaseColegio(Resource):
    def get(self,id_institucion):
        institucion = Institucion.objects(id = id_institucion).first()
        cursosBase = []
        for cursoBase in CursoBase.objects(institucion = id_institucion).all():
            cursosBase.append(cursoBase.to_dict())
        return cursosBase

class CursosAdminColegio(Resource):
    def get(self,id_institucion):
        institucion = Institucion.objects(id = id_institucion).first()
        cursos = []
        for curso in Curso.objects(institucion = id_institucion).all():
            cursos.append(curso.to_dict())
        return cursos

class CursoItem(Resource):
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
    
    def get(self,id):
        return Curso.objects(id=id).first().to_dict()

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
            if alumno.activo:
                evaluacion = Evaluacion.objects(alumno=alumno.id, curso = curso ).first()
                respuesta = []
                alumno = alumno.to_dict()
                if evaluacion!=None:
                    for habilidad_respuesta in curso.habilidades:
                        preguntas_habilidad = 0
                        respuestas_correctas_habilidad = 0
                        for contenido in curso.contenidos:
                            for pregunta in contenido.preguntas:
                                if pregunta['habilidad'].id == habilidad_respuesta.id:
                                    preguntas_habilidad = preguntas_habilidad+1
                                    for respuesta_aux in evaluacion.respuestas:
                                        if respuesta_aux.numero_pregunta == pregunta.numero:
                                            if respuesta_aux.correcta:
                                                respuestas_correctas_habilidad = respuestas_correctas_habilidad +1

                        respuesta.append(
                            { 'respuesta_correctas': respuestas_correctas_habilidad,
                              'cantidad_preguntas': preguntas_habilidad,
                              'habilidad': habilidad_respuesta['nombre']
                            }
                        )                         
                    alumno['evaluacion'] = True
                    alumno['progreso'] = evaluacion.acierto
                else:
                    for habilidad_respuesta in curso.habilidades:
                        print(habilidad_respuesta)
                        preguntas_habilidad = 0
                        for contenido in curso.contenidos:
                            for pregunta in contenido.preguntas:
                                if pregunta['habilidad'] == habilidad_respuesta:
                                    preguntas_habilidad = preguntas_habilidad+1
                        respuesta.append(
                            { 'respuesta_correctas': 0,
                              'cantidad_preguntas': preguntas_habilidad,
                              'habilidad': habilidad_respuesta['nombre']
                            }
                        )
                    alumno['evaluacion'] = False
                    alumno['progreso'] = 0
                alumno['respuestas'] = respuesta
                alumnos.append(alumno)
        return {
                "curso": curso.to_dict(),
                "alumnos": alumnos
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
        token = request.headers.get('auth_token')
        profesor = Profesor.load_from_token(token)
        asignatura = Asignatura.objects(id= data['asignatura']).first()
        curso_base = CursoBase.objects(id=data['curso_base']).first()
        curso = Curso()
        curso.nombre = data['nombre']
        curso.categoria = curso_base.categoria

        for habilidad_base in curso_base.habilidades:
            curso.habilidades.append(habilidad_base.id)

        for contenido_base in curso_base.contenidos:
            contenido = Contenido()
            contenido.identificador = contenido_base.identificador
            contenido.texto = contenido_base['texto']
            for pregunta_base in contenido_base['preguntas']:
                pregunta = Pregunta()
                pregunta.texto = pregunta_base['texto']
                pregunta.numero = pregunta_base['numero']
                habilidad = Habilidad.objects(id=pregunta_base['habilidad'].id).first()
                pregunta.habilidad = habilidad.id
                pregunta.tipo_pregunta = pregunta_base['tipo_pregunta']
                for alternativa_base in pregunta_base['alternativas']:
                    alternativa = Alternativa()
                    alternativa.texto = alternativa_base['texto']
                    alternativa.texto_secundario = alternativa_base['texto_secundario']
                    alternativa.correcta = alternativa_base['correcta']
                    pregunta.alternativas.append(alternativa)
                contenido.preguntas.append(pregunta)
            curso.contenidos.append(contenido)
        curso.asignatura = asignatura.id
        curso.profesor = profesor.id
        curso.activo = True
        curso.curso_base = curso_base.id
        curso.descripcion = data['descripcion']
        curso.save()
        return {'Response': 'exito', 'id': str(curso.id), 'id_base': str(curso_base.id)}

    def put(self):
        #Cargar datos dinamicos
        data = request.data.decode()
        data = json.loads(data)
        idCurso = data['id']
        data = data['data']

        cursoBase = CursoBase.objects(id=data['curso_base']).first()
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
            asignatura = ""
            if curso.profesor != None:
                profesor = curso.profesor.nombres+" "+curso.profesor.apellido_paterno
            if curso.asignatura != None:
                asignatura = curso.asignatura.nombre
            diccionario_aux ={
                "id": str(curso.id),
                "nombre": curso.nombre,
                "cant_estudiantes": len(curso.alumnos),
                "profesor": profesor,
                "nombre_asignatura": asignatura,
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
        cursosBase = []
        for cursoBase in CursoBase.objects().all():
            cursosBase.append(cursoBase.to_dict())
        return cursosBase

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
