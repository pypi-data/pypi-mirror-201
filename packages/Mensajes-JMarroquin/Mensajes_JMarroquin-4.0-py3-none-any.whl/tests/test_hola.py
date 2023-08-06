import unittest
import numpy as np
from Mensajes.Hola.saludos import generar_array


class Pruebas_Hola(unittest.TestCase):
    def test_generar_array(self):
        np.testing.assert_array_equal(
            np.array([0,1,2,3,4,5]),
            generar_array(6)
        )


#from Mensajes.saludos import saludar   Le decimos el nombre del archvivo y que modulo queremos
#from Mensajes.Hola.saludos import *    Para tener acceso a todas las definiciones del modulo
#from Mensajes.Adios.despedidas import *
#Nombre del paquete, nombre del subpaquete, nombre del modulo

