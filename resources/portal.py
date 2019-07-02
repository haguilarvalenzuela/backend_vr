from flask import Flask, Blueprint, jsonify
from models.portal import Portal
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json

def init_module(api):
    api.add_resource(PortalItem, '/portales/<id>')
    api.add_resource(Portales, '/portales')


class PortalItem(Resource):
    def get(self, id):
        return json.loads(Portal.objects(id=id).first().to_json())


class Portales(Resource):
    def get(self):
        return json.loads(Portal.objects().all().to_json())