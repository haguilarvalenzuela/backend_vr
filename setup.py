import io

from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    url='http://flask.pocoo.org/docs/tutorial/',
    license='BSD',
    maintainer='Nice Dev',
    maintainer_email='',
    description='Testing for vr.',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
    extras_require={
        'test': [
            'pytest',
        ],
    },
)