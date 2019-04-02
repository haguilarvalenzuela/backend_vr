from flask import Flask, Blueprint, jsonify
from models.inscripcion import Inscripcion
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json

def init_module(api):
    api.add_resource(InscripcionItem, '/inscripciones/<id>')
    api.add_resource(Inscripciones, '/inscripciones')


class InscripcionItem(Resource):
    def get(self, id):
        return json.loads(Inscripcion.objects(id=id).first().to_json())


class Inscripciones(Resource):
    def get(self):
        print(Inscripcion.objects().all().to_json())
        return json.loads(Inscripcion.objects().all().to_json())