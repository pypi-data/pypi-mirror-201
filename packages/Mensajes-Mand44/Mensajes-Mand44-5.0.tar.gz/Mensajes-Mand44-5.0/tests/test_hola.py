#144 (MODULOS)
'''
#import saludos         -> ESTA ES LA FORMA DE IMPORTAR TODO EL CODIGO DE saludos

#saludos.saludar()
#                               =======================================================

from saludos import saludar, Saludo   #-> ASI SE IMPORTA POR PARTES.   SE USA UN * PARA IMPORTARLO TODO.

saludar()
Saludo()
'''



#145 (PAQUETES)
'''
from mensajes.hola1.saludos import *
# NOTA:  ESTA ES LA FORMA EN LA QUE SE ESCEIBEN LOS PAQUETES, SI VEO ALGO ESCRITo (IMPORTADO) EN LA FROMA mensajes.hola1.saludos ES
#        UN PAQUETE QUE PRIMERO VISITA LA CARPETA mensajes (PAQUETE), Y LUEGO hola1 (SUBPAQUETE). 
# IMPORTATE:  AUNQUE NO ES OBLIGARTORIO, ES UTIL CREAR UN __init__ EN CADA NUEVA CARPETA DE UN PAQUETE PARA IDENTIFICARLO RAPIDAMENTE
#             Y ADEMAS EL CODIGO DENTRO DE ESTE __init__ SE EJECUTARA AUTOMATICAMENTE CUANDO SEA IMPORTADO. 

from mensajes.adios.despedidas import *

saludar()
Saludo()

despedida()
Despedida()
'''



#146
'''
from mensajes.hola1.saludos import *
from mensajes.adios.despedidas import *

saludar()
Saludo()

despedida()
Despedida()
'''


#213

import unittest
import numpy as np
from mensajes.hola1.saludos import generarArray

class Pruebas_hola(unittest.TestCase):
    def test_generar_array(self):
        np.testing.assert_array_equal(np.array([0,1,2,3,4,5]), generarArray(6))  # ESTO SERIA EQUIVALENTE A UN assertEqual() SOLO QUE EL PRIMERO
                                                                                 # SERIA LA COMPROBACION (USANDO UN GENERADOR DE ARRAYS DE np)

        #self.assertEqual()...     ESTO SERIA LO QUE HARIA TRADICIONALMENTE USANDO EL unittest

#    NOTA: LOS TEST SE PUEDEN EJECUTAR DESDE LA TERMINAL CON ESTA SINTAXIS:  python setup.py test (SIEMPRE Y CUANDO ESTE AFUERA, EN LA RAIZ)

