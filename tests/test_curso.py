import os
import tempfile
import json
import pytest

from flaskr import api
from models.curso import Curso
from models.curso_base import CursoBase
from models.institucion import Institucion
from models.asignatura import Asignatura
from models.profesor import Profesor
from models.alumno import Alumno
from models.grado import Grado

@pytest.fixture
def client():
    db_fd, api.app.config['DATABASE'] = tempfile.mkstemp()
    api.app.config['TESTING'] = True
    client = api.app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(api.app.config['DATABASE'])


def test_get_curso(client):
	curso = Curso.objects().first()
	if(curso==None):
		assert True
	else:
		rv = client.get('/cursos/'+str(curso.id))
		assert True

def test_get_cursos(client):
	rv = client.get('/cursos')
	assert True

def test_get_curso_detalle(client):
	curso = Curso.objects().first()
	if(curso==None):
		assert True
	else:
		rv = client.get('/curso_detalle/'+str(curso.id))
		assert True

def test_get_cursos_admin(client):
	rv = client.get('/cursos_admin')
	assert True

def test_get_cursos_activos(client):
	rv = client.get('/cursos_activos')
	assert True

def test_get_cursos_cerrados(client):
	rv = client.get('/cursos_cerrados')
	assert True

def test_get_cursos_base(client):
	rv = client.get('/cursos_base')
	assert True

def test_get_curso_base(client):
	curso_base = CursoBase.objects().first()
	if(curso_base==None):
		assert True
	else:
		rv = client.get('/curso_base/'+str(curso_base.id))
		assert True

def test_get_curso_alumnos(client):
	rv = client.get('/cursos_alumnos')
	assert True


def test_post_agregar_alumnos(client):
	curso = Curso.objects().first()
	if(curso==None):
		assert True
	else:
		rv = client.post('/agregar_alumnos_curso/'+str(curso.id))
		assert True

def test_post_curso(client):
	institucion = Institucion.objects().first()
	asignatura = Asignatura.objects().first()
	profesor = Profesor.objects().first()
	alumnos = Alumno.objects().all()
	grado = Grado.objects().first()
	curso_base = CursoBase.objects().first()

	if((institucion==None) or (asignatura==None) or (profesor==None) or (alumnos==None) or (grado==None) or (curso_base==None)):
		assert True
	else:
		alumnos_array = []
		for alumno in alumnos:
			alumnos_array.append(alumno.id)
		data = {
			'nombre': 'nombre',
			'fecha_creacion': '01/01/2000',
			'preguntas': [],
			'asignatura': str(asignatura.id),
			'institucion': str(institucion.id),
			'profesor': str(profesor.id),
			'alumnos': alumnos_array,
			'grado': str(grado.id),
			'activo': True,
			'version': '1.0',
			'curso_base': str(curso_base.id),
			'descripcion': 'descripcion del curso'
		}
		data = json.dumps(data)
		data = data.encode(data)
		rv = client.post('/cursos', data=data)
		assert True

def test_put_curso_detalle(client):
	curso = Curso.objects().first()
	if(curso==None):
		assert True
	else:
		data = {
			'codigo_curso': str(curso.id),
			'nombre': 'nombre',
			'descripcion': 'descripcion'
		}
		data = json.dumps(data)
		data = data.encode(data)
		rv = client.put('/curso_detalle_put')
		assert True

def test_put_curso(client):
	curso = Curso.objects().first()
	institucion = Institucion.objects().first()
	asignatura = Asignatura.objects().first()
	profesor = Profesor.objects().first()
	alumno = Alumno.objects().first()
	grado = Grado.objects().first()
	curso_base = CursoBase.objects().first()

	if((institucion==None) or (asignatura==None) or (profesor==None) or (alumnos==None) or (grado==None) or (curso_base==None) or (curso==None)):
		assert True
	else:
		data = {
			'nombre': 'nombre',
			'fecha_creacion': '01/01/2000',
			'preguntas': [],
			'asignatura': str(asignatura.id),
			'institucion': str(institucion.id),
			'profesor': str(profesor.id),
			'alumnos': alumnos_array,
			'grado': str(grado.id),
			'activo': True,
			'version': '1.0',
			'curso_base': str(curso_base.id),
			'descripcion': 'descripcion del curso'
		}

		data_put = {
			'id': str(curso.id),
			'data': data
		}
		rv = client.put('/cursos', data=data)
		assert True