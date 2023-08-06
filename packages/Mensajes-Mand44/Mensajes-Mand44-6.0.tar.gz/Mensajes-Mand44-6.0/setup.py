#146 (DISTRIBUCION)
#   IMPORTANTE: PARA DISTRIBUIR UN CODIGO ES NECESARIO CREAR FUERA DE LAS CARPETAS ESTE ARCHIVO, UN setup.py ANTES QUE NADA.
#   Y TAMBIEN EL COGIO DE AQUI ABAJO:

#213 (ESTA RELACIONADO AL 146)
#214

from struct import pack
from setuptools import setup, find_packages
setup(
    name = 'Mensajes-Mand44',
    version = '6.0',
    description= 'Un paquete para saludar y despedir',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # ESTA PEDE SER LA SOLUCION PARA ALGUNOS ERRORES COMUNES EN twine
    author = 'Manuel',
    author_email= 'manu@el.dev',
    url= 'https://manuel.dev',
    license_files=['LICENSE'],
    packages = find_packages(),       #ESTA SERIA LA FORMA AUTOMATICA DE AGREGAR PACKAGES
    #packages = ['mensajes', 'mensajes.hola1', 'mensajes.adios'],     ESTA SERIA LA FROMA MANUAL DE AGREGAR LOS PAQUETES
    scripts = [],
    test_suite = 'tests',
    #install_requires = ['numpy']   ESTA SERIA LA FORMA MANUAL DE AGREGAR PAQUETES EXTERNOS, Y PARA ESPECIFICAR VERSIONES: ['numpy>=1.24.0']
    install_requires = [paquetes.strip() for paquetes in open('requirements.txt').readlines()], 
    # ESTA ES UNA FORMA AUTOMATIZADA DE AGREGAR PAQUETES EXTERNOS, CREANDO UN ARCHIVO txt PARA LUEGO RECORRERLO USANDO UN for Y open 
    classifiers=['Environment :: Console',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 3.11',
                 'Programming Language :: Python :: 3.12',
                 'Topic :: Utilities']   #   ESTOS CLASIFICADORES LOS PUEDO SACAR DE INTERNET (DE LA PAGINA DE pypi.org POR EJEMPLO)

)

#   NOTA:  DESPUES DE TERMINAR DE ESCRIBIR EL CODIGO DE ARRIBA, TENGO QUE ABRIR LA TERMINAL O CONSOLA Y ESCRIBIR (DESDE DONDE APAREZCA
#          LA DIRECCION DE ESTE ARCHIVO):  python setup.py sdist  ESTO GENERARA LA CARPETA  dist  LA CUAL CONTENDRA EL ARCHIVO 
#          QUE ME INTERESA. ENTONCES VUELO A ABRIE LA CONSOLA Y PONGO PRIMERO  cd dist  (APRIETO ENTER) Y LUEGO PONGO 
#          pip install (nombre del archivo dentro de la carpeta dist) 
        #NOTA:  SI NO FUNCIONA CON EL (nombre del archivo dentro de la carpeta dist) AGREGAR  .gz  AL FINAL.
#          DESPUES DE ESTO PUEDO EJECUTAR EL CODIGO LOCALMENTE ABRIENDO EL cmd O INCLUSO DESDE PYTHON. PARA ESTO PRIMERO 
#          PONGO python(enter) Y LUEGO from (lo que desee) import * Y LUEGO YA PUEDO EJECUTAR LA FUNCION QUE DESEE. TAMBIEN SE PUEDE
#          DESDE Jupyter.

#   NOTA:  PARA CREAR UNA ACTUALIZACION DEL PROGRAMA SOLO TENDRIA QUE PRIMERO MODIFICAR LO QUE QUISIERA DEL CODIGO Y DESPUES 
#          CAMBIAR DE 1.0 A 2.0 EN version Y VOLVER A EJECUTAR EL CODIGO DE ARRIBA PERO PRIMERO YENDO A cd .. (enter, es la raiz)
#          Y LUEGO  python setup.py sdist (ESTO CREARA OTRO ARCHIVO DENTRO DE LA CARPETA dist PERO EN 2.0) DESPUES DE ESTO HAY
#          QUE EJECITAR EN LA TERMINAL EL  pip install (nombre)2.0 --upgrade (SI NO FUNCIONA PROCURA PRIMERO PONER cd dist antes de pip install...)

#   NOTA:  SI QUISIERA BORRAR EL PAQUETE TENDRIA QUE IR A LA CONSOLA (COMO EL cmd) Y PONER pip uninstall (nombre)


# NOTA( DEL 214): ES IMPORTANTE INSTALAR DESDE LA TERMINAL: pip install build twine, DESPUES DE AGREGAR LOS CALSIFICADORES SI ES QUE 
#                 VAMOS A PUBLICAR EL ARCHIVO EN INTERNET. 
#                 DESPUES ESCRIBO LO SIGUIENTE: python -m build (ENTER). PARA CREAR LOS DISTRIBUIBLES (COMO LA CARPETA dist... ASI: Mensajes-Mand44-5.0.tar.gz)
#                 DESPUES SE ESCRIBE: python -m twine check dist/* PARA COMPROBAR QUE TODOS LOS PAQUETES ESTAN BIEN.

# PARA SUBIR LOS FICHEROS A INTERNET EN MODO Test: PRIMERO SE HACE LO DE ARRIBA, LUEGO SE ESCRIBE: python -m twine upload -r testpypi dist/*
#                                                  DESPUES NOS VA A PEDIR NUESTRO NOMBRE DE USUARIO, ETC. 
# PARA SUBIR LOS FICHEROS A INTERNET OFICIAMENTE: SE ESCRIBE: python -m twine upload dist/*