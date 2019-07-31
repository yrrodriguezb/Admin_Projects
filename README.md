## Admin Projects

Es un proyecto para la administración, configuración, colaboración de los diferentes proyectos que existen en el sistema.

Para poder ejecutar este proyecto se debe tener en cuenta las siguientes condiciones:

  1. [virtualenv](https://virtualenv.pypa.io/en/latest/)
  2. [python version 3.6.8](https://www.python.org/downloads/release/python-368/)
  3. [pip](https://pypi.org/project/pip/)


### Pasos de Instalación
  1. Clonar el proyecto: `git clone https://github.com/yrrodriguezb/Admin_Projects.git`
  2. Ingresar al directorio del proyecto: `cd Admin_Projects`
  3. Crear un entono virtual: `virtualenv venv --python=python3`
  4. Activar el entorno virtual: `source venv/bin/activate`
  5. Instalar los requerimientos: `pip3 install -r requirements.txt`
  6. Realizar la migraciones de [Django](https://www.djangoproject.com/): `python manage.py migrate`
  7. Ejecutar el servidor: `python manage.py runserver`

Para desactivar el entono virtual ejecutar: `deactivate`

**Nota**: El entornno virtual y el proyecto pueden estar en directorios diferentes.
   