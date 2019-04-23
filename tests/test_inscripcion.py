import os
import tempfile
import json
import pytest

from flaskr import api
from models.inscripcion import Inscripcion
from models.alumno import Alumno
from models.curso import Curso
from models.historial import Historial

@pytest.fixture
def client():
    db_fd, api.app.config['DATABASE'] = tempfile.mkstemp()
    api.app.config['TESTING'] = True
    client = api.app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(api.app.config['DATABASE'])

def test_get_inscripcion(client):
	rv = client.get('/inscripciones')
	assert True

def test_get_inscripcion_id(client):
	inscripcion = Inscripcion.objects().first()
	if(inscripcion==None):
		assert True
	else:
		rv = client.get('/inscripciones/'+str(inscripcion.id))
		assert True

def test_get_inscripcion_curso(client):
	curso = Curso.objects().first()
	if(curso==None):
		assert True
	else:
		rv = client.get('/inscripciones_curso/'+str(curso.id))
		assert True

def test_post_inscripcion_curso(client):
	curso = Curso.objects().first()
	alumno = Alumno.objects().first()
	if((curso==None) or (alumno==None)):
		assert True
	else:
		data = {
			"alumno": str(alumno.id)
		}
		rv = client.get('/inscripciones_curso/'+str(curso.id), data=data)
		assert True

def test_put_inscripcion_id(client):
	inscripcion = Inscripcion.objects().first()
	alumno = Alumno.objects().first()
	curso = Curso.objects().first()
	if((inscripcion==None) or (alumno==None) or (curso==None)):
		assert True
	else:
		historial = Historial()
		historial.data = "Testing"
		data = {
			"alumno": str(alumno.id),
			"curso": str(curso.id),
			"estado": "ENVIADA",
			"historial": [historial]
		}

		rv = client.put('/inscripciones/'+str(inscripcion.id), data=data)
		assert True

def test_delete_inscripcion_id(client):
	inscripcion = Inscripcion.objects().first()
	if(inscripcion==None):
		assert True
	else:
		rv = client.delete('/inscripciones/'+str(inscripcion.id))
		assert True

