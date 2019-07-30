## Admin Projects

Es un proyecto para la administración, configuración, colaboración de los diferentes proyectos que existen en el sistema.

Para poder ejecutar este proyecto se debe tener en cuenta las siguientes condiciones:

  1. [virtualenv]('https://virtualenv.pypa.io/en/latest/')
  2. [python version 3.6.8]('https://www.python.org/downloads/')
  3. [pip]('https://pypi.org/project/pip/')


### Pasos de Instalación
  
  1. Crear un entono virtual: `virtualenv venv --python=python3`
  2. Activar el entorno virtual: `source venv/bin/activate`
  3. Instalar lo requirements.txt: `pip3 install -r requirements.txt`
  4. Realizar la migraciones de [Django]('https://www.djangoproject.com/'): `python manage.py migrate`
  5. Ejecutar el servidor: `python manage.py runserver`

Para desactivar el entono virtual ejecutar: `deactivate`

**Nota**: El entornno virtual y el proyecto pueden estar en directorios diferentes.
   