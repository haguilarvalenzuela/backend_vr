import os
import tempfile
import json
import pytest

from flaskr import api
from flask import current_app
from models.categoria import Categoria
from models.institucion import Institucion

@pytest.fixture
def client():
    db_fd, api.app.config['DATABASE'] = tempfile.mkstemp()
    api.app.config['TESTING'] = True
    client = api.app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(api.app.config['DATABASE'])

def test_get_categorias(client):
	institucion = Institucion.objects().first()
	if institucion == None:
		assert True
	else:
		rv = client.get('/categorias/'+str(institucion.id))
		assert rv.data