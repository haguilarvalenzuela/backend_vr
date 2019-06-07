import os
import tempfile
import json
import pytest
import random
import string

from flaskr import api
from models.alumno import Alumno

@pytest.fixture
def client():
    db_fd, api.app.config['DATABASE'] = tempfile.mkstemp()
    api.app.config['TESTING'] = True
    client = api.app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(api.app.config['DATABASE'])

def test_curso_cargar_failed(client):

    with api.app.app_context():
        alumno = Alumno.objects().first()
        if alumno == None:
            return 'Alumno no existe'
        token = alumno.get_token()
        letters = string.ascii_lowercase
        id_invalid_resource = ''.join(random.choice(letters) for i in range(23))
        rv = client.get('/recursos/'+id_invalid_resource, headers={'auth_token':token})
        response = rv.data.decode("utf-8")
        response_json = json.loads(response)
        rsp_msg = response_json['response']    
        if rsp_msg == 'no_token':
            assert b'no_token' in rv.data

        if rsp_msg == 'bad_request':
            assert b'bad_request' in rv.data

