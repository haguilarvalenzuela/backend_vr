import os
import tempfile
import json
import pytest

from io import BytesIO
from os.path import dirname, abspath
from flaskr import api
from models.institucion import Institucion

@pytest.fixture
def client():
    db_fd, api.app.config['DATABASE'] = tempfile.mkstemp()
    api.app.config['TESTING'] = True
    client = api.app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(api.app.config['DATABASE'])

def test_get_institucion_item(client):
	institucion = Institucion.objects().first()
	if institucion == None:
		assert True
	else:
		rv = client.get('/instituciones/'+str(institucion.id))
		if rv._status_code == 200:
			assert True
		else:
			assert False

def test_get_instituciones(client):
	rv = client.get('/instituciones')
	if rv._status_code == 200:
		assert True
	else:
		assert False

def test_get_institucion_identificador(client):
	institucion = Institucion.objects().first()
	if institucion == None:
		assert True
	else:
		rv = client.get('/institucion/identificador/'+institucion.identificador)
		if rv._status_code == 200:
			assert True
		else:
			assert False

def test_post_institucion_imagen(client):
	with api.app.app_context():

		institucion = Institucion.objects().first()
		if institucion == None:
			assert True
		else:
			directory_root = dirname(dirname(abspath(__file__)))
			path_img = os.path.join(str(directory_root),
			                        "flaskr/uploads/categorias/default.jpg")
        	
			with open(path_img, 'rb') as img_open:
				img = BytesIO(img_open.read())
				data = {
					'imagen': (img, 'img.jpg')
				}
				rv = client.post('/institucion/imagen/'+str(institucion.id),
				                 content_type='multipart/form-data', data=data)
				if rv._status_code == 200:
					assert True
				else:
					assert False

def test_get_institucion_imagen(client):
	institucion = Institucion.objects().first()
	if institucion == None:
		assert True
	else:
		rv = client.get('/institucion/imagen/'+str(institucion.id))
		if rv._status_code == 200:
			assert True
		else:
			assert False

def test_get_institucion_imagen_default(client):
	institucion = Institucion.objects().first()
	if institucion == None:
		assert True
	else:
		rv = client.get('/institucion/imagen/default/'+str(institucion.id))
		if rv._status_code == 200:
			assert True
		else:
			assert False
