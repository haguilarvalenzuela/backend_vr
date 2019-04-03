from flask import Flask, Blueprint, jsonify
from models.administrador import Administrador
from models.asignatura import Asignatura
from models.institucion import Institucion
from models.evaluacion import Evaluacion
from models.curso import Curso

from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json

def init_module(api):
    api.add_resource(AdministradorItem, '/administradores/<id>')
    api.add_resource(Administradores, '/administradores')
    api.add_resource(DataChartDoug, '/data_chart_doug/<institucionId>')
    api.add_resource(DataCharBar, '/data_chart_bar/<institucionId>' )



class AdministradorItem(Resource):
    def get(self, id):
        return json.loads(Administrador.objects(id=id).first().to_json())


class Administradores(Resource):
    def get(self):
        print(Administrador.objects().all().to_json())
        return json.loads(Administrador.objects().all().to_json())
		