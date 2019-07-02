import os
import tempfile
import json
import pytest
from io import BytesIO
from os.path import dirname, abspath
from flaskr import api
from models.seccion import Seccion

@pytest.fixture
def client():
    db_fd, api.app.config['DATABASE'] = tempfile.mkstemp()
    api.app.config['TESTING'] = True
    client = api.app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(api.app.config['DATABASE'])

def test_delete_secciones(client):
	seccion = Seccion.objects().first()
	if seccion == None:
		assert True
	else:
		rv = client.delete('/secciones/'+str(seccion.id))
		if rv._status_code == 200:
			assert True
		else:
			assert False

def test_put_seccion_subir(client):
	seccion = Seccion.objects().first()
	if seccion == None:
		assert True
	else:
		rv = client.put('/seccion/subir/'+str(seccion.id))
		if rv._status_code == 200:
			assert True
		else:
			assert False

def test_put_seccion_bajar(client):
	seccion = Seccion.objects().first()
	if seccion == None:
		assert True
	else:
		rv = client.put('/seccion/bajar/'+str(seccion.id))
		if rv._status_code == 200:
			assert True
		else:
			assert False

def test_post_seccion_imagen(client):
	with api.app.app_context():
		seccion = Seccion.objects().first()
		if seccion == None:
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
				rv = client.post('/seccion/imagen/'+str(seccion.id), data=data)
				if rv._status_code == 200:
					assert True
				else:
					assert False

def test_get_seccion_imagen(client):
	seccion = Seccion.objects().first()
	if seccion == None:
		assert True
	else:
		rv = client.get('/seccion/imagen/'+str(seccion.id))
		if rv._status_code == 200:
			assert True
		else:
			assert False

def test_get_seccion_imagen_original(client):
	seccion = Seccion.objects().first()
	if seccion == None:
		assert True
	else:
		rv = client.get('/seccion/imagen/original/'+str(seccion.id))
		if rv._status_code == 200:
			assert True
		else:
			assert False


def test_get_seccion_imagen_default(client):
	seccion = Seccion.objects().first()
	if seccion == None:
		assert True
	else:
		rv = client.get('/seccion/imagen/default/'+str(seccion.id))
		if rv._status_code == 200:
			assert True
		else:
			assert False
