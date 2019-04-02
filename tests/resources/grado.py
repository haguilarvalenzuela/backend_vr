from flask import Flask, Blueprint, jsonify
from models.grado import Grado
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json

def init_module(api):
    api.add_resource(GradoItem, '/grados/<id>')
    api.add_resource(Grados, '/grados')

class GradoItem(Resource):
    def get(self, id):
        return json.loads(Grado.objects(id=id).first().to_json())


class Grados(Resource):
    def get(self):
        return json.loads(Grado.objects().all().to_json())
