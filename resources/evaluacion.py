from flask import Flask, Blueprint, jsonify
from models.evaluacion import Evaluacion
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json

def init_module(api):
    api.add_resource(EvaluacionItem, '/evaluaciones/<id>')
    api.add_resource(Evaluaciones, '/evaluaciones')

class EvaluacionItem(Resource):
    def get(self, id):
        return json.loads(Evaluacion.objects(id=id).first().to_json())


class Evaluaciones(Resource):
    def get(self):
        print(Evaluacion.objects().all().to_json())
        return json.loads(Evaluacion.objects().all().to_json())
