import os
import tempfile
import json
import pytest

from flaskr import api
from models.administrador import Administrador

@pytest.fixture
def client():
    db_fd, api.app.config['DATABASE'] = tempfile.mkstemp()
    api.app.config['TESTING'] = True
    client = api.app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(api.app.config['DATABASE'])

def test_get_administradores(client):

	rv = client.get('/administradores')
	assert rv.data