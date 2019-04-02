import os
import tempfile

import pytest

from flaskr import api
from models.profesor import Profesor


@pytest.fixture
def client():
    db_fd, api.app.config['DATABASE'] = tempfile.mkstemp()
    api.app.config['TESTING'] = True
    client = api.app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(api.app.config['DATABASE'])

def test_get_profesores(client):

    rv = client.get('/profesores')
    assert rv.data

def test_get_profesor_id(client):

	profesor = Profesor.objects().first()
	rv = client.get('/profesores/'+str(profesor.id))
	assert rv.data