from flask import Flask, Blueprint, jsonify
from models.seccion import Seccion
from flask_restful import Api, Resource, url_for
from libs.to_dict import mongo_to_dict
import json

def init_module(api):
    api.add_resource(Secciones, '/secciones')
    api.add_resource(SeccionesItem, '/secciones/<id>')
    api.add_resource(SeccionesBanner, '/seccion_banner')
    api.add_resource(SeccionesSlider, '/seccion_slider')
    api.add_resource(SeccionesCurso, '/seccion_cursos')
    api.add_resource(SeccionesNosotros, '/seccion_nosotros')
    api.add_resource(SeccionesContacto, '/seccion_contacto')


class SeccionItem(Resource):
    def get(self, id):
        return json.loads(Seccion.objects(id=id).first().to_json())

class Secciones(Resource):
    def get(self):

    	arrayJson = []
    	secciones = Seccion.objects().all()
    	for seccion in secciones:

    		contenido = ''
    		if(seccion.tipo == "BANNER"):
    			contenido = self.renderContentBanner()

    		if(seccion.tipo == "SLIDE"):
    			contenido = self.renderContentSlider()

    		if(seccion.tipo == "CURSOS"):
    			contenido = self.renderContentCursos()

    		if(seccion.tipo == "QUIENES_SOMOS"):
    			contenido = self.renderContentNosotros()

    		if(seccion.tipo == "CONTACTO"):
    			contenido = self.renderContentContacto()

    		dataJson = {'tipo': seccion.tipo, 'contenido': contenido}
    		arrayJson.append(dataJson)
    	return arrayJson


class SeccionesBanner(Resource):
    def get(self):
        contenido = '<h1>Components</h1>'
        contenido += '<p>Provide contextual feedback messages for typical user actions with the handful of available and flexible alert messages. <a class="text-white" href="#">click here.</a></p>'
        return contenido

class SeccionesSlider(Resource):
    def get(self):
        contenido = []
        cantidad_slide = 3
        i = 1
        while(i <= 3):
            contenido.append('VRKIDS Slide {}'.format(i))
            i += 1
        return contenido

class SeccionesCursos(Resource):
    def get(self):
        contenido = 'Some quick example text from API VRKIDS  test_texttest_texttest_texttest_texttest_texttest_texttest_texttest_text'
        return contenido

class SeccionesNosotros(Resource):
    def get(self):
        titulo = 'VrFromApi'
        parrafo = 'texto prueba api texto prueba api texto prueba apitexto prueba apitexto prueba apitexto prueba apitexto prueba api texto prueba api texto prueba api texto prueba api'
        
        checklist = ['texto','texto','texto','texto','texto','texto']
        img = 'features-img1.jpg'
        imgBanner = 'background-img-2.jpg'
        textoBanner = 'texto para banner'

        contenido = {'titulo': titulo, 
                     'parrafo': parrafo, 
                     'checklist': checklist, 
                     'img': img,
                     'imgBanner': imgBanner,
                     'textoBanner': textoBanner}

        return contenido

class SeccionesContacto(Resource):
    def get(self):

        direccion = 'Direcion #123. Santiago, Chile'
        telefono = '+56 9 123 45 678'
        email = 'email@email.email'

        contenido = {'direccion': direccion, 'telefono': telefono, 'email': email}
        return contenido