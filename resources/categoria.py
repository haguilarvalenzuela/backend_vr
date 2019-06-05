from flask import Flask, Blueprint, jsonify, request, send_file
from models.categoria import Categoria
from models.curso import Curso
from models.curso_base import CursoBase
from models.institucion import Institucion
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json

def init_module(api):
    api.add_resource(Categorias, '/categorias/<id>')
    api.add_resource(CategoriaImagenItem, '/categoria_imagen/<id>')
    api.add_resource(CategoriaImagenDefaultItem, '/categoria_imagen_default/<id>')

class Categorias(Resource):
    def get(self,id):
        response = []
        institucion = Institucion.objects(id=id).first()
        for categoria in Categoria.objects().all():
            if categoria.activo:
                cursos = Curso.objects(categoria=categoria.id, institucion=institucion.id).count()
                cursosBase = CursoBase.objects(categoria=categoria.id).count()
                categoria = categoria.to_dict()
                categoria['cursos']=cursos
                categoria['cursosBase']=cursosBase
                response.append(categoria)
        return response

class CategoriaImagenItem(Resource):
    def get(self,id):
        return send_file('uploads/categorias/'+id+'_thumbnail.jpg')

class CategoriaImagenDefaultItem(Resource):
    def get(self,id):
        categoria = Categoria.objects(id=id).first()
        categoria.imagen = "default"
        categoria.save()
        return {'Response': 'exito'}