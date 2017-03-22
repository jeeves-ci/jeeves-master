from setuptools import setup


setup(
    zip_safe=True,
    name='jeeves-master',
    version='0.1',
    author='adaml',
    author_email='adam.lavie@gmail.com',
    packages=[
        'rest_service',
        'rest_service.resources',
    ],
    license='LICENSE',
    description='Jeeves-CI is a distributed task engine for dispatching jobs '
                'on clean docker/vms environments across workers.',
    install_requires=[
        'pika>=0.10.0',
        'flask>=0.12',
        'flask-restful==0.2.5',
        'flask-restful-swagger==0.12',
        'sqlalchemy==1.1.5',
        'pyyaml>=3.12',
        'psycopg2==2.7.1'
    ]
)
