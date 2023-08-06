#144 (MODULOS)
'''
#def saludar():                                          -> REVISAR test.py PARA VER EL RESTO DE LAS NOTAS COMPLEMENTARIAS
    #print('Hola, te saludo desde saludos.saludar')

#print(__name__)        -> LO USE PARA SABER EL VALO DE __name__ SI LO EJECUTO DESDE EL ORIGEN; saludos.py

#if __name__ == '__main__':
#   IMPORTANTE: ESTE CODIGO if EN ESPECIFICO SE USA PARA QUE, A LA HORA DE IMPORTAR ESTE CODIGO (O CUALQUIER OTRO) A OTRO ARICHIVO, 
#               NO SE EJECUTE DOS VECES EL CODIGO, YA QUE SI IMPORTO ESTE CODIGO A OTRO ARCHIVO Y LO LLAMO DESDE ALLA ENTONCES
#               SE VA A EJECUTAR DESDE ALLA PERO TAMBIEN AQUI (DOBLE VEZ), ENTONCES CON ESTE if YA SE IMPIDE ESTO Y SOLO SE EJECUTA
#               EL CODIGO QUE SE DESEE DESDE EL OTRO ARCHIVO. 
#               DE HECHO, DESDE AQUI, EL ORIGEN DEL IMPORT, EL __name__ ES IGUAL A __main__ PERO SI LO EJECUTARA, POR EJEMPLO DESDE
#               test.py ENTONCES TENDRIA EL NOMBRE saludos (EL NOMBRE DEL ARCHIVO).
    #saludar()
#                                       =============================================

def saludar(): 
    print('Hola, te saludo desde saludos.saludar')

class Saludo():
    def __init__(self):
        print('Hola, te saludo desde Saludo.__init__')
'''



#145 (PAQUETES)
'''
def saludar(): 
    print('Hola, te saludo desde saludos.saludar')
class Saludo():
    def __init__(self):
        print('Hola, te saludo desde Saludo.__init__')
'''



#146
'''
def saludar(): 
    print('Hola, te saludo desde saludos.saludar')
class Saludo():
    def __init__(self):
        print('Hola, te saludo desde Saludo.__init__')

def prueba():
    print('Esto es una prueba de la nueva version.')
'''




#213
import numpy as np

def saludar(): 
    print('Hola, te saludo desde saludos.saludar')
class Saludo():
    def __init__(self):
        print('Hola, te saludo desde Saludo.__init__')

def generarArray(numeros):
    return np.arange(numeros)    #MANERA DE GENERAR UN array USANDO numpy

def prueba():
    print('Esto es una nueva prueba de la nueva version 6.0.')

if __name__ == '__main__':
    print(generarArray(5))