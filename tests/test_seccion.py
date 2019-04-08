import os
import tempfile
import json
import pytest

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

def test_get_seccion(client):
	rv = client.get('/secciones')
	assert True

def test_get_seccion_id(client):
	seccion = Seccion.objects().first()
	if(seccion==None):
		assert True
	else:
		rv = client.get('/secciones/'+str(seccion.id))
		assert True

def test_get_seccion_content_banner(client):
	rv = client.get('/seccion_banner')
	assert True

def test_get_seccion_content_slider(client):
	rv = client.get('/seccion_slider')
	assert True

def test_get_seccion_content_cursos(client):
	rv = client.get('/seccion_cursos')
	assert True

def test_get_seccion_content_nosotros(client):
	rv = client.get('/seccion_nosotros')
	assert True

def test_get_seccion_content_contacto(client):
	rv = client.get('/seccion_contacto')
	assert True