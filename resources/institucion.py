from flask import Flask, Blueprint, jsonify
from models.institucion import Institucion
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json

def init_module(api):
    api.add_resource(InstitucionItem, '/instituciones/<id>')
    api.add_resource(Instituciones, '/instituciones')


class InstitucionItem(Resource):
    def get(self, id):
        return json.loads(Institucion.objects(id=id).first().to_json())


class Instituciones(Resource):
    def get(self):
        print(Institucion.objects().all().to_json())
        return json.loads(Institucion.objects().all().to_json())