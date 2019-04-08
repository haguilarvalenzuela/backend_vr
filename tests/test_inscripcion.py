import os
import tempfile
import json
import pytest

from flaskr import api
from models.inscripcion import Inscripcion

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
