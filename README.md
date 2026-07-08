# djangoRepositorio
Aplicación para guardar libros, cd's, aplicaciones, etc


## Instalación

Debe tener instalado python 3.14.

Se debe ejecutar lo siguiente para instalarlo

`git clone https://github.com/JSanzM/djangoRepositorio.git`

`cd djangoRepositorio`

`virtualenv .venv`

`source .venv/bin/activate`

`pip  install -r requirementes.txt`


## Crear la base de datos y los modelos
`cd repositorio`

`python manage.py migrate`



## Para ejecutarlo siempre

Desde el directorio djangoRepositorio/repositorio

`python manage.py runserver`


